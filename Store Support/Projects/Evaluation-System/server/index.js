/**
 * Main Server
 * Express API for evaluation system
 */

import express from 'express';
import fileUpload from 'express-fileupload';
import cors from 'cors';
import dataProcessor from './dataProcessor.js';
import evaluationEngine from './evaluationEngine.js';
import { evaluationFields, evaluationPeriods } from './config.js';
import templateEngine from './templateEngine.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ limit: '50mb', extended: true }));
app.use(fileUpload({
  limits: { fileSize: 50 * 1024 * 1024 },
  useTempFiles: false
}));

// Serve static files
app.use(express.static(path.join(__dirname, '../client')));

/**
 * Get field definitions for mapping interface
 */
app.get('/api/fields', (req, res) => {
  res.json({
    fields: evaluationFields,
    periods: evaluationPeriods,
    categories: Object.keys(evaluationFields).reduce((cats, field) => {
      const cat = evaluationFields[field].category;
      if (!cats.includes(cat)) cats.push(cat);
      return cats;
    }, [])
  });
});

/**
 * Upload and parse file
 */
app.post('/api/upload', async (req, res) => {
  try {
    if (!req.files || !req.files.file) {
      return res.status(400).json({ error: 'No file provided' });
    }

    const file = req.files.file;
    const parsedData = await dataProcessor.parseFile(file.data, file.name);
    const headers = dataProcessor.getHeaders(parsedData);

    res.json({
      success: true,
      data: parsedData.slice(0, 5), // First 5 rows for preview
      totalRows: parsedData.length,
      availableColumns: headers,
      fullData: parsedData // Send full data for client-side processing
    });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

/**
 * Manual data entry
 */
app.post('/api/projects/manual', (req, res) => {
  try {
    const { projects } = req.body;
    if (!projects || !Array.isArray(projects)) {
      return res.status(400).json({ error: 'Invalid projects data' });
    }

    res.json({
      success: true,
      projectsReceived: projects.length
    });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

/**
 * Process mapped data and generate evaluation
 */
app.post('/api/evaluate', async (req, res) => {
  try {
    const { data, columnMappings, userInfo } = req.body;

    if (!data || !columnMappings) {
      return res.status(400).json({ error: 'Missing data or column mappings' });
    }

    // Map the data
    const mappedData = dataProcessor.mapData(data, columnMappings);

    // Validate required fields
    const requiredFields = ['project_name', 'description', 'accomplishment'];
    const validation = dataProcessor.validateData(mappedData, requiredFields);

    if (!validation.isValid) {
      return res.status(400).json({
        error: 'Data validation failed',
        errors: validation.errors
      });
    }

    // Generate summary
    const summary = dataProcessor.generateSummary(mappedData);

    // Generate evaluation
    const evaluation = evaluationEngine.generateEvaluation(
      mappedData,
      summary,
      userInfo
    );

    // Calculate score
    const score = evaluationEngine.calculateScore(mappedData, summary);

    res.json({
      success: true,
      evaluation,
      score,
      summary
    });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

/**
 * Generate HTML output
 */
app.post('/api/generate-html', async (req, res) => {
  try {
    const { evaluation, userInfo, score } = req.body;

    if (!evaluation) {
      return res.status(400).json({ error: 'No evaluation data provided' });
    }

    const html = templateEngine.generateHTML(evaluation, score, userInfo);

    res.json({
      success: true,
      html: html
    });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

/**
 * Download evaluation as HTML file
 */
app.post('/api/download-html', async (req, res) => {
  try {
    const { evaluation, userInfo, score } = req.body;

    if (!evaluation) {
      return res.status(400).json({ error: 'No evaluation data provided' });
    }

    const html = templateEngine.generateHTML(evaluation, score, userInfo);
    const filename = `Evaluation_${userInfo.name || 'Employee'}_${new Date().toISOString().split('T')[0]}.html`;

    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.setHeader('Content-Disposition', `attachment; filename=${filename}`);
    res.send(html);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

/**
 * Health check
 */
app.get('/api/health', (req, res) => {
  res.json({ status: 'Server is running', timestamp: new Date().toISOString() });
});

/**
 * Serve index.html for all other routes
 */
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../client/index.html'));
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ error: 'Internal server error' });
});

app.listen(PORT, () => {
  console.log(`
╔════════════════════════════════════════╗
║   Evaluation System Server Running     ║
╠════════════════════════════════════════╣
║   URL: http://localhost:${PORT}           ║
║   API: http://localhost:${PORT}/api       ║
║   Upload: POST /api/upload             ║
║   Evaluate: POST /api/evaluate         ║
║   Download: POST /api/download-html    ║
╚════════════════════════════════════════╝
  `);
});

export default app;
