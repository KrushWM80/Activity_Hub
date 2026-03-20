/**
 * Projects Storage Management - File-based JSON Storage Layer
 * 
 * Manages persistent storage for:
 * - Native projects (created directly in Activity Hub)
 * - Project followers relationships (user follows)
 * - Project partner groups (organizational partnerships)
 * - Project metadata (sync status, cache info)
 * 
 * Storage Structure:
 * storage/
 *   projects/
 *     native/
 *       projects.json              # Array of native projects
 *       metadata.json              # Native project metadata (created_dates, etc)
 *     bridged/
 *       intake-hub-cache.json     # Cached bridged projects from Intake Hub
 *       last-sync.json            # Last sync timestamp and stats
 *   relationships/
 *     followers.json              # project_id -> [user_ids]
 *     partner_groups.json         # project_id -> {group_name, [followers]}
 */

const fs = require('fs');
const path = require('path');

class ProjectsStorage {
  constructor(storageBaseDir = './storage') {
    this.baseDir = storageBaseDir;
    this.projectsDir = path.join(this.baseDir, 'projects');
    this.relationshipsDir = path.join(this.baseDir, 'relationships');
    this.nativeDir = path.join(this.projectsDir, 'native');
    this.bridgedDir = path.join(this.projectsDir, 'bridged');
    
    this.initializeDirectories();
  }

  /**
   * Initialize storage directories if they don't exist
   */
  initializeDirectories() {
    const dirs = [
      this.baseDir,
      this.projectsDir,
      this.relationshipsDir,
      this.nativeDir,
      this.bridgedDir
    ];

    dirs.forEach(dir => {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
    });

    // Initialize empty JSON files if they don't exist
    this.ensureFileExists(path.join(this.nativeDir, 'projects.json'), []);
    this.ensureFileExists(path.join(this.nativeDir, 'metadata.json'), {});
    this.ensureFileExists(path.join(this.bridgedDir, 'intake-hub-cache.json'), []);
    this.ensureFileExists(path.join(this.bridgedDir, 'last-sync.json'), { timestamp: null, count: 0, errors: [] });
    this.ensureFileExists(path.join(this.relationshipsDir, 'followers.json'), {});
    this.ensureFileExists(path.join(this.relationshipsDir, 'partner_groups.json'), {});
  }

  /**
   * Ensure a file exists with default content
   */
  ensureFileExists(filePath, defaultContent) {
    if (!fs.existsSync(filePath)) {
      fs.writeFileSync(filePath, JSON.stringify(defaultContent, null, 2));
    }
  }

  /**
   * Read JSON file safely
   */
  readJSON(filePath) {
    try {
      if (!fs.existsSync(filePath)) {
        return null;
      }
      const content = fs.readFileSync(filePath, 'utf8');
      return JSON.parse(content);
    } catch (error) {
      console.error(`Error reading ${filePath}:`, error.message);
      return null;
    }
  }

  /**
   * Write JSON file safely
   */
  writeJSON(filePath, data) {
    try {
      const dir = path.dirname(filePath);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
      return true;
    } catch (error) {
      console.error(`Error writing ${filePath}:`, error.message);
      return false;
    }
  }

  // ==================== NATIVE PROJECTS ====================

  /**
   * Get all native projects
   */
  getNativeProjects() {
    return this.readJSON(path.join(this.nativeDir, 'projects.json')) || [];
  }

  /**
   * Get native project by ID
   */
  getNativeProject(projectId) {
    const projects = this.getNativeProjects();
    return projects.find(p => p.project_id === projectId);
  }

  /**
   * Create new native project
   */
  createNativeProject(projectData) {
    const projects = this.getNativeProjects();
    const newProject = {
      ...projectData,
      project_source: 'Manual_Upload',
      created_date: new Date().toISOString(),
      last_updated: new Date().toISOString(),
      _internal_id: `native_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    };
    
    projects.push(newProject);
    this.writeJSON(path.join(this.nativeDir, 'projects.json'), projects);
    
    // Update metadata
    const metadata = this.readJSON(path.join(this.nativeDir, 'metadata.json')) || {};
    metadata[newProject.project_id] = {
      created_date: newProject.created_date,
      created_by: projectData.created_by || 'system',
      is_native: true
    };
    this.writeJSON(path.join(this.nativeDir, 'metadata.json'), metadata);
    
    return newProject;
  }

  /**
   * Update native project
   */
  updateNativeProject(projectId, updates) {
    const projects = this.getNativeProjects();
    const index = projects.findIndex(p => p.project_id === projectId);
    
    if (index === -1) {
      throw new Error(`Native project ${projectId} not found`);
    }

    projects[index] = {
      ...projects[index],
      ...updates,
      last_updated: new Date().toISOString()
    };
    
    this.writeJSON(path.join(this.nativeDir, 'projects.json'), projects);
    return projects[index];
  }

  /**
   * Delete native project
   */
  deleteNativeProject(projectId) {
    const projects = this.getNativeProjects();
    const filtered = projects.filter(p => p.project_id !== projectId);
    
    if (filtered.length === projects.length) {
      throw new Error(`Native project ${projectId} not found`);
    }

    this.writeJSON(path.join(this.nativeDir, 'projects.json'), filtered);
    
    // Remove from metadata
    const metadata = this.readJSON(path.join(this.nativeDir, 'metadata.json')) || {};
    delete metadata[projectId];
    this.writeJSON(path.join(this.nativeDir, 'metadata.json'), metadata);
    
    // Remove relationships
    this.removeAllRelationships(projectId);
    
    return true;
  }

  // ==================== BRIDGED PROJECTS (INTAKE HUB) ====================

  /**
   * Get all bridged projects (cached from Intake Hub)
   */
  getBridgedProjects() {
    return this.readJSON(path.join(this.bridgedDir, 'intake-hub-cache.json')) || [];
  }

  /**
   * Get bridged project by ID
   */
  getBridgedProject(projectId) {
    const projects = this.getBridgedProjects();
    return projects.find(p => p.project_id === projectId);
  }

  /**
   * Update bridged projects cache (called by sync service)
   */
  updateBridgedCache(projects, syncStats = {}) {
    this.writeJSON(path.join(this.bridgedDir, 'intake-hub-cache.json'), projects);
    
    const syncInfo = {
      timestamp: new Date().toISOString(),
      count: projects.length,
      errors: syncStats.errors || [],
      duration_ms: syncStats.duration_ms || 0,
      ...syncStats
    };
    
    this.writeJSON(path.join(this.bridgedDir, 'last-sync.json'), syncInfo);
    return syncInfo;
  }

  /**
   * Get last sync info
   */
  getLastSyncInfo() {
    return this.readJSON(path.join(this.bridgedDir, 'last-sync.json')) || {
      timestamp: null,
      count: 0,
      errors: []
    };
  }

  // ==================== COMBINED VIEW ====================

  /**
   * Get all projects (native + bridged)
   * Filters based on user access and roles
   */
  getAllProjects(filterOptions = {}) {
    const native = this.getNativeProjects();
    const bridged = this.getBridgedProjects();
    
    let allProjects = [
      ...native,
      ...bridged
    ];

    // Apply filters if provided
    if (filterOptions.status) {
      allProjects = allProjects.filter(p => p.status === filterOptions.status);
    }
    
    if (filterOptions.phase) {
      allProjects = allProjects.filter(p => p.phase === filterOptions.phase);
    }
    
    if (filterOptions.owner) {
      allProjects = allProjects.filter(p => p.owner === filterOptions.owner);
    }

    if (filterOptions.search) {
      const searchLower = filterOptions.search.toLowerCase();
      allProjects = allProjects.filter(p => 
        (p.project_id && p.project_id.toLowerCase().includes(searchLower)) ||
        (p.title && p.title.toLowerCase().includes(searchLower))
      );
    }

    return allProjects;
  }

  /**
   * Get any project by ID (searches both native and bridged)
   */
  getProject(projectId) {
    return this.getNativeProject(projectId) || this.getBridgedProject(projectId);
  }

  // ==================== FOLLOWERS RELATIONSHIPS ====================

  /**
   * Get all followers for a project
   */
  getProjectFollowers(projectId) {
    const followers = this.readJSON(path.join(this.relationshipsDir, 'followers.json')) || {};
    return followers[projectId] || [];
  }

  /**
   * Add follower to project
   */
  addFollower(projectId, userId) {
    const followers = this.readJSON(path.join(this.relationshipsDir, 'followers.json')) || {};
    
    if (!followers[projectId]) {
      followers[projectId] = [];
    }

    if (!followers[projectId].includes(userId)) {
      followers[projectId].push(userId);
    }

    this.writeJSON(path.join(this.relationshipsDir, 'followers.json'), followers);
    return followers[projectId];
  }

  /**
   * Remove follower from project
   */
  removeFollower(projectId, userId) {
    const followers = this.readJSON(path.join(this.relationshipsDir, 'followers.json')) || {};
    
    if (followers[projectId]) {
      followers[projectId] = followers[projectId].filter(uid => uid !== userId);
    }

    this.writeJSON(path.join(this.relationshipsDir, 'followers.json'), followers);
    return followers[projectId] || [];
  }

  /**
   * Check if user follows project
   */
  isFollowing(projectId, userId) {
    return this.getProjectFollowers(projectId).includes(userId);
  }

  // ==================== PARTNER GROUPS ====================

  /**
   * Get partner groups for a project
   */
  getProjectPartners(projectId) {
    const partners = this.readJSON(path.join(this.relationshipsDir, 'partner_groups.json')) || {};
    return partners[projectId] || [];
  }

  /**
   * Add partner group to project
   */
  addPartner(projectId, groupName, groupFollowers = []) {
    const partners = this.readJSON(path.join(this.relationshipsDir, 'partner_groups.json')) || {};
    
    if (!partners[projectId]) {
      partners[projectId] = [];
    }

    // Check if group already exists
    const existing = partners[projectId].find(g => g.group_name === groupName);
    
    if (!existing) {
      partners[projectId].push({
        group_name: groupName,
        followers: groupFollowers,
        added_date: new Date().toISOString()
      });
    } else {
      // Update followers if provided
      if (groupFollowers.length > 0) {
        existing.followers = groupFollowers;
      }
    }

    this.writeJSON(path.join(this.relationshipsDir, 'partner_groups.json'), partners);
    return partners[projectId];
  }

  /**
   * Remove partner group from project
   */
  removePartner(projectId, groupName) {
    const partners = this.readJSON(path.join(this.relationshipsDir, 'partner_groups.json')) || {};
    
    if (partners[projectId]) {
      partners[projectId] = partners[projectId].filter(g => g.group_name !== groupName);
    }

    this.writeJSON(path.join(this.relationshipsDir, 'partner_groups.json'), partners);
    return partners[projectId] || [];
  }

  // ==================== UTILITY ====================

  /**
   * Remove all relationships for a project (when deleting)
   */
  removeAllRelationships(projectId) {
    const followers = this.readJSON(path.join(this.relationshipsDir, 'followers.json')) || {};
    delete followers[projectId];
    this.writeJSON(path.join(this.relationshipsDir, 'followers.json'), followers);

    const partners = this.readJSON(path.join(this.relationshipsDir, 'partner_groups.json')) || {};
    delete partners[projectId];
    this.writeJSON(path.join(this.relationshipsDir, 'partner_groups.json'), partners);
  }

  /**
   * Get storage statistics
   */
  getStorageStats() {
    return {
      native_projects: this.getNativeProjects().length,
      bridged_projects: this.getBridgedProjects().length,
      total_followers: Object.values(this.readJSON(path.join(this.relationshipsDir, 'followers.json')) || {}).reduce((sum, arr) => sum + arr.length, 0),
      last_sync: this.getLastSyncInfo()
    };
  }
}

module.exports = ProjectsStorage;
