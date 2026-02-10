/**
 * Upload Wizard - Main orchestrator for the upload process
 * Manages step navigation, data flow, and final import
 */

const UploadWizard = {
    currentStep: 1,
    totalSteps: 6,
    sourceType: null,     // 'file', 'bigquery', 'api', 'saved'
    sourceData: null,     // Parsed data from source
    connection: null,     // Connection configuration
    managementMode: null, // 'source_connected' or 'activity_hub_managed'
    apiSyncConfig: null,  // API sync configuration if applicable

    /**
     * Initialize the wizard
     */
    async init() {
        // Initialize dependent modules
        await LocalStorageManager.init();
        await ColumnMapper.init();
        await DataValidator.init();

        // Bind navigation buttons
        this.bindNavigation();

        // Bind source selection
        this.bindSourceSelection();

        // Bind file upload
        this.bindFileUpload();

        // Bind management decision
        this.bindManagementDecision();

        // Bind import action
        this.bindImportAction();

        // Render saved connections
        DataConnections.renderSavedConnections();

        // Start at step 1
        this.showStep(1);

        console.log('Upload Wizard initialized');
    },

    /**
     * Bind navigation button events
     */
    bindNavigation() {
        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');

        if (prevBtn) {
            prevBtn.addEventListener('click', () => this.previousStep());
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', () => this.nextStep());
        }
    },

    /**
     * Bind source type selection
     */
    bindSourceSelection() {
        document.querySelectorAll('.connection-card').forEach(card => {
            card.addEventListener('click', () => {
                // Remove selected from all cards
                document.querySelectorAll('.connection-card').forEach(c => c.classList.remove('selected'));
                
                // Add selected to clicked card
                card.classList.add('selected');
                
                // Store source type
                this.sourceType = card.dataset.connection;
                
                // Enable next button
                const nextBtn = document.getElementById('next-btn');
                if (nextBtn) nextBtn.disabled = false;
            });
        });
    },

    /**
     * Bind file upload events
     */
    bindFileUpload() {
        const dropZone = document.getElementById('upload-zone');
        const fileInput = document.getElementById('file-input');
        const browseBtn = document.getElementById('browse-btn');

        if (!dropZone) return;

        // Browse button click
        browseBtn?.addEventListener('click', () => fileInput?.click());

        // File input change
        fileInput?.addEventListener('change', (e) => {
            if (e.target.files?.length > 0) {
                this.handleFileUpload(e.target.files[0]);
            }
        });

        // Drag and drop
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('drag-over');
        });

        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('drag-over');
        });

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('drag-over');
            if (e.dataTransfer.files?.length > 0) {
                this.handleFileUpload(e.dataTransfer.files[0]);
            }
        });

        // Remove file button
        document.getElementById('remove-file')?.addEventListener('click', () => {
            this.sourceData = null;
            this.connection = null;
            document.getElementById('upload-zone')?.classList.remove('hidden');
            document.getElementById('file-preview')?.classList.add('hidden');
            document.getElementById('file-input').value = '';
            const nextBtn = document.getElementById('next-btn');
            if (nextBtn) nextBtn.disabled = true;
        });
    },

    /**
     * Handle file upload
     */
    async handleFileUpload(file) {
        const uploadZone = document.getElementById('upload-zone');
        const filePreview = document.getElementById('file-preview');
        const fileName = document.getElementById('file-name');
        const fileMeta = document.getElementById('file-meta');
        const previewTable = document.getElementById('preview-table');

        try {
            fileName.textContent = file.name;

            // Parse the file
            const result = await FileParser.parseFile(file);

            this.sourceData = result;
            this.connection = { type: 'file', name: file.name };

            // Show preview, hide upload zone
            uploadZone.classList.add('hidden');
            filePreview.classList.remove('hidden');
            
            fileMeta.textContent = `${result.totalRows} rows • ${result.columns.length} columns detected`;
            this.renderPreviewTable(previewTable, result);

            // Enable next button
            const nextBtn = document.getElementById('next-btn');
            if (nextBtn) nextBtn.disabled = false;

        } catch (error) {
            fileMeta.textContent = `Error: ${error.message}`;
            console.error('File parse error:', error);
        }
    },

    /**
     * Render preview table
     */
    renderPreviewTable(container, data) {
        if (!container || !data) return;

        const previewRows = data.records.slice(0, 5);

        container.innerHTML = `
            <table>
                <thead>
                    <tr>${data.columns.map(col => `<th>${col}</th>`).join('')}</tr>
                </thead>
                <tbody>
                    ${previewRows.map(row => `
                        <tr>${data.columns.map(col => `<td>${row[col] || ''}</td>`).join('')}</tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    },

    /**
     * Bind management decision events
     */
    bindManagementDecision() {
        document.querySelectorAll('.decision-card').forEach(card => {
            card.addEventListener('click', () => {
                // Remove selected from all
                document.querySelectorAll('.decision-card').forEach(c => c.classList.remove('selected'));
                
                // Add selected
                card.classList.add('selected');
                
                // Store decision
                this.managementMode = card.dataset.mode;

                // Show/hide API setup if applicable
                const apiSetup = document.getElementById('api-setup');
                if (apiSetup) {
                    if (this.managementMode === 'source_connected' && this.sourceType === 'api') {
                        apiSetup.classList.remove('hidden');
                    } else {
                        apiSetup.classList.add('hidden');
                    }
                }

                // Enable next button
                const nextBtn = document.getElementById('next-btn');
                if (nextBtn) nextBtn.disabled = false;
            });
        });

        // Sync direction change
        document.getElementById('sync-direction')?.addEventListener('change', (e) => {
            const biDiWarning = document.getElementById('bidirectional-warning');
            if (biDiWarning) {
                biDiWarning.classList.toggle('hidden', e.target.value !== 'bidirectional');
            }
        });
    },

    /**
     * Bind import action
     */
    bindImportAction() {
        document.getElementById('start-import')?.addEventListener('click', () => {
            this.executeImport();
        });
    },

    /**
     * Show specific step
     */
    showStep(stepNumber) {
        // Validate step number
        stepNumber = Math.max(1, Math.min(stepNumber, this.totalSteps));

        // Hide all wizard content steps
        document.querySelectorAll('.wizard-content').forEach(content => {
            content.classList.add('hidden');
        });

        // Show target step
        const targetStep = document.getElementById(`step-${stepNumber}`);
        if (targetStep) {
            targetStep.classList.remove('hidden');
        }

        // Update progress indicator
        this.updateProgress(stepNumber);

        // Update navigation buttons
        this.updateNavButtons(stepNumber);

        // Run step-specific setup
        this.setupStep(stepNumber);

        this.currentStep = stepNumber;
    },

    /**
     * Update navigation button states
     */
    updateNavButtons(stepNumber) {
        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');

        if (prevBtn) {
            prevBtn.disabled = stepNumber === 1;
        }

        if (nextBtn) {
            // On step 6, hide next button (import step)
            if (stepNumber === 6) {
                nextBtn.style.display = 'none';
            } else {
                nextBtn.style.display = '';
                // Disable next until user makes a selection
                nextBtn.disabled = true;
                
                // Re-enable if selection already made
                if (stepNumber === 1 && this.sourceType) {
                    nextBtn.disabled = false;
                } else if (stepNumber === 2 && this.sourceData) {
                    nextBtn.disabled = false;
                } else if (stepNumber === 3) {
                    nextBtn.disabled = false; // Auto-enabled on mapping step
                } else if (stepNumber === 4) {
                    nextBtn.disabled = false; // Validation step always allows proceed
                } else if (stepNumber === 5 && this.managementMode) {
                    nextBtn.disabled = false;
                }
            }
        }
    },

    /**
     * Update progress indicators
     */
    updateProgress(stepNumber) {
        document.querySelectorAll('.wizard-steps .wizard-step').forEach((step, index) => {
            step.classList.remove('active', 'completed');
            if (index + 1 < stepNumber) {
                step.classList.add('completed');
            } else if (index + 1 === stepNumber) {
                step.classList.add('active');
            }
        });
    },

    /**
     * Setup specific step content
     */
    setupStep(stepNumber) {
        switch (stepNumber) {
            case 2:
                this.setupSourceStep();
                break;
            case 3:
                this.setupMappingStep();
                break;
            case 4:
                this.setupValidationStep();
                break;
            case 5:
                this.setupDecisionStep();
                break;
            case 6:
                this.setupImportStep();
                break;
        }
    },

    /**
     * Setup source selection step based on source type
     */
    setupSourceStep() {
        // Show/hide source panels based on selection
        document.querySelectorAll('.source-panel').forEach(panel => {
            panel.classList.add('hidden');
        });

        if (this.sourceType === 'file') {
            document.getElementById('source-file')?.classList.remove('hidden');
        } else if (this.sourceType === 'bigquery') {
            document.getElementById('source-bigquery')?.classList.remove('hidden');
        } else if (this.sourceType === 'api') {
            document.getElementById('source-api')?.classList.remove('hidden');
        } else if (this.sourceType === 'saved') {
            document.getElementById('source-saved')?.classList.remove('hidden');
            DataConnections.renderSavedConnections();
        }
    },

    /**
     * Setup mapping step
     */
    setupMappingStep() {
        console.log('setupMappingStep called');
        console.log('sourceData:', this.sourceData);
        
        if (!this.sourceData) {
            console.warn('No sourceData available for mapping');
            return;
        }

        // Pass source columns to mapper
        ColumnMapper.sourceColumns = this.sourceData.columns;
        console.log('Set ColumnMapper.sourceColumns:', ColumnMapper.sourceColumns);
        
        ColumnMapper.detectColumnTypes(this.sourceData.records.slice(0, 100));

        // Run auto-mapping first
        ColumnMapper.autoMap();
        
        // Then render mapping UI with the mappings applied
        ColumnMapper.render();
    },

    /**
     * Setup validation step
     */
    setupValidationStep() {
        if (!this.sourceData) return;

        // Check required mappings first
        const reqCheck = DataValidator.checkRequiredMappings(ColumnMapper.mappings);
        if (!reqCheck.valid) {
            alert(`Missing required field mappings: ${reqCheck.unmappedFields.join(', ')}`);
            this.showStep(3);
            return;
        }

        // Run validation
        const results = DataValidator.validateAll(this.sourceData.records, ColumnMapper.mappings);

        // Render results
        DataValidator.renderValidationSummary();
        DataValidator.renderValidationTable();

        // Bind filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                DataValidator.renderValidationTable(e.target.dataset.filter);
            });
        });
    },

    /**
     * Setup management decision step
     */
    setupDecisionStep() {
        const summaryEl = document.getElementById('import-summary');
        if (summaryEl && DataValidator.validationResults) {
            const results = DataValidator.validationResults;
            summaryEl.innerHTML = `
                <strong>Ready to import ${results.validRecords} records</strong>
                ${results.invalidRecords > 0 ? `<br><small>${results.invalidRecords} records will be skipped due to errors</small>` : ''}
            `;
        }
    },

    /**
     * Setup final import step
     */
    setupImportStep() {
        const finalSummary = document.getElementById('final-summary');
        if (!finalSummary) return;

        const validRecords = DataValidator.validationResults?.validRecords || 0;
        const mode = this.managementMode === 'source_connected' 
            ? 'Keep data connected to source' 
            : 'Activity Hub will manage data';

        finalSummary.innerHTML = `
            <div class="summary-item"><strong>Source:</strong> ${this.connection?.name || this.sourceType}</div>
            <div class="summary-item"><strong>Records to Import:</strong> ${validRecords}</div>
            <div class="summary-item"><strong>Management Mode:</strong> ${mode}</div>
            <div class="summary-item"><strong>Mapped Fields:</strong> ${Object.keys(ColumnMapper.mappings).filter(k => ColumnMapper.mappings[k].sourceColumn).length}</div>
        `;
    },

    /**
     * Go to next step
     */
    nextStep() {
        if (this.validateCurrentStep()) {
            this.showStep(this.currentStep + 1);
        }
    },

    /**
     * Go to previous step
     */
    previousStep() {
        this.showStep(this.currentStep - 1);
    },

    /**
     * Go to specific step
     */
    goToStep(stepNumber) {
        this.showStep(stepNumber);
    },

    /**
     * Validate current step before proceeding
     */
    validateCurrentStep() {
        switch (this.currentStep) {
            case 1:
                if (!this.sourceType) {
                    alert('Please select a data source type');
                    return false;
                }
                return true;

            case 2:
                if (!this.sourceData || !this.sourceData.records.length) {
                    alert('Please upload or connect to your data source');
                    return false;
                }
                return true;

            case 3:
                const reqCheck = DataValidator.checkRequiredMappings(ColumnMapper.mappings);
                if (!reqCheck.valid) {
                    alert(`Please map required fields: ${reqCheck.unmappedFields.join(', ')}`);
                    return false;
                }
                return true;

            case 4:
                if (DataValidator.validationResults?.validRecords === 0) {
                    alert('No valid records to import. Please fix validation errors.');
                    return false;
                }
                return true;

            case 5:
                if (!this.managementMode) {
                    alert('Please select how you want to manage your data');
                    return false;
                }
                return true;

            default:
                return true;
        }
    },

    /**
     * Set connection from saved connections
     */
    setConnection(connection) {
        this.connection = connection;
        this.sourceType = connection.type;
    },

    /**
     * Execute the final import
     */
    async executeImport() {
        const progressFill = document.querySelector('.progress-fill');
        const progressText = document.querySelector('.progress-text');
        const importProgress = document.getElementById('import-progress');
        const importComplete = document.getElementById('import-complete');
        const startBtn = document.getElementById('start-import');

        try {
            startBtn.disabled = true;
            importProgress.classList.remove('hidden');

            // Get valid records
            const validRecords = DataValidator.getValidRecords();
            const totalRecords = validRecords.length;

            // Transform records using mapping
            const transformedRecords = [];
            
            for (let i = 0; i < totalRecords; i++) {
                const record = validRecords[i];
                const transformed = this.transformRecord(record, ColumnMapper.mappings);
                
                // Add metadata
                transformed._source = this.connection?.name || this.sourceType;
                transformed._importedAt = new Date().toISOString();
                transformed._managementMode = this.managementMode;

                if (this.managementMode === 'source_connected') {
                    transformed._sourceConfig = this.connection;
                }

                transformedRecords.push(transformed);

                // Update progress
                const progress = Math.round(((i + 1) / totalRecords) * 80);
                progressFill.style.width = `${progress}%`;
                progressText.textContent = `Processing ${i + 1} of ${totalRecords}...`;

                // Yield to UI
                if (i % 100 === 0) {
                    await new Promise(r => setTimeout(r, 0));
                }
            }

            // Save to IndexedDB
            progressText.textContent = 'Saving to database...';
            await LocalStorageManager.addProjects(transformedRecords);

            // Save upload record
            const uploadRecord = await LocalStorageManager.createUpload({
                sourceType: this.sourceType,
                sourceName: this.connection?.name,
                recordsImported: transformedRecords.length,
                mapping: ColumnMapper.mappings,
                managementMode: this.managementMode
            });

            // Complete!
            progressFill.style.width = '100%';
            progressText.textContent = 'Complete!';

            // Show completion message
            setTimeout(() => {
                importProgress.classList.add('hidden');
                importComplete.classList.remove('hidden');
                
                document.getElementById('imported-count').textContent = transformedRecords.length;
                document.getElementById('upload-id').textContent = uploadRecord.id;
            }, 500);

        } catch (error) {
            console.error('Import error:', error);
            progressText.textContent = `Error: ${error.message}`;
            startBtn.disabled = false;
        }
    },

    /**
     * Transform a record using the mapping configuration
     */
    transformRecord(sourceRecord, mappings) {
        const transformed = {};

        Object.entries(mappings).forEach(([targetField, mapping]) => {
            if (!mapping.sourceColumn) return;

            let value = sourceRecord[mapping.sourceColumn];

            // Apply transformation if specified
            if (mapping.transformation && value !== null && value !== undefined) {
                value = this.applyTransformation(value, mapping.transformation, mapping.transformOptions);
            }

            transformed[targetField] = value;
        });

        return transformed;
    },

    /**
     * Apply a transformation to a value
     */
    applyTransformation(value, transformation, options = {}) {
        switch (transformation) {
            case 'trim':
                return String(value).trim();

            case 'uppercase':
                return String(value).toUpperCase();

            case 'lowercase':
                return String(value).toLowerCase();

            case 'parse_date':
                const date = new Date(value);
                return isNaN(date.getTime()) ? null : date.toISOString();

            case 'parse_number':
                const num = parseFloat(String(value).replace(/[^0-9.-]/g, ''));
                return isNaN(num) ? null : num;

            case 'extract_store_number':
                const storeMatch = String(value).match(/\d+/);
                return storeMatch ? parseInt(storeMatch[0], 10) : null;

            case 'map_values':
                if (options.valueMap) {
                    const normalizedValue = String(value).toLowerCase().trim();
                    return options.valueMap[normalizedValue] || value;
                }
                return value;

            case 'prefix':
                return options.prefix ? `${options.prefix}${value}` : value;

            default:
                return value;
        }
    },

    /**
     * View imported projects
     */
    viewProjects() {
        window.location.href = '../index.html';
    },

    /**
     * Start a new upload
     */
    newUpload() {
        // Reset state
        this.sourceType = null;
        this.sourceData = null;
        this.connection = null;
        this.managementMode = null;
        this.apiSyncConfig = null;

        // Reset UI
        document.querySelectorAll('.source-card').forEach(c => c.classList.remove('selected'));
        document.querySelectorAll('.decision-card').forEach(c => c.classList.remove('selected'));
        document.getElementById('import-complete')?.classList.add('hidden');

        // Go to step 1
        this.showStep(1);
    }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    UploadWizard.init();
});
