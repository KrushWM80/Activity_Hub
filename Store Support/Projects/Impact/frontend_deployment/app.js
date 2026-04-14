// Impact Platform Dashboard - App.js
// API Base URL - Points to backend on same network server
const API_BASE = "http://weus42608431466:8002/api/impact";
const CURRENT_USER_ID = "krush"; // Would come from auth in production
const CURRENT_USER_NAME = "Kendall Rush"; // Would come from auth in production

// Store all projects for reference
let allProjects = [];

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Load initial data
    loadProjects();
    populateBusinessAreaFilter();
    populateOwnerFilter();
});

// ==================== URL ROUTING & NAVIGATION ====================
function setupNavigation() {
    // Click handlers for nav items
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault(); // CRITICAL: Prevent browser default link behavior
            const href = this.getAttribute('href');
            if (href && href !== '#') {
                // Update URL without full page reload
                window.history.pushState({}, '', href);
                
                // Update active state
                document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));
                this.classList.add('active');
                
                // Load appropriate content based on URL
                if (href.includes('/projects')) {
                    loadProjects();
                } else if (href.includes('/for-you')) {
                    loadProjects(); // For now, load projects for all tabs
                } else if (href.includes('/reporting')) {
                    loadProjects(); // For now, load projects for all tabs
                }
            }
        });
    });
}

// ==================== PROJECT LOADING ====================
async function loadProjects() {
    try {
        const businessArea = document.getElementById('filter-business-area').value;
        const health = document.getElementById('filter-health').value;
        const status = document.getElementById('filter-status').value;
        const owner = document.getElementById('filter-owner').value;

        let url = `${API_BASE}/projects`;
        const params = new URLSearchParams();
        
        if (businessArea) params.append('business_area', businessArea);
        if (health) params.append('health_status', health);
        if (status) params.append('status', status);
        if (owner) params.append('owner_id', owner);
        
        if (params.toString()) url += '?' + params.toString();

        const response = await fetch(url);
        const projects = await response.json();
        
        // Store all projects for reference
        allProjects = projects;

        // Load metrics
        const metricsResponse = await fetch(`${API_BASE}/metrics`);
        const metrics = await metricsResponse.json();
        updateMetrics(metrics);

        // Populate filters
        populateBusinessAreaFilter(projects);
        populateOwnerFilter(projects);

        // Display projects
        displayProjects(projects);
    } catch (error) {
        console.error('Error loading projects:', error);
        showError('Failed to load projects');
    }
}

// Update dashboard metrics
function updateMetrics(metrics) {
    document.getElementById('metric-projects').textContent = metrics.active_projects;
    document.getElementById('metric-owners').textContent = metrics.unique_owners;
    document.getElementById('metric-updated').textContent = metrics.projects_updated_this_week;
    document.getElementById('metric-percent').textContent = metrics.percent_updated.toFixed(1) + '%';
}

// ==================== FILTERS ====================
async function populateBusinessAreaFilter(projects = null) {
    try {
        if (!projects) {
            const response = await fetch(`${API_BASE}/projects`);
            projects = await response.json();
        }

        const select = document.getElementById('filter-business-area');
        const areas = [...new Set(projects.map(p => p.business_area))].sort();
        const currentValue = select.value;
        
        while (select.options.length > 1) {
            select.remove(1);
        }
        
        areas.forEach(area => {
            const option = document.createElement('option');
            option.value = area;
            option.textContent = area;
            select.appendChild(option);
        });
        
        if (currentValue && areas.includes(currentValue)) {
            select.value = currentValue;
        }
    } catch (error) {
        console.error('Error populating business area filter:', error);
    }
}

async function populateOwnerFilter(projects = null) {
    try {
        if (!projects) {
            const response = await fetch(`${API_BASE}/projects`);
            projects = await response.json();
        }

        const select = document.getElementById('filter-owner');
        const owners = [...new Map(projects.map(p => [p.owner_id, p.owner_name])).entries()]
            .map(([id, name]) => ({id, name}))
            .sort((a, b) => a.name.localeCompare(b.name));
        
        const currentValue = select.value;
        
        while (select.options.length > 1) {
            select.remove(1);
        }
        
        owners.forEach(owner => {
            const option = document.createElement('option');
            option.value = owner.id;
            option.textContent = owner.name;
            select.appendChild(option);
        });
        
        if (currentValue && owners.some(o => o.id === currentValue)) {
            select.value = currentValue;
        }
    } catch (error) {
        console.error('Error populating owner filter:', error);
    }
}

// ==================== OWNER LOOKUP ====================
async function getAvailableOwners() {
    try {
        const response = await fetch(`${API_BASE}/owners`);
        if (response.ok) {
            return await response.json();
        }
        return [];
    } catch (error) {
        console.error('Error fetching owners:', error);
        return [];
    }
}

async function lookupOwnerName(ownerId) {
    try {
        const owners = await getAvailableOwners();
        const owner = owners.find(o => o.owner_id === ownerId);
        return owner ? owner.owner_name : '';
    } catch (error) {
        console.error('Error looking up owner name:', error);
        return '';
    }
}

async function lookupOwnerId(ownerName) {
    try {
        const owners = await getAvailableOwners();
        const owner = owners.find(o => o.owner_name.toLowerCase() === ownerName.toLowerCase());
        return owner ? owner.owner_id : '';
    } catch (error) {
        console.error('Error looking up owner ID:', error);
        return '';
    }
}

// Auto-fill owner name when owner ID is entered
async function handleOwnerIdChange(inputElement) {
    const ownerId = inputElement.value.trim();
    if (ownerId) {
        const ownerName = await lookupOwnerName(ownerId);
        const ownerNameField = document.getElementById('form-owner-name-field') || 
                              document.getElementById('form-owner-name') || 
                              document.getElementById('edit-owner-name-field') ||
                              document.getElementById('edit-owner-name');
        if (ownerNameField) {
            ownerNameField.value = ownerName || '';
        }
    }
}

// Auto-fill owner ID when owner name is entered
async function handleOwnerNameChange(inputElement) {
    const ownerName = inputElement.value.trim();
    if (ownerName) {
        const ownerId = await lookupOwnerId(ownerName);
        const ownerIdField = document.getElementById('form-owner-id-field') || 
                            document.getElementById('form-owner-id') ||
                            document.getElementById('edit-owner-id-field') ||
                            document.getElementById('edit-owner-id');
        if (ownerIdField) {
            ownerIdField.value = ownerId || '';
        }
    }
}

// ==================== PROJECT DISPLAY ====================
function displayProjects(projects) {
    const table = document.getElementById('projects-table');
    
    if (!projects || projects.length === 0) {
        table.innerHTML = `
            <tr>
                <td colspan="7" class="empty-state">
                    <i class="fas fa-inbox"></i>
                    <p style="margin-top: 10px;">No projects found matching your filters.</p>
                </td>
            </tr>
        `;
        return;
    }

    table.innerHTML = projects.map(project => {
        const isOwner = project.owner_id === CURRENT_USER_ID;
        const showEditBtn = isOwner ? '' : 'style="display:none;"';
        
        return `
            <tr onclick="showProjectDetails('${project.impact_id}')" style="cursor: pointer;">
                <td>
                    <strong style="cursor: pointer; color: #0071CE;" onclick="handleTitleClick(event, '${project.impact_id}', '${project.source}')">
                        ${project.title}
                    </strong>
                    <div style="font-size: 11px; color: #999; margin-top: 3px;">
                        ${project.source === 'Intake Hub' ? '<span style="background: #E3F2FD; color: #1976D2; padding: 2px 6px; border-radius: 3px;">Intake Hub</span>' : '<span style="background: #F3E5F5; color: #8E24AA; padding: 2px 6px; border-radius: 3px;">Projects</span>'}
                    </div>
                </td>
                <td>${project.business_area}</td>
                <td>${project.owner_name}</td>
                <td>
                    ${getHealthBadge(project.health_status)}
                </td>
                <td>
                    <small>${project.latest_update ? project.latest_update.substring(0, 50) : 'N/A'}</small>
                </td>
                <td>
                    ${project.current_wm_week_update ? 
                        '<span class="status-updated"><i class="fas fa-check"></i> Updated</span>' :
                        '<span class="status-not-updated"><i class="fas fa-exclamation-circle"></i> Not Updated</span>'
                    }
                </td>
                <td onclick="event.stopPropagation();">
                    <button class="btn btn-sm btn-primary" ${showEditBtn} onclick="showEditProjectModal('${project.impact_id}')">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

function getHealthBadge(health) {
    const healthLower = (health || '').toLowerCase();
    let className = 'health-green';
    let displayText = health;
    
    if (healthLower === 'green' || healthLower === 'on track') {
        className = 'health-green';
        displayText = 'On Track';
    } else if (healthLower === 'yellow' || healthLower === 'at risk') {
        className = 'health-yellow';
        displayText = 'At Risk';
    } else if (healthLower === 'red' || healthLower === 'off track') {
        className = 'health-red';
        displayText = 'Off Track';
    }
    
    return `<span class="${className}">${displayText}</span>`;
}

// ==================== PROJECT DETAILS POPUP ====================
function showProjectDetails(projectId) {
    const project = allProjects.find(p => p.impact_id === projectId);
    if (!project) return;

    const content = document.getElementById('projectDetailsContent');
    content.innerHTML = `
        <div style="padding: 20px;">
            <div style="margin-bottom: 20px;">
                <h5 style="color: #0071CE; margin-bottom: 5px;">${project.title}</h5>
                <div>
                    ${project.source === 'Intake Hub' ? 
                        '<span style="background: #E3F2FD; color: #1976D2; padding: 4px 8px; border-radius: 4px; font-size: 12px;">Intake Hub</span>' : 
                        '<span style="background: #F3E5F5; color: #8E24AA; padding: 4px 8px; border-radius: 4px; font-size: 12px;">Projects</span>'
                    }
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
                <div>
                    <label style="font-weight: 600; color: #666; font-size: 12px; text-transform: uppercase;">Business Area</label>
                    <p style="margin: 5px 0; font-size: 14px;">${project.business_area}</p>
                </div>
                <div>
                    <label style="font-weight: 600; color: #666; font-size: 12px; text-transform: uppercase;">Health Status</label>
                    <p style="margin: 5px 0; font-size: 14px;">${getHealthBadge(project.health_status)}</p>
                </div>
                <div>
                    <label style="font-weight: 600; color: #666; font-size: 12px; text-transform: uppercase;">Owner</label>
                    <p style="margin: 5px 0; font-size: 14px;">${project.owner_name}</p>
                </div>
                <div>
                    <label style="font-weight: 600; color: #666; font-size: 12px; text-transform: uppercase;">Project Status</label>
                    <p style="margin: 5px 0; font-size: 14px;">${project.project_status}</p>
                </div>
            </div>

            ${project.description ? `
                <div style="margin-bottom: 20px;">
                    <label style="font-weight: 600; color: #666; font-size: 12px; text-transform: uppercase;">Description</label>
                    <p style="margin: 5px 0; font-size: 14px;">${project.description}</p>
                </div>
            ` : ''}

            ${project.latest_update ? `
                <div style="margin-bottom: 20px;">
                    <label style="font-weight: 600; color: #666; font-size: 12px; text-transform: uppercase;">Latest Update</label>
                    <p style="margin: 5px 0; font-size: 14px;">${project.latest_update}</p>
                    ${project.latest_update_timestamp ? `<small style="color: #999;">${new Date(project.latest_update_timestamp).toLocaleDateString()}</small>` : ''}
                </div>
            ` : ''}

            <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
                <small style="color: #999;">
                    Created: ${new Date(project.created_timestamp).toLocaleDateString()} | 
                    ID: ${project.impact_id}
                </small>
            </div>
        </div>
    `;

    const modal = new bootstrap.Modal(document.getElementById('projectDetailsModal'));
    modal.show();
}

// ==================== TITLE CLICK HANDLER ====================
function handleTitleClick(event, projectId, source) {
    event.stopPropagation();
    
    if (source === 'Intake Hub') {
        // Navigate to Intake Hub
        const project = allProjects.find(p => p.impact_id === projectId);
        if (project) {
            window.open(`https://intake-hub.walmart.com/project/${projectId}`, '_blank');
        }
    } else {
        // Show project details popup for Projects-only items
        showProjectDetails(projectId);
    }
}

// ==================== EDIT PROJECT ====================
function showEditProjectModal(projectId) {
    const project = allProjects.find(p => p.impact_id === projectId);
    if (!project) return;

    // Check if user is owner
    if (project.owner_id !== CURRENT_USER_ID) {
        showError('You can only edit projects you own');
        return;
    }

    // Populate form
    document.getElementById('edit-project-id').value = projectId;
    document.getElementById('edit-project-source').value = project.source;
    document.getElementById('edit-title').value = project.title;
    document.getElementById('edit-description').value = project.description || '';
    document.getElementById('edit-latest-note').value = project.latest_update || '';
    document.getElementById('edit-owner-name').value = project.owner_name || '';
    document.getElementById('edit-owner-id').value = project.owner_id || '';
    document.getElementById('edit-business-area').value = project.business_area || '';
    
    // Ensure health status is set correctly
    const healthStatusSelect = document.getElementById('edit-health-status');
    healthStatusSelect.value = project.health_status || '';
    
    // Verify the value was set
    if (healthStatusSelect.value !== project.health_status) {
        console.warn(`Health status '${project.health_status}' not found in select options`);
    }

    // Show info message based on source
    const infoDiv = document.getElementById('editFieldsInfo');
    if (project.source === 'Intake Hub') {
        infoDiv.innerHTML = '<strong>Intake Hub Project:</strong> You can only update the "Latest Note" field. Other fields will be read from Intake Hub. Our note will override if it is newer.';
        infoDiv.style.display = 'block';
        
        // Disable fields for Intake Hub projects
        document.getElementById('edit-title').disabled = true;
        document.getElementById('edit-description').disabled = true;
        document.getElementById('edit-owner-name').disabled = true;
        document.getElementById('edit-owner-id').disabled = true;
        document.getElementById('edit-business-area').disabled = true;
        document.getElementById('edit-health-status').disabled = true;
    } else {
        infoDiv.innerHTML = '<strong>Projects Entry:</strong> You can update all fields. Week Status is auto-generated.';
        infoDiv.style.display = 'block';
        
        // Enable all fields for Projects entries
        document.getElementById('edit-title').disabled = false;
        document.getElementById('edit-description').disabled = false;
        document.getElementById('edit-owner-name').disabled = false;
        document.getElementById('edit-owner-id').disabled = false;
        document.getElementById('edit-business-area').disabled = false;
        document.getElementById('edit-health-status').disabled = false;
    }

    const modal = new bootstrap.Modal(document.getElementById('editProjectModal'));
    modal.show();
}

async function submitEditProjectForm() {
    try {
        const projectId = document.getElementById('edit-project-id').value;
        const source = document.getElementById('edit-project-source').value;
        const latestNote = document.getElementById('edit-latest-note').value;

        let updateData = {
            current_wm_week_update: latestNote
        };

        // For Projects-only entries, allow full updates
        if (source === 'Manual Entry') {
            updateData = {
                title: document.getElementById('edit-title').value,
                description: document.getElementById('edit-description').value,
                health_status: document.getElementById('edit-health-status').value,
                current_wm_week_update: latestNote,
            };
        }

        const response = await fetch(`${API_BASE}/projects/${projectId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updateData)
        });

        if (response.ok) {
            showSuccess('Project updated successfully');
            bootstrap.Modal.getInstance(document.getElementById('editProjectModal')).hide();
            loadProjects();
        } else {
            showError('Failed to update project');
        }
    } catch (error) {
        console.error('Error updating project:', error);
        showError('Error updating project: ' + error.message);
    }
}

// ==================== ADD PROJECT ====================
function showAddProjectModal() {
    document.getElementById('addProjectForm').reset();
    
    // Pre-populate current user's information
    document.getElementById('form-owner-id').value = CURRENT_USER_ID;
    document.getElementById('form-owner-name').value = CURRENT_USER_NAME;
    
    const modal = new bootstrap.Modal(document.getElementById('addProjectModal'));
    modal.show();
}

async function submitProjectForm() {
    const form = document.getElementById('addProjectForm');
    
    // Validate
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    const projectData = {
        title: document.getElementById('form-title').value,
        description: document.getElementById('form-description').value,
        owner_name: document.getElementById('form-owner-name').value,
        owner_id: document.getElementById('form-owner-id').value,
        business_area: document.getElementById('form-business-area').value,
        health_status: document.getElementById('form-health-status').value,
        project_status: 'Active'
    };

    try {
        const response = await fetch(`${API_BASE}/projects`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(projectData)
        });

        if (response.ok) {
            const result = await response.json();
            showSuccess(`Project "${projectData.title}" created successfully`);
            bootstrap.Modal.getInstance(document.getElementById('addProjectModal')).hide();
            loadProjects();
        } else {
            showError('Failed to create project');
        }
    } catch (error) {
        console.error('Error creating project:', error);
        showError('Error creating project');
    }
}

// ==================== PPT GENERATION ====================
async function generatePPT() {
    try {
        showSuccess('Generating PPT report...');
        
        const businessArea = document.getElementById('filter-business-area').value;
        const status = document.getElementById('filter-status').value;

        let url = `${API_BASE}/generate-ppt`;
        const params = new URLSearchParams();
        
        if (businessArea) params.append('business_area', businessArea);
        if (status) params.append('status', status);
        
        if (params.toString()) url += '?' + params.toString();

        const response = await fetch(url, { method: 'POST' });
        
        if (response.ok) {
            const result = await response.json();
            
            if (result.download_url) {
                const link = document.createElement('a');
                link.href = result.download_url;
                link.download = `projects-report-${new Date().toISOString().split('T')[0]}.pptx`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                showSuccess('PPT report generated and downloaded successfully!');
            }
        } else {
            showError('Failed to generate PPT report');
        }
    } catch (error) {
        console.error('Error generating PPT:', error);
        showError('Error generating PPT report: ' + error.message);
    }
}

// ==================== NOTIFICATIONS ====================
function showSuccess(message) {
    const alertHtml = `
        <div class="alert alert-success alert-dismissible fade show" role="alert" style="position: fixed; top: 100px; right: 20px; z-index: 1050; max-width: 500px;">
            <i class="fas fa-check-circle"></i> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    const alertContainer = document.createElement('div');
    alertContainer.innerHTML = alertHtml;
    document.body.appendChild(alertContainer.firstElementChild);
    
    setTimeout(() => {
        document.querySelector('.alert-success')?.remove();
    }, 4000);
}

function showError(message) {
    const alertHtml = `
        <div class="alert alert-danger alert-dismissible fade show" role="alert" style="position: fixed; top: 100px; right: 20px; z-index: 1050; max-width: 500px;">
            <i class="fas fa-exclamation-circle"></i> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    const alertContainer = document.createElement('div');
    alertContainer.innerHTML = alertHtml;
    document.body.appendChild(alertContainer.firstElementChild);
    
    setTimeout(() => {
        document.querySelector('.alert-danger')?.remove();
    }, 5000);
}
