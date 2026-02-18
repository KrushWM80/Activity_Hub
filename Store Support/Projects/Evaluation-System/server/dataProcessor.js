/**
 * Data Processor
 * Handles parsing, mapping, and transformation of user data
 */

import fs from 'fs';
import csv from 'csv-parser';
import { Readable } from 'stream';
import XLSX from 'xlsx';

class DataProcessor {
  /**
   * Parse CSV from buffer
   */
  async parseCSV(buffer) {
    return new Promise((resolve, reject) => {
      const data = [];
      Readable.from(buffer.toString().split('\n').map(line => line + '\n'))
        .pipe(csv())
        .on('data', (row) => data.push(row))
        .on('error', reject)
        .on('end', () => resolve(data));
    });
  }

  /**
   * Parse Excel from buffer
   */
  async parseExcel(buffer) {
    try {
      const workbook = XLSX.read(buffer, { type: 'buffer' });
      const sheetName = workbook.SheetNames[0];
      const data = XLSX.utils.sheet_to_json(workbook.Sheets[sheetName]);
      return data;
    } catch (error) {
      throw new Error(`Failed to parse Excel file: ${error.message}`);
    }
  }

  /**
   * Detect file type from buffer
   */
  detectFileType(filename) {
    const ext = filename.toLowerCase().split('.').pop();
    if (['csv', 'txt'].includes(ext)) return 'csv';
    if (['xlsx', 'xls', 'xlsm'].includes(ext)) return 'excel';
    throw new Error(`Unsupported file type: ${ext}`);
  }

  /**
   * Parse any supported file format
   */
  async parseFile(buffer, filename) {
    const type = this.detectFileType(filename);
    if (type === 'csv') {
      return await this.parseCSV(buffer);
    } else if (type === 'excel') {
      return await this.parseExcel(buffer);
    }
  }

  /**
   * Extract column headers from data
   */
  getHeaders(data) {
    if (!data || data.length === 0) return [];
    return Object.keys(data[0]);
  }

  /**
   * Map user columns to system fields
   * mappings: { userColumn: 'systemFieldName' }
   */
  mapData(rawData, columnMappings) {
    if (!rawData || rawData.length === 0) {
      throw new Error('No data provided');
    }

    return rawData.map(row => {
      const mappedRow = {};
      Object.entries(columnMappings).forEach(([userColumn, systemField]) => {
        if (row[userColumn] !== undefined) {
          mappedRow[systemField] = row[userColumn].toString().trim();
        }
      });
      return mappedRow;
    });
  }

  /**
   * Validate mapped data
   */
  validateData(mappedData, requiredFields) {
    const errors = [];
    
    mappedData.forEach((row, index) => {
      requiredFields.forEach(field => {
        if (!row[field] || row[field].trim() === '') {
          errors.push(`Row ${index + 1}: Missing required field "${field}"`);
        }
      });
    });

    return {
      isValid: errors.length === 0,
      errors
    };
  }

  /**
   * Generate summary statistics from mapped data
   */
  generateSummary(mappedData) {
    const summary = {
      totalProjects: mappedData.length,
      projectsByStatus: {},
      totalHours: 0,
      totalTeamMembers: 0,
      departments: new Set(),
      metrics: [],
      dateRange: {
        earliest: null,
        latest: null
      }
    };

    mappedData.forEach(project => {
      // Count by status
      if (project.project_status) {
        summary.projectsByStatus[project.project_status] = 
          (summary.projectsByStatus[project.project_status] || 0) + 1;
      }

      // Accumulate hours
      if (project.hours_invested) {
        summary.totalHours += parseInt(project.hours_invested) || 0;
      }

      // Count team members
      if (project.team_size) {
        summary.totalTeamMembers += parseInt(project.team_size) || 0;
      }

      // Collect departments
      if (project.team_departments) {
        project.team_departments
          .split(',')
          .map(d => d.trim())
          .forEach(dept => summary.departments.add(dept));
      }

      // Track metrics
      if (project.metrics_value && project.metrics_label) {
        summary.metrics.push({
          label: project.metrics_label,
          value: project.metrics_value,
          businessValue: project.business_value
        });
      }

      // Track date range
      if (project.start_date) {
        const startDate = new Date(project.start_date);
        if (!summary.dateRange.earliest || startDate < summary.dateRange.earliest) {
          summary.dateRange.earliest = startDate;
        }
      }

      if (project.end_date) {
        const endDate = new Date(project.end_date);
        if (!summary.dateRange.latest || endDate > summary.dateRange.latest) {
          summary.dateRange.latest = endDate;
        }
      }
    });

    summary.departments = Array.from(summary.departments);

    return summary;
  }
}

export default new DataProcessor();
