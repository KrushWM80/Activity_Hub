/**
 * Projects Sync Service - Intake Hub Data Bridge
 * 
 * Syncs projects from Intake Hub BigQuery to local Projects storage
 * Applies field mappings and transformations from Data-Bridge config
 * 
 * Sync Modes:
 * - Scheduled: Runs on timer (hourly/daily, configurable)
 * - On-Demand: Triggered by UI request
 * - Batch: One-time import
 */

const fs = require('fs');
const path = require('path');

class ProjectsSync {
  constructor(storage, validator, mappingPath = '../../../Interface/Admin/Data-Bridge/Mappings/Projects/intake-hub-mapping.json') {
    this.storage = storage;
    this.validator = validator;
    this.mapping = this.loadMapping(mappingPath);
    this.isSyncing = false;
    this.lastSyncTime = null;
  }

  /**
   * Load field mappings from config
   */
  loadMapping(mappingPath) {
    try {
      const fullPath = path.resolve(__dirname, mappingPath);
      return JSON.parse(fs.readFileSync(fullPath, 'utf8'));
    } catch (error) {
      console.warn('Failed to load mappings:', error.message);
      return null;
    }
  }

  /**
   * Sync from Intake Hub (mock implementation - real would use BigQuery)
   * In production: Connect to BigQuery client and query Intake Hub table
   */
  async syncFromIntakeHub(intakeHubData = null) {
    if (this.isSyncing) {
      throw new Error('Sync already in progress');
    }

    const startTime = Date.now();
    this.isSyncing = true;
    const stats = {
      synced: 0,
      failed: 0,
      errors: [],
      warnings: [],
      skipped: 0
    };

    try {
      // In production: Query BigQuery
      // const intakeHubData = await this.queryIntakeHub();
      
      if (!intakeHubData) {
        intakeHubData = []; // Empty by default, override with real BigQuery query
      }

      const transformedProjects = [];

      for (const row of intakeHubData) {
        try {
          const transformed = this.transformRow(row);

          // Validate against schema
          const validation = this.validator.validateProject(transformed, false);

          if (validation.valid) {
            transformedProjects.push(transformed);
            stats.synced++;
          } else {
            stats.failed++;
            stats.errors.push({
              source_id: row.PROJECT_ID || row.Intake_Card,
              errors: validation.errors
            });
          }

          if (validation.warnings && validation.warnings.length > 0) {
            stats.warnings.push(...validation.warnings);
          }
        } catch (error) {
          stats.failed++;
          stats.errors.push({
            source_id: row.PROJECT_ID || row.Intake_Card,
            error: error.message
          });
        }
      }

      // Update storage with transformed projects
      const syncStats = {
        synced: stats.synced,
        failed: stats.failed,
        errors: stats.errors.slice(0, 100), // Keep first 100 errors
        warnings: stats.warnings.slice(0, 50),
        duration_ms: Date.now() - startTime
      };

      this.storage.updateBridgedCache(transformedProjects, syncStats);
      this.lastSyncTime = new Date().toISOString();

      console.log(`[ProjectsSync] Synced ${stats.synced} projects, ${stats.failed} failed`);
      return {
        success: true,
        stats,
        syncedAt: this.lastSyncTime
      };
    } catch (error) {
      console.error('[ProjectsSync] Sync error:', error.message);
      return {
        success: false,
        error: error.message,
        stats
      };
    } finally {
      this.isSyncing = false;
    }
  }

  /**
   * Transform Intake Hub row to Projects Schema format
   * Uses mapping configuration to align columns
   */
  transformRow(row) {
    if (!this.mapping || !this.mapping.columnMappings) {
      // Fallback: assume row already matches schema
      return row;
    }

    const transformed = {
      project_source: 'Intake_Hub'
    };

    // Map each category of columns
    const mappings = this.mapping.columnMappings;

    // Handle identifiers
    if (mappings.identifiers) {
      transformed.project_id = this.applyTransformation(
        row,
        mappings.identifiers.find(m => m.targetColumn === 'project_id')
      );
      
      transformed.intake_card = this.applyTransformation(
        row,
        mappings.identifiers.find(m => m.targetColumn === 'intake_card')
      );
      
      transformed.title = this.applyTransformation(
        row,
        mappings.identifiers.find(m => m.targetColumn === 'title')
      );
    }

    // Handle status fields
    if (mappings.status) {
      transformed.status = this.applyTransformation(
        row,
        mappings.status.find(m => m.targetColumn === 'status')
      );
      
      transformed.phase = this.applyTransformation(
        row,
        mappings.status.find(m => m.targetColumn === 'phase')
      );
      
      transformed.health = this.applyTransformation(
        row,
        mappings.status.find(m => m.targetColumn === 'health')
      );
    }

    // Handle location fields
    if (mappings.location) {
      mappings.location.forEach(mapping => {
        transformed[mapping.targetColumn] = this.applyTransformation(row, mapping);
      });
    }

    // Handle time fields
    if (mappings.time) {
      mappings.time.forEach(mapping => {
        transformed[mapping.targetColumn] = this.applyTransformation(row, mapping);
      });
    }

    // Handle ownership
    if (mappings.ownership) {
      mappings.ownership.forEach(mapping => {
        transformed[mapping.targetColumn] = this.applyTransformation(row, mapping);
      });
    }

    // Handle categorization
    if (mappings.categorization) {
      mappings.categorization.forEach(mapping => {
        transformed[mapping.targetColumn] = this.applyTransformation(row, mapping);
      });
    }

    // Handle impact
    if (mappings.impact) {
      mappings.impact.forEach(mapping => {
        transformed[mapping.targetColumn] = this.applyTransformation(row, mapping);
      });
    }

    // Handle description
    if (mappings.description) {
      mappings.description.forEach(mapping => {
        transformed[mapping.targetColumn] = this.applyTransformation(row, mapping);
      });
    }

    // Add sync metadata
    transformed.synced_at = new Date().toISOString();
    transformed.data_source_id = row.PROJECT_ID || row.Intake_Card;

    return transformed;
  }

  /**
   * Apply transformation to a source field
   * Handles fallbacks and transformation functions
   */
  applyTransformation(row, mapping) {
    if (!mapping) {
      return undefined;
    }

    let value = row[mapping.sourceColumn];

    // Try alternate sources if primary is missing
    if ((value === null || value === undefined || value === '') && mapping.alternateSource) {
      value = row[mapping.alternateSource];
    }

    // Try applying transformation function
    if (mapping.transformation && value !== null && value !== undefined) {
      value = this.runTransformation(mapping.transformation, value, row, mapping);
    }

    return value;
  }

  /**
   * Execute transformation function
   * Built-in transformations for common types
   */
  runTransformation(transformationName, value, row, mapping) {
    switch (transformationName) {
      case 'resolve_project_id':
        // IH-specific: Use PROJECT_ID if available, else Intake_Card, else facility-based
        return row.PROJECT_ID || row.Intake_Card || (row.Facility ? `R-${row.Facility}` : undefined);

      case 'resolve_title':
        // Multiple fallback sources
        return row.PROJECT_TITLE || row.Title || 
               (row.Project_Type && row.Initiative_Type ? `${row.Project_Type} - ${row.Initiative_Type}` : undefined) ||
               'Untitled';

      case 'normalize_status':
        // Map IH status values to canonical status
        const statusMap = {
          'planning': 'Pending',
          'active': 'Active',
          'on hold': 'Pending',
          'completed': 'Complete',
          'cancelled': 'Cancelled'
        };
        return statusMap[value.toLowerCase()] || value;

      case 'normalize_phase':
        // Map IH phase values to canonical phases
        const phaseMap = {
          'poc': 'POC/POT',
          'test': 'Test',
          'pilot': 'Test',
          'scale': 'Mkt Scale',
          'rollout': 'Roll/Deploy',
          'deploy': 'Roll/Deploy',
          'complete': 'Complete'
        };
        return phaseMap[value.toLowerCase()] || value;

      case 'normalize_market_3digit':
        // Ensure market is 3 digits with leading zeros
        const market = String(value || '').padStart(3, '0');
        return /^\d{3}$/.test(market) ? market : value;

      case 'extract_store_list':
        // Parse comma-separated or semicolon-separated facility list
        if (typeof value !== 'string') return [];
        return value.split(/[,;]/).map(s => s.trim()).filter(s => s);

      case 'parse_date':
        // Parse date from various formats
        const date = new Date(value);
        return isNaN(date) ? value : date.toISOString().split('T')[0];

      default:
        return value;
    }
  }

  /**
   * Get sync status
   */
  getSyncStatus() {
    return {
      is_syncing: this.isSyncing,
      last_sync: this.lastSyncTime,
      cache_info: this.storage.getLastSyncInfo()
    };
  }

  /**
   * Force full re-sync (clears cache, re-imports all)
   */
  async fullResync(intakeHubData) {
    console.log('[ProjectsSync] Starting full re-sync...');
    return this.syncFromIntakeHub(intakeHubData);
  }

  /**
   * Incremental sync (only new/updated since last sync)
   * Requires timestamp tracking in Intake Hub
   */
  async incrementalSync(intakeHubData) {
    console.log('[ProjectsSync] Starting incremental sync from', this.lastSyncTime);
    
    // Filter to only records updated since last sync
    if (this.lastSyncTime && intakeHubData) {
      const lastSyncDate = new Date(this.lastSyncTime);
      intakeHubData = intakeHubData.filter(row => {
        const updated = new Date(row.last_updated || row.updated_at || 0);
        return updated >= lastSyncDate;
      });
    }

    return this.syncFromIntakeHub(intakeHubData);
  }
}

module.exports = ProjectsSync;
