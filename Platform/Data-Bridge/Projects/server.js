/**
 * Projects Data-Bridge Backend Server - Main Entry Point
 * 
 * Integrates storage, validation, sync, and API for Projects data bridge
 * Runs on port 8002 as the "Projects Data-Bridge Admin API" service
 * 
 * Usage:
 *   node server.js
 *   
 * Environment Variables:
 *   PORT: Server port (default 8002)
 *   STORAGE_DIR: Base storage directory (default ./storage)
 *   SYNC_INTERVAL_MS: Auto-sync interval in milliseconds (default 3600000 = 1 hour)
 */

const express = require('express');
const cors = require('cors');
const path = require('path');

// Import Projects backend modules
const ProjectsStorage = require('./projects-storage');
const ProjectsValidator = require('./projects-validator');
const ProjectsSync = require('./projects-sync');
const { initializeProjectsAPI } = require('./projects-api');

// Configuration
const PORT = process.env.PORT || 8002;
const STORAGE_DIR = process.env.STORAGE_DIR || path.join(__dirname, 'storage');
const SYNC_INTERVAL_MS = process.env.SYNC_INTERVAL_MS || 3600000; // 1 hour

// Initialize Express app
const app = express();

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public')); // Serve frontend files if any

// Initialize backend services
console.log('[Projects Backend] Initializing services...');

const storage = new ProjectsStorage(STORAGE_DIR);
const validator = new ProjectsValidator();
const sync = new ProjectsSync(storage, validator);

console.log(`[Projects Backend] Storage initialized at: ${STORAGE_DIR}`);
console.log('[Projects Backend] Schema validator loaded');
console.log('[Projects Backend] Sync service ready');

// Initialize API routes
const projectsAPI = initializeProjectsAPI(storage, validator, sync);
app.use('/api', projectsAPI);

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    service: 'Projects Backend',
    port: PORT,
    storage: {
      path: STORAGE_DIR,
      ...storage.getStorageStats()
    }
  });
});

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    service: 'Activity Hub - Projects Backend',
    version: '1.0.0',
    endpoints: {
      projects: '/api/projects',
      templates: '/api/templates/{type}',
      sync: '/api/sync/status',
      health: '/health'
    }
  });
});

// Error handling
app.use((err, req, res, next) => {
  console.error('[Projects Backend] Error:', err);
  res.status(500).json({
    success: false,
    error: err.message
  });
});

// Handle 404
app.use((req, res) => {
  res.status(404).json({
    success: false,
    error: 'Endpoint not found'
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`[Projects Backend] Server running on port ${PORT}`);
  console.log(`[Projects Backend] Base URL: http://localhost:${PORT}`);
  console.log(`[Projects Backend] Health check: http://localhost:${PORT}/health`);
  console.log(`[Projects Backend] API docs: http://localhost:${PORT}`);

  // Set up periodic sync if configured
  if (SYNC_INTERVAL_MS > 0) {
    console.log(`[Projects Backend] Auto-sync enabled every ${SYNC_INTERVAL_MS}ms`);
    
    setInterval(async () => {
      console.log('[Projects Backend] Running scheduled sync...');
      const result = await sync.syncFromIntakeHub();
      console.log('[Projects Backend] Scheduled sync complete:', {
        success: result.success,
        synced: result.stats.synced,
        failed: result.stats.failed
      });
    }, SYNC_INTERVAL_MS);
  }
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('[Projects Backend] SIGTERM received, shutting down...');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('[Projects Backend] SIGINT received, shutting down...');
  process.exit(0);
});

module.exports = app;
