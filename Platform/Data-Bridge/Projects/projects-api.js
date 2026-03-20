/**
 * Projects API Service - REST Endpoints for Frontend
 * 
 * Port: 8001 (Projects Service)
 * Base URL: http://localhost:8001/api/projects/
 * 
 * Endpoints:
 * GET    /api/projects                - List projects (with filters, pagination)
 * GET    /api/projects/{id}           - Get project details
 * POST   /api/projects                - Create new native project
 * PUT    /api/projects/{id}           - Update project
 * DELETE /api/projects/{id}           - Delete project
 * POST   /api/projects/{id}/follow    - User follows project
 * DELETE /api/projects/{id}/follow    - User unfollows project
 * GET    /api/projects/{id}/followers - Get project followers
 * GET    /api/projects/{id}/metrics   - Get metrics for project
 * GET    /api/templates/{type}        - Get template definition
 * POST   /api/templates/{type}/render - Render template with project data
 * GET    /api/sync/status             - Get sync status
 * POST   /api/sync/trigger            - Trigger sync from Intake Hub
 */

const express = require('express');
const router = express.Router();

/**
 * Initialize API Router with service dependencies
 */
function initializeProjectsAPI(storage, validator, sync, metricsService = null) {
  
  // ==================== PROJECT LISTING & RETRIEVAL ====================

  /**
   * GET /api/projects
   * List all projects with filters and pagination
   * Query params: status, phase, owner, search, limit, offset, data_source
   */
  router.get('/projects', (req, res) => {
    try {
      const {
        status,
        phase,
        owner,
        search,
        limit = 50,
        offset = 0,
        data_source,
        sort_by = 'created_date',
        sort_dir = 'desc'
      } = req.query;

      // Build filter options
      const filterOptions = {};
      if (status) filterOptions.status = status;
      if (phase) filterOptions.phase = phase;
      if (owner) filterOptions.owner = owner;
      if (search) filterOptions.search = search;

      let projects = storage.getAllProjects(filterOptions);

      // Filter by data source if specified
      if (data_source) {
        projects = projects.filter(p => p.project_source === data_source);
      }

      // Sort
      projects.sort((a, b) => {
        const aVal = a[sort_by] || '';
        const bVal = b[sort_by] || '';
        const comparison = aVal < bVal ? -1 : aVal > bVal ? 1 : 0;
        return sort_dir === 'asc' ? comparison : -comparison;
      });

      // Paginate
      const total = projects.length;
      projects = projects.slice(offset, offset + parseInt(limit));

      res.json({
        success: true,
        data: projects,
        pagination: {
          total,
          limit: parseInt(limit),
          offset: parseInt(offset),
          pages: Math.ceil(total / parseInt(limit))
        }
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        error: error.message
      });
    }
  });

  /**
   * GET /api/projects/{id}
   * Get single project details with followers and partner groups
   */
  router.get('/projects/:id', (req, res) => {
    try {
      const { id } = req.params;
      const project = storage.getProject(id);

      if (!project) {
        return res.status(404).json({
          success: false,
          error: `Project ${id} not found`
        });
      }

      // Enrich with relationships
      const enriched = {
        ...project,
        followers: storage.getProjectFollowers(id),
        partner_groups: storage.getProjectPartners(id),
        follower_count: storage.getProjectFollowers(id).length
      };

      // Fetch metrics if service available
      if (metricsService) {
        enriched.metrics = metricsService.getProjectMetrics(id);
      }

      res.json({
        success: true,
        data: enriched
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        error: error.message
      });
    }
  });

  // ==================== PROJECT CREATION & MODIFICATION ====================

  /**
   * POST /api/projects
   * Create new native project
   * Body: Project data matching schema
   */
  router.post('/projects', express.json(), (req, res) => {
    try {
      const projectData = req.body;

      // Validate
      const validation = validator.validateProject(projectData, true);
      if (!validation.valid) {
        return res.status(400).json({
          success: false,
          errors: validation.errors,
          warnings: validation.warnings
        });
      }

      // Create
      const newProject = storage.createNativeProject(projectData);

      res.status(201).json({
        success: true,
        data: newProject,
        message: 'Project created successfully'
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        error: error.message
      });
    }
  });

  /**
   * PUT /api/projects/{id}
   * Update existing project
   * Body: Fields to update
   */
  router.put('/projects/:id', express.json(), (req, res) => {
    try {
      const { id } = req.params;
      const updates = req.body;

      const existing = storage.getProject(id);
      if (!existing) {
        return res.status(404).json({
          success: false,
          error: `Project ${id} not found`
        });
      }

      // Check if native (can only update native projects directly)
      if (existing.project_source !== 'Manual_Upload') {
        return res.status(403).json({
          success: false,
          error: 'Can only update native projects. Bridged projects update via Data-Bridge sync.'
        });
      }

      // Validate merged data
      const merged = { ...existing, ...updates };
      const validation = validator.validateProject(merged, false);
      if (!validation.valid) {
        return res.status(400).json({
          success: false,
          errors: validation.errors
        });
      }

      // Update
      const updated = storage.updateNativeProject(id, updates);

      res.json({
        success: true,
        data: updated,
        message: 'Project updated successfully'
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        error: error.message
      });
    }
  });

  /**
   * DELETE /api/projects/{id}
   * Delete native project
   */
  router.delete('/projects/:id', (req, res) => {
    try {
      const { id } = req.params;

      const existing = storage.getProject(id);
      if (!existing) {
        return res.status(404).json({
          success: false,
          error: `Project ${id} not found`
        });
      }

      // Check if native
      if (existing.project_source !== 'Manual_Upload') {
        return res.status(403).json({
          success: false,
          error: 'Can only delete native projects'
        });
      }

      storage.deleteNativeProject(id);

      res.json({
        success: true,
        message: `Project ${id} deleted successfully`
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        error: error.message
      });
    }
  });

  // ==================== FOLLOWERS & RELATIONSHIPS ====================

  /**
   * POST /api/projects/{id}/follow
   * User follows a project
   * Body: { user_id: string }
   */
  router.post('/projects/:id/follow', express.json(), (req, res) => {
    try {
      const { id } = req.params;
      const { user_id } = req.body;

      if (!user_id) {
        return res.status(400).json({
          success: false,
          error: 'user_id is required'
        });
      }

      const project = storage.getProject(id);
      if (!project) {
        return res.status(404).json({
          success: false,
          error: `Project ${id} not found`
        });
      }

      const followers = storage.addFollower(id, user_id);

      res.json({
        success: true,
        data: { followers },
        message: `${user_id} now follows project ${id}`
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        error: error.message
      });
    }
  });

  /**
   * DELETE /api/projects/{id}/follow
   * User unfollows a project
   * Query: user_id
   */
  router.delete('/projects/:id/follow', (req, res) => {
    try {
      const { id } = req.params;
      const { user_id } = req.query;

      if (!user_id) {
        return res.status(400).json({
          success: false,
          error: 'user_id is required'
        });
      }

      const project = storage.getProject(id);
      if (!project) {
        return res.status(404).json({
          success: false,
          error: `Project ${id} not found`
        });
      }

      const followers = storage.removeFollower(id, user_id);

      res.json({
        success: true,
        data: { followers },
        message: `${user_id} unfollows project ${id}`
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        error: error.message
      });
    }
  });

  /**
   * GET /api/projects/{id}/followers
   * Get all followers and partner groups for project
   */
  router.get('/projects/:id/followers', (req, res) => {
    try {
      const { id } = req.params;

      const project = storage.getProject(id);
      if (!project) {
        return res.status(404).json({
          success: false,
          error: `Project ${id} not found`
        });
      }

      res.json({
        success: true,
        data: {
          followers: storage.getProjectFollowers(id),
          partner_groups: storage.getProjectPartners(id),
          owner: project.owner,
          director: project.director
        }
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        error: error.message
      });
    }
  });

  // ==================== METRICS ====================

  /**
   * GET /api/projects/{id}/metrics
   * Get metrics for project (from Project_Metric_Lift table)
   */
  router.get('/projects/:id/metrics', (req, res) => {
    try {
      const { id } = req.params;

      const project = storage.getProject(id);
      if (!project) {
        return res.status(404).json({
          success: false,
          error: `Project ${id} not found`
        });
      }

      // TODO: Real implementation queries Project_Metric_Lift BigQuery table
      // For now, return mock metrics
      const metrics = {
        testing_completion: 75,
        validation_completion: 60,
        stores_involved: 45,
        stores_completed: 32,
        health: project.health || 'Unknown'
      };

      res.json({
        success: true,
        data: metrics
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        error: error.message
      });
    }
  });

  // ==================== TEMPLATES ====================

  /**
   * GET /api/templates/{type}
   * Get template definition by type
   * Types: sif-aim, meeting, forum, status-report, etc
   */
  router.get('/templates/:type', (req, res) => {
    try {
      const { type } = req.params;

      // TODO: Load from templates storage
      // For now, return mock template
      const templates = {
        'sif-aim': {
          name: 'SIF/AIM Meeting',
          type: 'meeting',
          sections: [
            {
              id: 'problem_statement',
              title: 'Problem Statement',
              fields: ['title', 'description', 'owner', 'customer_impact']
            },
            {
              id: 'proposed_solution',
              title: 'Proposed Solution',
              fields: ['solution_description', 'projected_completion']
            }
          ]
        }
      };

      const template = templates[type];
      if (!template) {
        return res.status(404).json({
          success: false,
          error: `Template ${type} not found`
        });
      }

      res.json({
        success: true,
        data: template
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        error: error.message
      });
    }
  });

  /**
   * POST /api/templates/{type}/render
   * Render template with project data
   * Body: { project_id: string }
   */
  router.post('/templates/:type/render', express.json(), (req, res) => {
    try {
      const { type } = req.params;
      const { project_id } = req.body;

      if (!project_id) {
        return res.status(400).json({
          success: false,
          error: 'project_id is required'
        });
      }

      const project = storage.getProject(project_id);
      if (!project) {
        return res.status(404).json({
          success: false,
          error: `Project ${project_id} not found`
        });
      }

      // TODO: Render template with project data
      const rendered = {
        template_type: type,
        project_id,
        html: '<div>Rendered template would go here</div>',
        data_populated: true
      };

      res.json({
        success: true,
        data: rendered
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        error: error.message
      });
    }
  });

  // ==================== SYNC MANAGEMENT ====================

  /**
   * GET /api/sync/status
   * Get current sync status
   */
  router.get('/sync/status', (req, res) => {
    try {
      res.json({
        success: true,
        data: {
          sync_status: sync.getSyncStatus(),
          storage_stats: storage.getStorageStats()
        }
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        error: error.message
      });
    }
  });

  /**
   * POST /api/sync/trigger
   * Trigger sync from Intake Hub
   * Query: mode = 'full' | 'incremental'
   */
  router.post('/sync/trigger', express.json(), async (req, res) => {
    try {
      const { mode = 'incremental' } = req.query;

      // TODO: In production, fetch real data from Intake Hub BigQuery
      const intakeHubData = req.body.data || [];

      const result = mode === 'full'
        ? await sync.fullResync(intakeHubData)
        : await sync.incrementalSync(intakeHubData);

      res.json({
        success: result.success,
        data: result,
        message: result.success ? 'Sync completed' : 'Sync failed'
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        error: error.message
      });
    }
  });

  return router;
}

module.exports = { initializeProjectsAPI };
