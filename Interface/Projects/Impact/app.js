// Impact Platform Dashboard - App.js
// API Base URL
const API_BASE = "http://localhost:8002/api/impact";

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadProjects();
    populateBusinessAreaFilter();
});

// Load projects from API
async function loadProjects() {
    try {
        const businessArea = document.getElementById('filter-business-area').value;
        const health = document.getElementById('filter-health').value;
        const status = document.getElementById('filter-status').value;

        let url = `${API_BASE}/projects`;
        const params = new URLSearchParams();
        
        if (businessArea) params.append('business_area', businessArea);
        if (health) params.append('health_status', health);
        if (status) params.append('status', status);
        
        if (params.toString()) url += '?' + params.toString();

        const response = await fetch(url);
        const projects = await response.json();

        // Load metrics
        const metricsResponse = await fetch(`${API_BASE}/metrics`);
        const metrics = await metricsResponse.json();
        updateMetrics(metrics);

        // Populate business area filter
        populateBusinessAreaFilter(projects);

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

// Display projects in table
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

    table.innerHTML = projects.map(project => `
        <tr>
            <td><strong>${project.title}</strong></td>
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
            <td>
                <button class="btn btn-sm btn-primary" onclick="editProject('${project.impact_id}')">
                    <i class="fas fa-edit"></i> Edit
                </button>
            </td>
        </tr>
    `).join('');
}

// Get health status badge HTML
function getHealthBadge(health) {
    const healthLower = (health || '').toLowerCase();
    let className = 'health-green';
    
    if (healthLower.includes('yellow') || healthLower.includes('risk')) {
        className = 'health-yellow';
    } else if (healthLower.includes('red')) {
        className = 'health-red';
    }
    
    return `<span class="${className}">${health}</span>`;
}

// Populate business area filter
async function populateBusinessAreaFilter(projects = null) {
    try {
        if (!projects) {
            const response = await fetch(`${API_BASE}/projects`);
            projects = await response.json();
        }

        const select = document.getElementById('filter-business-area');
        const areas = [...new Set(projects.map(p => p.business_area))].sort();
        
        // Keep existing selected value
        const currentValue = select.value;
        
        // Remove existing options except first
        while (select.options.length > 1) {
            select.remove(1);
        }
        
        // Add area options
        areas.forEach(area => {
            const option = document.createElement('option');
            option.value = area;
            option.textContent = area;
            select.appendChild(option);
        });
        
        // Restore selected value
        if (currentValue && areas.includes(currentValue)) {
            select.value = currentValue;
        }
    } catch (error) {
        console.error('Error populating business area filter:', error);
    }
}

// Show add project modal
function showAddProjectModal() {
    const modal = new bootstrap.Modal(document.getElementById('addProjectModal'));
    document.getElementById('addProjectForm').reset();
    modal.show();
}

// Submit new project form
async function submitProjectForm() {
    const form = document.getElementById('addProjectForm');
    
    // Get values
    const projectData = {
        title: document.getElementById('form-title').value,
        description: document.getElementById('form-description').value,
        owner_name: document.getElementById('form-owner-name').value,
        owner_id: document.getElementById('form-owner-id').value,
        business_area: document.getElementById('form-business-area').value,
        health_status: document.getElementById('form-health-status').value,
        project_status: 'Active'
    };

    // Validate
    if (!projectData.title || !projectData.owner_name || !projectData.owner_id) {
        alert('Please fill in all required fields');
        return;
    }

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

// Edit project
async function editProject(projectId) {
    // For now, show a simple update modal
    // In production, this would load project details and allow editing
    alert(`Edit functionality for project ${projectId} - (Coming soon)`);
}

// Generate PPT report
async function generatePPT() {
    try {
        const businessArea = document.getElementById('filter-business-area').value;
        const status = document.getElementById('filter-status').value;

        let url = `${API_BASE}/generate-ppt`;
        const params = new URLSearchParams();
        
        if (businessArea) params.append('business_area', businessArea);
        if (status) params.append('status', status);
        
        if (params.toString()) url += '?' + params.toString();

        const response = await fetch(url, { method: 'POST' });
        const result = await response.json();

        if (result.download_url) {
            // Trigger download
            const downloadUrl = result.download_url;
            window.location.href = downloadUrl;
            showSuccess('PPT report generated and downloaded');
        }
    } catch (error) {
        console.error('Error generating PPT:', error);
        showError('Failed to generate PPT report');
    }
}

// Show success message
function showSuccess(message) {
    const alertHtml = `
        <div class="alert alert-success alert-dismissible fade show" role="alert" style="position: fixed; top: 20px; right: 20px; z-index: 1000; max-width: 500px;">
            <i class="fas fa-check-circle"></i> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    const alertContainer = document.createElement('div');
    alertContainer.innerHTML = alertHtml;
    document.body.appendChild(alertContainer.firstElementChild);
    
    setTimeout(() => {
        document.querySelector('.alert-success')?.remove();
    }, 3000);
}

// Show error message
function showError(message) {
    const alertHtml = `
        <div class="alert alert-danger alert-dismissible fade show" role="alert" style="position: fixed; top: 20px; right: 20px; z-index: 1000; max-width: 500px;">
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

// Add "My Projects" tab functionality (future enhancement)
function switchTab(tabName) {
    console.log(`Switching to tab: ${tabName}`);
    loadProjects();
}
