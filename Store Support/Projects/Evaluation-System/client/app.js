/**
 * Evaluation System Client
 * Handles UI, file upload, mapping, and generation
 */

let currentStep = 1;
let uploadedData = null;
let mappedData = null;
let generatedEvaluation = null;
let evaluationScore = null;
let evaluationSummary = null;
let systemFields = null;
let columnMappings = {};
let userInfo = {};

const API = 'http://localhost:3001/api';

// ============ INITIALIZATION ============

document.addEventListener('DOMContentLoaded', async () => {
    loadSystemFields();
    setupEventListeners();
});

async function loadSystemFields() {
    try {
        const response = await fetch(`${API}/fields`);
        const data = await response.json();
        systemFields = data.fields;
        console.log('System fields loaded:', Object.keys(systemFields).length);
    } catch (error) {
        showAlert('Failed to load system fields', 'error');
    }
}

function setupEventListeners() {
    // File upload drag and drop
    const fileUpload = document.getElementById('fileUpload');
    fileUpload.addEventListener('click', () => document.getElementById('fileInput').click());
}

// ============ NAVIGATION ============

function goToStep(step) {
    // Validate step transitions
    if (step === 2 && !validateUserInfo()) return;
    if (step === 3 && !uploadedData) {
        showAlert('Please upload a file first', 'error');
        return;
    }
    if (step === 4 && !validateColumnMappings()) {
        showAlert('Please map all required columns', 'error');
        return;
    }

    // Hide all sections
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));

    // Show selected section
    document.getElementById(`step${step}`).classList.add('active');

    // Update sidebar
    document.querySelectorAll('.step').forEach((s, i) => {
        s.classList.remove('active');
        if (i + 1 <= step) s.classList.add('completed');
        if (i + 1 === step) s.classList.add('active');
    });

    currentStep = step;
}

// ============ STEP 1: USER INFO ============

function validateUserInfo() {
    const name = document.getElementById('userName').value.trim();
    const period = document.getElementById('evaluationPeriod').value;

    if (!name) {
        showAlert('Please enter your name', 'error');
        return false;
    }

    if (!period) {
        showAlert('Please select an evaluation period', 'error');
        return false;
    }

    userInfo = {
        name: name,
        title: document.getElementById('userTitle').value.trim(),
        email: document.getElementById('userEmail').value.trim(),
        period: period
    };

    return true;
}

function resetForm() {
    document.getElementById('userForm').reset();
    uploadedData = null;
    mappedData = null;
    generatedEvaluation = null;
    columnMappings = {};
    userInfo = {};
    document.getElementById('filePreview').style.display = 'none';
    document.getElementById('generateResult').classList.remove('show');
    document.getElementById('nextButton').disabled = true;
    goToStep(1);
}

// ============ STEP 2: FILE UPLOAD ============

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        uploadFile(file);
    }
}

function handleDragOver(event) {
    event.preventDefault();
    event.stopPropagation();
    document.getElementById('fileUpload').classList.add('dragover');
}

function handleDragLeave(event) {
    event.preventDefault();
    event.stopPropagation();
    document.getElementById('fileUpload').classList.remove('dragover');
}

function handleDrop(event) {
    event.preventDefault();
    event.stopPropagation();
    document.getElementById('fileUpload').classList.remove('dragover');
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        uploadFile(files[0]);
    }
}

async function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
        showAlert('', ''); // Clear alerts
        const response = await fetch(`${API}/upload`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error);
        }

        const result = await response.json();
        uploadedData = result.fullData;

        // Display preview
        displayPreview(result.data, result.availableColumns, result.totalRows);

        showAlert(`Loaded ${result.totalRows} rows from file`, 'success');
        document.getElementById('nextButton').disabled = false;

    } catch (error) {
        showAlert(error.message, 'error');
    }
}

function displayPreview(data, columns, totalRows) {
    const table = document.getElementById('previewTable');
    table.innerHTML = '';

    // Header
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    columns.forEach(col => {
        const th = document.createElement('th');
        th.textContent = col;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Body
    const tbody = document.createElement('tbody');
    data.forEach(row => {
        const tr = document.createElement('tr');
        columns.forEach(col => {
            const td = document.createElement('td');
            td.textContent = row[col] || '-';
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
    table.appendChild(tbody);

    document.getElementById('totalRows').textContent = totalRows;
    document.getElementById('filePreview').style.display = 'block';
}

// ============ STEP 3: COLUMN MAPPING ============

async function loadMappingInterface() {
    if (!uploadedData || uploadedData.length === 0) return;

    const headers = Object.keys(uploadedData[0]);
    const container = document.getElementById('mappingContainer');
    container.innerHTML = '';

    // Group fields by category
    const categories = {};
    Object.entries(systemFields).forEach(([fieldName, field]) => {
        if (!categories[field.category]) {
            categories[field.category] = [];
        }
        categories[field.category].push({ fieldName, ...field });
    });

    // Create mapping table
    let html = '<table class="mapping-table"><thead><tr><th>Your Column</th><th>Maps To</th><th>Field Type</th><th></th></tr></thead><tbody>';

    headers.forEach(header => {
        const required = Object.values(systemFields).some(f => f.required && f.label.toLowerCase().includes(header.toLowerCase())) ? ' <span style="color: red;">*</span>' : '';
        
        let options = '<option value="">-- Not mapped --</option>';
        Object.entries(systemFields).forEach(([fieldName, field]) => {
            const selected = columnMappings[header] === fieldName ? 'selected' : '';
            options += `<option value="${fieldName}" ${selected}>${field.label}</option>`;
        });

        const info = columnMappings[header] && systemFields[columnMappings[header]] 
            ? systemFields[columnMappings[header]].info 
            : 'Select a field to see description';

        html += `
            <tr>
                <td><strong>${header}</strong>${required}</td>
                <td>
                    <select onchange="columnMappings['${header}'] = this.value">
                        ${options}
                    </select>
                </td>
                <td>${columnMappings[header] ? systemFields[columnMappings[header]].type : '-'}</td>
                <td>
                    <div class="info-tooltip">i
                        <span class="tooltip-text">${info}</span>
                    </div>
                </td>
            </tr>
        `;
    });

    html += '</tbody></table>';
    container.innerHTML = html;
}

function validateColumnMappings() {
    const requiredFields = ['project_name', 'description', 'accomplishment'];
    const mappedFields = Object.values(columnMappings);

    const allRequired = requiredFields.every(field => mappedFields.includes(field));

    if (!allRequired) {
        const missing = requiredFields.filter(f => !mappedFields.includes(f))
            .map(f => systemFields[f].label)
            .join(', ');
        showAlert(`Missing required fields: ${missing}`, 'error');
        return false;
    }

    return true;
}

// Override goToStep to load mapping when going to step 3
const originalGoToStep = goToStep;
goToStep = function(step) {
    if (step === 3 && uploadedData) {
        loadMappingInterface();
    }
    originalGoToStep(step);
};

// ============ STEP 4: GENERATE ============

async function generateEvaluation() {
    if (!validateUserInfo() || !uploadedData || !validateColumnMappings()) {
        return;
    }

    document.getElementById('loadingDiv').classList.add('show');
    document.getElementById('generateResult').classList.remove('show');

    try {
        // Map the data
        mappedData = mapData(uploadedData, columnMappings);

        // Send to server for generation
        const response = await fetch(`${API}/evaluate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                data: mappedData,
                columnMappings: columnMappings,
                userInfo: userInfo
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Generation failed');
        }

        const result = await response.json();
        generatedEvaluation = result.evaluation;
        evaluationScore = result.score;
        evaluationSummary = result.summary;

        // Display results
        document.getElementById('scoreDisplay').textContent = evaluationScore;
        const scoreLabel = evaluationScore >= 80 ? 'Exceeds Expectations' : 
                          evaluationScore >= 70 ? 'Meets Expectations' : 'Developing';
        document.getElementById('scoreLabel').textContent = scoreLabel;

        document.getElementById('loadingDiv').classList.remove('show');
        document.getElementById('generateResult').classList.add('show');
        document.getElementById('generateBtn').style.display = 'none';
        document.getElementById('nextReviewBtn').style.display = 'inline-block';

        showAlert('Evaluation generated successfully!', 'success');

    } catch (error) {
        document.getElementById('loadingDiv').classList.remove('show');
        showAlert(error.message, 'error');
    }
}

function mapData(data, mappings) {
    return data.map(row => {
        const mapped = {};
        Object.entries(mappings).forEach(([sourceCol, targetField]) => {
            if (targetField && row[sourceCol]) {
                mapped[targetField] = row[sourceCol];
            }
        });
        return mapped;
    });
}

// ============ STEP 5: REVIEW & DOWNLOAD ============

async function generateHTML() {
    if (!generatedEvaluation) return;

    try {
        const response = await fetch(`${API}/generate-html`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                evaluation: generatedEvaluation,
                score: evaluationScore,
                userInfo: userInfo
            })
        });

        if (!response.ok) throw new Error('Failed to generate HTML');

        const result = await response.json();
        displayReview(result.html);

    } catch (error) {
        showAlert(error.message, 'error');
    }
}

function displayReview(html) {
    const container = document.getElementById('reviewContent');
    container.innerHTML = `
        <div style="margin-bottom: 20px;">
            <p style="color: #666;">Below is your generated evaluation. You can:</p>
            <ul style="margin-left: 20px; color: #666;">
                <li>Review the content</li>
                <li>Edit the HTML before downloading</li>
                <li>Download as HTML file for sharing</li>
            </ul>
        </div>
        <div style="background: var(--light); padding: 20px; border-radius: 4px; max-height: 600px; overflow-y: auto;">
            <textarea id="htmlContent" style="width: 100%; height: 400px; padding: 10px; border: 1px solid var(--border); border-radius: 4px; font-family: monospace; font-size: 12px;">${escapeHtml(html)}</textarea>
        </div>
    `;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function downloadHTML() {
    let html = document.getElementById('htmlContent')?.value;
    
    if (!html) {
        // Generate fresh HTML
        const response = await fetch(`${API}/generate-html`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                evaluation: generatedEvaluation,
                score: evaluationScore,
                userInfo: userInfo
            })
        });
        const result = await response.json();
        html = result.html;
    }

    try {
        const response = await fetch(`${API}/download-html`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                evaluation: generatedEvaluation,
                score: evaluationScore,
                userInfo: userInfo
            })
        });

        if (!response.ok) throw new Error('Download failed');

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `Evaluation_${userInfo.name}_${new Date().toISOString().split('T')[0]}.html`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);

        showAlert('Evaluation downloaded successfully!', 'success');

    } catch (error) {
        showAlert(error.message, 'error');
    }
}

// ============ UTILITIES ============

function showAlert(message, type) {
    const alert = document.getElementById('alert');
    alert.innerHTML = message;
    alert.className = `alert ${type}`;

    if (message) {
        alert.classList.add('show');
        if (type === 'success') {
            setTimeout(() => alert.classList.remove('show'), 5000);
        }
    } else {
        alert.classList.remove('show');
    }
}

// Load mapping interface before going to step 5
const step5Trigger = goToStep;
let originalGotoStep5 = step5Trigger;
window.goToStep = function(step) {
    if (step === 5 && generatedEvaluation && !document.getElementById('htmlContent')) {
        generateHTML();
    }
    originalGotoStep5(step);
};

// ============ HOSTING GUIDE MODAL ============

function openHostingGuide() {
    const modal = document.getElementById('hostingModal');
    modal.classList.add('show');
    // Reset to overview tab
    switchHostingTab('overview');
    // Reset selector
    document.getElementById('hostingSelector').value = '';
}

function closeHostingGuide() {
    const modal = document.getElementById('hostingModal');
    modal.classList.remove('show');
}

function switchHostingTab(tabName) {
    // Hide all content
    document.querySelectorAll('.hosting-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active from all tabs
    document.querySelectorAll('.hosting-tab').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected content
    document.getElementById(tabName).classList.add('active');
    
    // Mark clicked tab as active
    event.target.classList.add('active');
}

function updateHostingInfo() {
    const selector = document.getElementById('hostingSelector').value;
    if (!selector) return;
    
    // Switch to overview tab to show details
    switchHostingTab('overview');
    
    // Scroll to the relevant card
    const cardTexts = {
        'codepuppy': 'Code Puppy Pages',
        'posit': 'Posit (RStudio Connect)',
        'selfhosted': 'Self-Hosted Server',
        'wm': 'Walmart Internal Resources',
        'mywm': 'MyWM Experiments',
        'power': 'Power Apps (Microsoft Power Platform)'
    };
    
    const cardTitle = cardTexts[selector];
    const allCards = document.querySelectorAll('.hosting-card');
    
    for (let card of allCards) {
        if (card.textContent.includes(cardTitle)) {
            card.scrollIntoView({ behavior: 'smooth', block: 'center' });
            // Highlight the card briefly
            card.style.background = '#e3f2fd';
            setTimeout(() => {
                card.style.background = '#f9f9f9';
            }, 2000);
            break;
        }
    }
}

// Close modal when clicking outside of it
window.onclick = function(event) {
    const modal = document.getElementById('hostingModal');
    if (event.target === modal) {
        modal.classList.remove('show');
    }
};
