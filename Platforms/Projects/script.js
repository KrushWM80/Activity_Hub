// IH Project Data Management Interface JavaScript
class IHProjectDataManager {
    constructor() {
        this.records = this.loadRecords();
        this.currentEditingRecord = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadAllRecords();
        
        // Load sample data if no records exist
        if (this.records.length === 0) {
            this.loadSampleData();
        }
    }

    bindEvents() {
        // Form submissions
        document.getElementById('createForm').addEventListener('submit', (e) => this.handleCreateRecord(e));
        document.getElementById('updateForm').addEventListener('submit', (e) => this.handleUpdateRecord(e));

        // Modal events
        window.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                this.closeUpdateModal();
            }
        });

        // Tab navigation
        document.querySelectorAll('.tab-button').forEach(button => {
            button.addEventListener('click', (e) => {
                const tabName = e.target.getAttribute('onclick').match(/'([^']+)'/)[1];
                this.showTab(tabName);
            });
        });

        // Search functionality
        document.getElementById('searchProjectId').addEventListener('input', this.debounce(() => this.searchRecords(), 300));
        document.getElementById('searchProjectName').addEventListener('input', this.debounce(() => this.searchRecords(), 300));
        document.getElementById('searchStoreNumber').addEventListener('input', this.debounce(() => this.searchRecords(), 300));
        document.getElementById('searchStatus').addEventListener('change', () => this.searchRecords());
    }

    // Local Storage Management
    loadRecords() {
        const stored = localStorage.getItem('ihProjectData');
        return stored ? JSON.parse(stored) : [];
    }

    saveRecords() {
        localStorage.setItem('ihProjectData', JSON.stringify(this.records));
    }

    // Sample Data for Demo
    loadSampleData() {
        const sampleData = [
            {
                id: this.generateId(),
                projectId: 'IH-2024-001',
                projectName: 'Store Security Assessment',
                storeNumber: 1234,
                region: 'North',
                district: 'District A',
                market: 'Metro',
                projectType: 'Investigation',
                priority: 'High',
                status: 'In Progress',
                assignedTo: 'John Smith',
                startDate: '2024-10-01',
                targetDate: '2024-11-15',
                description: 'Comprehensive security assessment of high-risk store location',
                notes: 'Focus on perimeter security and internal controls',
                createdDate: new Date().toISOString(),
                lastModified: new Date().toISOString()
            },
            {
                id: this.generateId(),
                projectId: 'IH-2024-002',
                projectName: 'Loss Prevention Training Program',
                storeNumber: 5678,
                region: 'South',
                district: 'District B',
                market: 'Suburban',
                projectType: 'Training',
                priority: 'Medium',
                status: 'Planning',
                assignedTo: 'Sarah Johnson',
                startDate: '2024-11-01',
                targetDate: '2024-12-01',
                description: 'Implement comprehensive loss prevention training for store associates',
                notes: 'Coordinate with HR for scheduling',
                createdDate: new Date().toISOString(),
                lastModified: new Date().toISOString()
            },
            {
                id: this.generateId(),
                projectId: 'IH-2024-003',
                projectName: 'Compliance Audit Review',
                storeNumber: 9101,
                region: 'West',
                district: 'District C',
                market: 'Urban',
                projectType: 'Audit',
                priority: 'Critical',
                status: 'Completed',
                assignedTo: 'Mike Davis',
                startDate: '2024-09-15',
                targetDate: '2024-10-15',
                description: 'Annual compliance audit and documentation review',
                notes: 'All requirements met, report submitted',
                createdDate: new Date().toISOString(),
                lastModified: new Date().toISOString()
            }
        ];
        
        this.records = sampleData;
        this.saveRecords();
        this.showStatusMessage('Sample data loaded successfully!', 'success');
    }

    // Utility Functions
    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    formatDate(dateString) {
        if (!dateString) return 'N/A';
        return new Date(dateString).toLocaleDateString();
    }

    // Tab Management
    showTab(tabName) {
        // Hide all tabs
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelectorAll('.tab-button').forEach(button => {
            button.classList.remove('active');
        });

        // Show selected tab
        document.getElementById(tabName).classList.add('active');
        document.querySelector(`[onclick="showTab('${tabName}')"]`).classList.add('active');

        // Load data based on tab
        if (tabName === 'view') {
            this.loadAllRecords();
        } else if (tabName === 'search') {
            this.searchRecords();
        }
    }

    // Record Creation
    handleCreateRecord(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const recordData = {};
        
        // Convert form data to object
        for (let [key, value] of formData.entries()) {
            recordData[key] = value;
        }

        // Validation
        if (!this.validateRecord(recordData)) {
            return;
        }

        // Check for duplicate Project ID
        if (this.records.some(record => record.projectId === recordData.projectId)) {
            this.showStatusMessage('Project ID already exists. Please use a unique Project ID.', 'error');
            return;
        }

        // Add metadata
        recordData.id = this.generateId();
        recordData.createdDate = new Date().toISOString();
        recordData.lastModified = new Date().toISOString();

        // Save record
        this.records.push(recordData);
        this.saveRecords();

        // Reset form and show success message
        e.target.reset();
        this.showStatusMessage('Record created successfully!', 'success');

        // Refresh view if on view tab
        if (document.getElementById('view').classList.contains('active')) {
            this.loadAllRecords();
        }
    }

    // Record Validation
    validateRecord(data) {
        const errors = [];

        if (!data.projectId || data.projectId.trim().length < 3) {
            errors.push('Project ID must be at least 3 characters long');
        }

        if (!data.projectName || data.projectName.trim().length < 5) {
            errors.push('Project Name must be at least 5 characters long');
        }

        if (data.storeNumber && (isNaN(data.storeNumber) || data.storeNumber < 1)) {
            errors.push('Store Number must be a positive number');
        }

        if (data.startDate && data.targetDate && new Date(data.startDate) > new Date(data.targetDate)) {
            errors.push('Target Date must be after Start Date');
        }

        if (errors.length > 0) {
            this.showStatusMessage('Validation errors: ' + errors.join(', '), 'error');
            return false;
        }

        return true;
    }

    // Search Functionality
    searchRecords() {
        const searchProjectId = document.getElementById('searchProjectId').value.toLowerCase();
        const searchProjectName = document.getElementById('searchProjectName').value.toLowerCase();
        const searchStoreNumber = document.getElementById('searchStoreNumber').value;
        const searchStatus = document.getElementById('searchStatus').value;

        let filteredRecords = this.records.filter(record => {
            const matchesProjectId = !searchProjectId || record.projectId.toLowerCase().includes(searchProjectId);
            const matchesProjectName = !searchProjectName || record.projectName.toLowerCase().includes(searchProjectName);
            const matchesStoreNumber = !searchStoreNumber || record.storeNumber.toString().includes(searchStoreNumber);
            const matchesStatus = !searchStatus || record.status === searchStatus;

            return matchesProjectId && matchesProjectName && matchesStoreNumber && matchesStatus;
        });

        this.displaySearchResults(filteredRecords);
    }

    displaySearchResults(records) {
        const container = document.getElementById('searchResults');
        
        if (records.length === 0) {
            container.innerHTML = '<div class="result-item"><p>No records found matching your search criteria.</p></div>';
            return;
        }

        container.innerHTML = records.map(record => `
            <div class="result-item">
                <div class="result-header">
                    <div class="result-title">${record.projectId} - ${record.projectName}</div>
                    <div class="result-actions">
                        <button class="btn btn-primary" onclick="ihManager.editRecord('${record.id}')">Edit</button>
                        <button class="btn btn-danger" onclick="ihManager.deleteRecord('${record.id}')">Delete</button>
                    </div>
                </div>
                <div class="result-details">
                    <div class="result-field">
                        <strong>Store Number:</strong>
                        <span>${record.storeNumber || 'N/A'}</span>
                    </div>
                    <div class="result-field">
                        <strong>Region:</strong>
                        <span>${record.region || 'N/A'}</span>
                    </div>
                    <div class="result-field">
                        <strong>Status:</strong>
                        <span class="status-badge status-${record.status.toLowerCase().replace(' ', '-')}">${record.status}</span>
                    </div>
                    <div class="result-field">
                        <strong>Priority:</strong>
                        <span class="status-badge priority-${record.priority.toLowerCase()}">${record.priority}</span>
                    </div>
                    <div class="result-field">
                        <strong>Assigned To:</strong>
                        <span>${record.assignedTo || 'Unassigned'}</span>
                    </div>
                    <div class="result-field">
                        <strong>Target Date:</strong>
                        <span>${this.formatDate(record.targetDate)}</span>
                    </div>
                </div>
                ${record.description ? `
                    <div class="result-field full-width" style="margin-top: 15px;">
                        <strong>Description:</strong>
                        <span>${record.description}</span>
                    </div>
                ` : ''}
            </div>
        `).join('');
    }

    clearSearch() {
        document.getElementById('searchProjectId').value = '';
        document.getElementById('searchProjectName').value = '';
        document.getElementById('searchStoreNumber').value = '';
        document.getElementById('searchStatus').value = '';
        this.searchRecords();
    }

    // Record Editing
    editRecord(recordId) {
        const record = this.records.find(r => r.id === recordId);
        if (!record) {
            this.showStatusMessage('Record not found', 'error');
            return;
        }

        this.currentEditingRecord = record;
        this.populateUpdateForm(record);
        this.showUpdateModal();
    }

    populateUpdateForm(record) {
        const form = document.getElementById('updateForm');
        
        // Create form fields dynamically
        form.innerHTML = `
            <input type="hidden" name="id" value="${record.id}">
            
            <div class="form-group">
                <label for="update_projectId">Project ID *</label>
                <input type="text" id="update_projectId" name="projectId" value="${record.projectId}" required>
            </div>

            <div class="form-group">
                <label for="update_projectName">Project Name *</label>
                <input type="text" id="update_projectName" name="projectName" value="${record.projectName}" required>
            </div>

            <div class="form-group">
                <label for="update_storeNumber">Store Number</label>
                <input type="number" id="update_storeNumber" name="storeNumber" value="${record.storeNumber || ''}">
            </div>

            <div class="form-group">
                <label for="update_region">Region</label>
                <select id="update_region" name="region">
                    <option value="">Select Region</option>
                    <option value="North" ${record.region === 'North' ? 'selected' : ''}>North</option>
                    <option value="South" ${record.region === 'South' ? 'selected' : ''}>South</option>
                    <option value="East" ${record.region === 'East' ? 'selected' : ''}>East</option>
                    <option value="West" ${record.region === 'West' ? 'selected' : ''}>West</option>
                    <option value="Central" ${record.region === 'Central' ? 'selected' : ''}>Central</option>
                </select>
            </div>

            <div class="form-group">
                <label for="update_district">District</label>
                <input type="text" id="update_district" name="district" value="${record.district || ''}">
            </div>

            <div class="form-group">
                <label for="update_market">Market</label>
                <input type="text" id="update_market" name="market" value="${record.market || ''}">
            </div>

            <div class="form-group">
                <label for="update_projectType">Project Type</label>
                <select id="update_projectType" name="projectType">
                    <option value="">Select Type</option>
                    <option value="Investigation" ${record.projectType === 'Investigation' ? 'selected' : ''}>Investigation</option>
                    <option value="Prevention" ${record.projectType === 'Prevention' ? 'selected' : ''}>Prevention</option>
                    <option value="Training" ${record.projectType === 'Training' ? 'selected' : ''}>Training</option>
                    <option value="Audit" ${record.projectType === 'Audit' ? 'selected' : ''}>Audit</option>
                    <option value="Compliance" ${record.projectType === 'Compliance' ? 'selected' : ''}>Compliance</option>
                </select>
            </div>

            <div class="form-group">
                <label for="update_priority">Priority Level</label>
                <select id="update_priority" name="priority">
                    <option value="">Select Priority</option>
                    <option value="Low" ${record.priority === 'Low' ? 'selected' : ''}>Low</option>
                    <option value="Medium" ${record.priority === 'Medium' ? 'selected' : ''}>Medium</option>
                    <option value="High" ${record.priority === 'High' ? 'selected' : ''}>High</option>
                    <option value="Critical" ${record.priority === 'Critical' ? 'selected' : ''}>Critical</option>
                </select>
            </div>

            <div class="form-group">
                <label for="update_status">Status</label>
                <select id="update_status" name="status">
                    <option value="Planning" ${record.status === 'Planning' ? 'selected' : ''}>Planning</option>
                    <option value="In Progress" ${record.status === 'In Progress' ? 'selected' : ''}>In Progress</option>
                    <option value="On Hold" ${record.status === 'On Hold' ? 'selected' : ''}>On Hold</option>
                    <option value="Completed" ${record.status === 'Completed' ? 'selected' : ''}>Completed</option>
                    <option value="Cancelled" ${record.status === 'Cancelled' ? 'selected' : ''}>Cancelled</option>
                </select>
            </div>

            <div class="form-group">
                <label for="update_assignedTo">Assigned To</label>
                <input type="text" id="update_assignedTo" name="assignedTo" value="${record.assignedTo || ''}">
            </div>

            <div class="form-group full-width">
                <label for="update_startDate">Start Date</label>
                <input type="date" id="update_startDate" name="startDate" value="${record.startDate || ''}">
            </div>

            <div class="form-group full-width">
                <label for="update_targetDate">Target Completion Date</label>
                <input type="date" id="update_targetDate" name="targetDate" value="${record.targetDate || ''}">
            </div>

            <div class="form-group full-width">
                <label for="update_description">Project Description</label>
                <textarea id="update_description" name="description" rows="4">${record.description || ''}</textarea>
            </div>

            <div class="form-group full-width">
                <label for="update_notes">Additional Notes</label>
                <textarea id="update_notes" name="notes" rows="3">${record.notes || ''}</textarea>
            </div>

            <div class="form-actions full-width">
                <button type="submit" class="btn btn-primary">Update Record</button>
                <button type="button" class="btn btn-secondary" onclick="ihManager.closeUpdateModal()">Cancel</button>
            </div>
        `;
    }

    handleUpdateRecord(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const updatedData = {};
        
        for (let [key, value] of formData.entries()) {
            updatedData[key] = value;
        }

        // Validation
        if (!this.validateRecord(updatedData)) {
            return;
        }

        // Check for duplicate Project ID (excluding current record)
        const duplicateRecord = this.records.find(record => 
            record.projectId === updatedData.projectId && record.id !== updatedData.id
        );
        
        if (duplicateRecord) {
            this.showStatusMessage('Project ID already exists. Please use a unique Project ID.', 'error');
            return;
        }

        // Find and update record
        const recordIndex = this.records.findIndex(r => r.id === updatedData.id);
        if (recordIndex === -1) {
            this.showStatusMessage('Record not found', 'error');
            return;
        }

        // Preserve creation date and update modification date
        updatedData.createdDate = this.records[recordIndex].createdDate;
        updatedData.lastModified = new Date().toISOString();

        this.records[recordIndex] = updatedData;
        this.saveRecords();

        this.closeUpdateModal();
        this.showStatusMessage('Record updated successfully!', 'success');

        // Refresh current view
        if (document.getElementById('view').classList.contains('active')) {
            this.loadAllRecords();
        }
        if (document.getElementById('search').classList.contains('active')) {
            this.searchRecords();
        }
    }

    showUpdateModal() {
        document.getElementById('updateModal').style.display = 'block';
    }

    closeUpdateModal() {
        document.getElementById('updateModal').style.display = 'none';
        this.currentEditingRecord = null;
    }

    // Record Deletion
    deleteRecord(recordId) {
        if (!confirm('Are you sure you want to delete this record? This action cannot be undone.')) {
            return;
        }

        const recordIndex = this.records.findIndex(r => r.id === recordId);
        if (recordIndex === -1) {
            this.showStatusMessage('Record not found', 'error');
            return;
        }

        this.records.splice(recordIndex, 1);
        this.saveRecords();
        this.showStatusMessage('Record deleted successfully!', 'success');

        // Refresh current view
        if (document.getElementById('view').classList.contains('active')) {
            this.loadAllRecords();
        }
        if (document.getElementById('search').classList.contains('active')) {
            this.searchRecords();
        }
    }

    // View All Records
    loadAllRecords() {
        const tbody = document.getElementById('recordsTableBody');
        
        if (this.records.length === 0) {
            tbody.innerHTML = '<tr><td colspan="9" style="text-align: center; padding: 40px;">No records found. Create your first record using the "Create New Record" tab.</td></tr>';
            return;
        }

        tbody.innerHTML = this.records.map(record => `
            <tr>
                <td>${record.projectId}</td>
                <td>${record.projectName}</td>
                <td>${record.storeNumber || 'N/A'}</td>
                <td>${record.region || 'N/A'}</td>
                <td><span class="status-badge status-${record.status.toLowerCase().replace(' ', '-')}">${record.status}</span></td>
                <td><span class="status-badge priority-${record.priority.toLowerCase()}">${record.priority}</span></td>
                <td>${record.assignedTo || 'Unassigned'}</td>
                <td>${this.formatDate(record.targetDate)}</td>
                <td>
                    <button class="btn btn-primary" onclick="ihManager.editRecord('${record.id}')" style="margin-right: 5px; padding: 6px 12px; font-size: 0.8rem;">Edit</button>
                    <button class="btn btn-danger" onclick="ihManager.deleteRecord('${record.id}')" style="padding: 6px 12px; font-size: 0.8rem;">Delete</button>
                </td>
            </tr>
        `).join('');
    }

    // Export Functionality
    exportData() {
        if (this.records.length === 0) {
            this.showStatusMessage('No data to export', 'info');
            return;
        }

        // Create CSV content
        const headers = [
            'Project ID', 'Project Name', 'Store Number', 'Region', 'District', 'Market',
            'Project Type', 'Priority', 'Status', 'Assigned To', 'Start Date', 'Target Date',
            'Description', 'Notes', 'Created Date', 'Last Modified'
        ];

        const csvContent = [
            headers.join(','),
            ...this.records.map(record => [
                this.escapeCsvValue(record.projectId),
                this.escapeCsvValue(record.projectName),
                record.storeNumber || '',
                this.escapeCsvValue(record.region),
                this.escapeCsvValue(record.district),
                this.escapeCsvValue(record.market),
                this.escapeCsvValue(record.projectType),
                this.escapeCsvValue(record.priority),
                this.escapeCsvValue(record.status),
                this.escapeCsvValue(record.assignedTo),
                record.startDate || '',
                record.targetDate || '',
                this.escapeCsvValue(record.description),
                this.escapeCsvValue(record.notes),
                this.formatDate(record.createdDate),
                this.formatDate(record.lastModified)
            ].join(','))
        ].join('\n');

        // Create and download file
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', `ih_project_data_${new Date().toISOString().split('T')[0]}.csv`);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        this.showStatusMessage('Data exported successfully!', 'success');
    }

    escapeCsvValue(value) {
        if (!value) return '';
        const stringValue = value.toString();
        if (stringValue.includes(',') || stringValue.includes('"') || stringValue.includes('\n')) {
            return '"' + stringValue.replace(/"/g, '""') + '"';
        }
        return stringValue;
    }

    // Status Messages
    showStatusMessage(message, type = 'info') {
        const statusDiv = document.getElementById('statusMessage');
        statusDiv.textContent = message;
        statusDiv.className = `status-message ${type}`;
        statusDiv.classList.add('show');

        setTimeout(() => {
            statusDiv.classList.remove('show');
        }, 4000);
    }
}

// Global functions for onclick handlers
window.showTab = function(tabName) {
    ihManager.showTab(tabName);
};

window.searchRecords = function() {
    ihManager.searchRecords();
};

window.clearSearch = function() {
    ihManager.clearSearch();
};

window.closeUpdateModal = function() {
    ihManager.closeUpdateModal();
};

window.loadAllRecords = function() {
    ihManager.loadAllRecords();
};

window.exportData = function() {
    ihManager.exportData();
};

// Initialize the application
let ihManager;
document.addEventListener('DOMContentLoaded', function() {
    ihManager = new IHProjectDataManager();
});