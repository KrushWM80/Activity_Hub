/**
 * Column Mapper
 * Handles mapping source columns to the Activity Hub schema
 * Uses aliases from the schema for auto-mapping
 */

const ColumnMapper = {
    schema: null,
    sourceColumns: [],
    columnStats: {},
    mappings: {}, // { targetField: { sourceColumn: 'SourceCol', transformation: null } }
    valueMappings: {}, // { targetField: { 'sourceValue': 'targetValue' } } for enum conversions
    schemaPath: '../../Admin/Data-Bridge/Schemas/projects-schema.json',
    dataConnection: null, // The data connection being used for this upload
    autoPopulateValues: {}, // { fieldName: value } - values set automatically based on connection

    /**
     * Initialize with schema
     */
    async init() {
        await this.loadSchema();
        return this;
    },

    /**
     * Load the projects schema
     */
    async loadSchema() {
        try {
            const response = await fetch(this.schemaPath);
            if (!response.ok) {
                throw new Error('Failed to load schema');
            }
            this.schema = await response.json();
        } catch (error) {
            console.error('Error loading schema:', error);
            // Fallback to inline schema if file not accessible
            this.schema = this.getFallbackSchema();
        }
    },

    /**
     * Get all schema fields flattened
     */
    getAllSchemaFields() {
        if (!this.schema) return [];

        const fields = [];
        Object.entries(this.schema.columns).forEach(([category, categoryData]) => {
            categoryData.fields.forEach(field => {
                fields.push({
                    ...field,
                    category: category,
                    categoryDescription: categoryData.description
                });
            });
        });
        return fields;
    },

    /**
     * Get required fields
     */
    getRequiredFields() {
        return this.getAllSchemaFields().filter(f => f.required);
    },

    /**
     * Get fields that users can map (excludes auto-populated fields)
     */
    getUserMappableFields() {
        return this.getAllSchemaFields().filter(f => !f.autoPopulate);
    },

    /**
     * Get auto-populated fields
     */
    getAutoPopulateFields() {
        return this.getAllSchemaFields().filter(f => f.autoPopulate);
    },

    /**
     * Set the data connection for this upload
     * Auto-populates project_source based on connection
     */
    setDataConnection(connectionName) {
        this.dataConnection = connectionName;
        // Auto-populate project_source based on the connection
        this.autoPopulateValues = {
            project_source: connectionName
        };
        console.log('Data connection set:', connectionName, 'Auto-populate:', this.autoPopulateValues);
    },

    /**
     * Get auto-populated value for a field
     */
    getAutoPopulateValue(fieldName) {
        return this.autoPopulateValues[fieldName] || null;
    },

    /**
     * Set source columns from parsed file
     */
    setSourceColumns(headers, columnStats = {}) {
        this.sourceColumns = headers;
        this.columnStats = columnStats;
        this.mappings = {};
    },

    /**
     * Detect column types from sample data
     */
    detectColumnTypes(records) {
        if (!records || records.length === 0) return;

        this.sourceColumns.forEach(column => {
            const values = records.map(r => r[column]).filter(v => v != null && v !== '');
            const sampleValues = values.slice(0, 3);
            
            // Try to detect type
            let detectedType = 'string';
            if (values.length > 0) {
                const allNumbers = values.every(v => !isNaN(parseFloat(v)));
                const allDates = values.every(v => !isNaN(Date.parse(v)));
                
                if (allNumbers) detectedType = 'number';
                else if (allDates && values[0].length > 6) detectedType = 'date';
            }

            this.columnStats[column] = {
                sampleValues,
                detectedType,
                nonEmptyCount: values.length,
                totalCount: records.length
            };
        });
    },

    /**
     * Main render method - renders both source and target panels
     */
    render() {
        console.log('ColumnMapper.render() called');
        console.log('sourceColumns:', this.sourceColumns);
        console.log('schema:', this.schema);
        
        const sourceContainer = document.getElementById('source-columns');
        const targetContainer = document.getElementById('target-schema');
        
        console.log('source-columns element:', sourceContainer);
        console.log('target-schema element:', targetContainer);
        
        if (!this.schema) {
            console.warn('Schema not loaded, using fallback');
            this.schema = this.getFallbackSchema();
        }
        
        if (!this.sourceColumns || this.sourceColumns.length === 0) {
            console.warn('No source columns available');
            if (sourceContainer) {
                sourceContainer.innerHTML = '<p class="empty-state">No columns detected. Please upload a file first.</p>';
            }
            return;
        }
        
        this.renderSourceColumns('source-columns');
        this.renderSchemaFields('target-schema');
        this.updateStats();
        this.bindEvents();
    },

    /**
     * Bind mapping-related events
     */
    bindEvents() {
        // Auto-map button
        document.getElementById('auto-map-btn')?.addEventListener('click', () => {
            this.autoMap();
            this.render();
        });

        // Clear all button
        document.getElementById('clear-mapping-btn')?.addEventListener('click', () => {
            this.mappings = {};
            this.render();
        });
    },

    /**
     * Auto-map columns using aliases
     */
    autoMap() {
        this.mappings = {};
        const allFields = this.getAllSchemaFields();
        const usedSourceColumns = new Set();

        allFields.forEach(field => {
            // Check exact match first
            const exactMatch = this.sourceColumns.find(col => 
                col.toLowerCase() === field.name.toLowerCase()
            );

            if (exactMatch && !usedSourceColumns.has(exactMatch)) {
                this.mappings[field.name] = {
                    sourceColumn: exactMatch,
                    transformation: field.transformation || null
                };
                usedSourceColumns.add(exactMatch);
                return;
            }

            // Check aliases
            if (field.aliases) {
                for (const alias of field.aliases) {
                    const aliasMatch = this.sourceColumns.find(col =>
                        col.toLowerCase() === alias.toLowerCase()
                    );

                    if (aliasMatch && !usedSourceColumns.has(aliasMatch)) {
                        this.mappings[field.name] = {
                            sourceColumn: aliasMatch,
                            transformation: field.transformation || null
                        };
                        usedSourceColumns.add(aliasMatch);
                        break;
                    }
                }
            }
        });

        return this.mappings;
    },

    /**
     * Set a specific mapping
     */
    setMapping(targetField, sourceColumn, transformation = null) {
        if (sourceColumn) {
            this.mappings[targetField] = {
                sourceColumn: sourceColumn,
                transformation: transformation
            };
            
            // Check if this field has enum values and if source values need mapping
            this.checkValueMismatch(targetField, sourceColumn);
        } else {
            delete this.mappings[targetField];
            delete this.valueMappings[targetField];
        }
    },
    
    /**
     * Check if source values mismatch target enum options
     */
    checkValueMismatch(targetField, sourceColumn) {
        const field = this.getFieldByName(targetField);
        if (!field) return;
        
        // Get allowed values from validation.enum
        const allowedValues = field.validation?.enum || [];
        if (allowedValues.length === 0) return;
        
        // Get unique source values from the data
        const stats = this.columnStats[sourceColumn];
        if (!stats) return;
        
        // Get all unique values from source data (we may need more than sample)
        const sourceValues = this.getUniqueSourceValues(sourceColumn);
        
        // Check if any source values are NOT in allowed values
        const mismatches = sourceValues.filter(v => 
            v && !allowedValues.some(av => av.toLowerCase() === v.toLowerCase())
        );
        
        if (mismatches.length > 0) {
            // Show value mapping UI
            this.showValueMappingModal(targetField, sourceColumn, sourceValues, allowedValues, mismatches);
        }
    },
    
    /**
     * Get field definition by name
     */
    getFieldByName(fieldName) {
        const allFields = this.getAllSchemaFields();
        return allFields.find(f => f.name === fieldName);
    },
    
    /**
     * Get unique values from source column
     */
    getUniqueSourceValues(sourceColumn) {
        // Access parsed data from FileParser
        if (typeof FileParser !== 'undefined' && FileParser.parsedData) {
            const values = FileParser.parsedData.map(row => row[sourceColumn]).filter(v => v != null && v !== '');
            return [...new Set(values)];
        }
        
        // Fallback to sample values
        const stats = this.columnStats[sourceColumn];
        return stats?.sampleValues || [];
    },
    
    /**
     * Show value mapping modal
     */
    showValueMappingModal(targetField, sourceColumn, sourceValues, allowedValues, mismatches) {
        const field = this.getFieldByName(targetField);
        const fieldName = field?.name || targetField;
        const displayName = fieldName.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
        
        // Create modal
        const modal = document.createElement('div');
        modal.className = 'value-mapping-modal';
        modal.innerHTML = `
            <div class="value-mapping-content">
                <div class="value-mapping-header">
                    <h3>⚠️ Value Alignment Required</h3>
                    <button class="close-btn" onclick="ColumnMapper.closeValueMappingModal()">&times;</button>
                </div>
                <div class="value-mapping-body">
                    <p class="mapping-explanation">
                        The column <strong>"${sourceColumn}"</strong> has values that don't match our <strong>"${displayName}"</strong> options.
                        Please map your values to the allowed options below.
                    </p>
                    
                    <div class="value-mapping-comparison">
                        <div class="values-section">
                            <h4>Your Values</h4>
                            <div class="value-list source-values">
                                ${sourceValues.map(v => `<span class="value-chip ${mismatches.includes(v) ? 'mismatch' : 'match'}">${v}</span>`).join('')}
                            </div>
                        </div>
                        <div class="values-section">
                            <h4>Allowed Options</h4>
                            <div class="value-list allowed-values">
                                ${allowedValues.map(v => `<span class="value-chip allowed">${v}</span>`).join('')}
                            </div>
                        </div>
                    </div>
                    
                    <div class="value-mapping-table">
                        <h4>Map Your Values:</h4>
                        <table>
                            <thead>
                                <tr>
                                    <th>Your Value</th>
                                    <th>→</th>
                                    <th>Maps To</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${sourceValues.map(sv => `
                                    <tr class="${mismatches.includes(sv) ? 'needs-mapping' : ''}">
                                        <td><code>${sv}</code></td>
                                        <td>→</td>
                                        <td>
                                            <select class="value-mapping-select" data-source="${sv}">
                                                <option value="">-- Select --</option>
                                                ${allowedValues.map(av => {
                                                    const isMatch = av.toLowerCase() === sv.toLowerCase();
                                                    return `<option value="${av}" ${isMatch ? 'selected' : ''}>${av}</option>`;
                                                }).join('')}
                                            </select>
                                        </td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="value-mapping-footer">
                    <button class="btn-secondary" onclick="ColumnMapper.closeValueMappingModal()">Cancel</button>
                    <button class="btn-primary" onclick="ColumnMapper.saveValueMappings('${targetField}')">✓ Apply Mappings</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        this.currentValueMappingField = targetField;
    },
    
    /**
     * Close value mapping modal
     */
    closeValueMappingModal() {
        const modal = document.querySelector('.value-mapping-modal');
        if (modal) modal.remove();
        this.currentValueMappingField = null;
    },
    
    /**
     * Save value mappings from modal
     */
    saveValueMappings(targetField) {
        const modal = document.querySelector('.value-mapping-modal');
        if (!modal) return;
        
        const mappings = {};
        modal.querySelectorAll('.value-mapping-select').forEach(select => {
            const sourceValue = select.dataset.source;
            const targetValue = select.value;
            if (targetValue) {
                mappings[sourceValue] = targetValue;
            }
        });
        
        this.valueMappings[targetField] = mappings;
        console.log('Value mappings saved:', targetField, mappings);
        
        this.closeValueMappingModal();
        this.updateMappingUI();
        
        // Show success notification
        const count = Object.keys(mappings).length;
        if (typeof showNotification === 'function') {
            showNotification(`Value mappings saved (${count} values mapped)`, 'success');
        }
    },
    
    /**
     * Apply value mappings to transform data
     */
    applyValueMapping(targetField, value) {
        const mappings = this.valueMappings[targetField];
        if (!mappings) return value;
        
        return mappings[value] || value;
    },
    
    /**
     * Get fields that have value mappings configured
     */
    getFieldsWithValueMappings() {
        return Object.keys(this.valueMappings).filter(k => 
            Object.keys(this.valueMappings[k]).length > 0
        );
    },

    /**
     * Clear all mappings
     */
    clearMappings() {
        this.mappings = {};
        this.valueMappings = {};
    },

    /**
     * Get unmapped source columns
     */
    getUnmappedSourceColumns() {
        const mappedSources = new Set(
            Object.values(this.mappings)
                .filter(m => m.sourceColumn)
                .map(m => m.sourceColumn)
        );
        return this.sourceColumns.filter(col => !mappedSources.has(col));
    },

    /**
     * Get unmapped required fields
     */
    getUnmappedRequiredFields() {
        const required = this.getRequiredFields();
        return required.filter(field => !this.mappings[field.name]);
    },

    /**
     * Get mapping statistics
     */
    getMappingStats() {
        const allFields = this.getAllSchemaFields();
        const required = this.getRequiredFields();
        const mapped = Object.keys(this.mappings).length;
        const unmappedRequired = this.getUnmappedRequiredFields().length;

        return {
            totalFields: allFields.length,
            totalRequired: required.length,
            mappedFields: mapped,
            unmappedFields: allFields.length - mapped,
            unmappedRequired: unmappedRequired,
            unmappedSource: this.getUnmappedSourceColumns().length,
            isValid: unmappedRequired === 0
        };
    },

    /**
     * Render source columns panel
     */
    renderSourceColumns(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = '';

        this.sourceColumns.forEach(column => {
            const stats = this.columnStats[column] || {};
            const mapping = Object.entries(this.mappings).find(
                ([_, m]) => m.sourceColumn === column
            );
            
            const div = document.createElement('div');
            div.className = `column-item ${mapping ? 'mapped' : ''}`;
            div.draggable = true;
            div.dataset.column = column;

            div.innerHTML = `
                <div>
                    <div class="column-name">${column}</div>
                    <div class="column-sample">${stats.sampleValues ? stats.sampleValues[0] || '' : ''}</div>
                </div>
                ${mapping ? `<div class="column-mapping-target">→ ${mapping[0]}</div>` : ''}
            `;

            // Drag events
            div.addEventListener('dragstart', (e) => {
                e.dataTransfer.setData('text/plain', column);
                div.classList.add('dragging');
            });

            div.addEventListener('dragend', () => {
                div.classList.remove('dragging');
            });

            container.appendChild(div);
        });
    },

    /**
     * Render schema fields panel
     */
    renderSchemaFields(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = '';

        if (!this.schema) {
            container.innerHTML = '<p>Loading schema...</p>';
            return;
        }

        Object.entries(this.schema.columns).forEach(([category, categoryData]) => {
            const categoryDiv = document.createElement('div');
            categoryDiv.className = 'schema-category';

            const headerDiv = document.createElement('div');
            headerDiv.className = 'category-header';
            headerDiv.innerHTML = `
                <span>${this.capitalize(category)}</span>
                <span class="category-toggle">▼</span>
            `;
            headerDiv.addEventListener('click', () => {
                const fields = categoryDiv.querySelector('.category-fields');
                fields.classList.toggle('collapsed');
                headerDiv.querySelector('.category-toggle').textContent = 
                    fields.classList.contains('collapsed') ? '▶' : '▼';
            });

            const fieldsDiv = document.createElement('div');
            fieldsDiv.className = 'category-fields';

            categoryData.fields.forEach(field => {
                const mapping = this.mappings[field.name];
                const fieldDiv = document.createElement('div');
                fieldDiv.className = `schema-field ${field.required ? 'required' : ''} ${mapping ? 'mapped' : ''}`;
                fieldDiv.dataset.field = field.name;

                // Create dropdown for mapping
                const options = ['', ...this.sourceColumns].map(col => {
                    const selected = mapping && mapping.sourceColumn === col ? 'selected' : '';
                    return `<option value="${col}" ${selected}>${col || '-- Select --'}</option>`;
                }).join('');

                fieldDiv.innerHTML = `
                    <div class="field-info">
                        <span class="field-name">${field.name}</span>
                        <span class="field-type">${field.type}${field.required ? ' • Required' : ''}</span>
                    </div>
                    <div class="field-mapping">
                        <select class="mapping-select" data-target="${field.name}">
                            ${options}
                        </select>
                        ${field.required ? '<span class="required-badge">REQ</span>' : ''}
                    </div>
                `;

                // Handle mapping selection
                const select = fieldDiv.querySelector('select');
                select.addEventListener('change', (e) => {
                    this.setMapping(field.name, e.target.value, field.transformation);
                    this.updateMappingUI();
                });

                // Handle drop
                fieldDiv.addEventListener('dragover', (e) => {
                    e.preventDefault();
                    fieldDiv.style.background = 'var(--walmart-blue-lightest)';
                });

                fieldDiv.addEventListener('dragleave', () => {
                    fieldDiv.style.background = '';
                });

                fieldDiv.addEventListener('drop', (e) => {
                    e.preventDefault();
                    fieldDiv.style.background = '';
                    const sourceColumn = e.dataTransfer.getData('text/plain');
                    this.setMapping(field.name, sourceColumn, field.transformation);
                    this.updateMappingUI();
                });

                fieldsDiv.appendChild(fieldDiv);
            });

            categoryDiv.appendChild(headerDiv);
            categoryDiv.appendChild(fieldsDiv);
            container.appendChild(categoryDiv);
        });
    },

    /**
     * Update UI after mapping changes
     */
    updateMappingUI() {
        // Refresh source columns
        this.renderSourceColumns('source-columns');

        // Update schema field dropdowns and states
        document.querySelectorAll('.schema-field').forEach(field => {
            const fieldName = field.dataset.field;
            const mapping = this.mappings[fieldName];
            const select = field.querySelector('select');

            if (select) {
                select.value = mapping ? mapping.sourceColumn : '';
            }

            if (mapping) {
                field.classList.add('mapped');
            } else {
                field.classList.remove('mapped');
            }
        });

        // Update stats
        this.updateStats();
    },

    /**
     * Update mapping statistics display
     */
    updateStats() {
        const stats = this.getMappingStats();

        const mappedEl = document.getElementById('mapped-count');
        const unmappedEl = document.getElementById('unmapped-count');
        const requiredEl = document.getElementById('required-count');

        if (mappedEl) mappedEl.textContent = stats.mappedFields;
        if (unmappedEl) unmappedEl.textContent = stats.unmappedSource;
        if (requiredEl) requiredEl.textContent = stats.unmappedRequired;
    },

    /**
     * Capitalize first letter
     */
    capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    },

    /**
     * Export current mappings
     */
    exportMappings() {
        return {
            sourceName: FileParser.fileName || 'Unknown',
            created: new Date().toISOString(),
            mappings: this.mappings,
            unmappedSource: this.getUnmappedSourceColumns(),
            stats: this.getMappingStats()
        };
    },

    /**
     * Import saved mappings
     */
    importMappings(savedMappings) {
        if (savedMappings && savedMappings.mappings) {
            this.mappings = savedMappings.mappings;
            this.updateMappingUI();
        }
    },

    /**
     * Fallback schema if file not accessible
     */
    getFallbackSchema() {
        return {
            columns: {
                identifiers: {
                    description: "Unique identifiers for projects and records",
                    fields: [
                        { name: "project_id", type: "string", required: true, aliases: ["PROJECT_ID", "ProjectId", "id"] },
                        { name: "intake_card", type: "string", required: false, aliases: ["Intake_Card", "IntakeCard"] },
                        { name: "title", type: "string", required: true, aliases: ["PROJECT_TITLE", "Title", "name"] }
                    ]
                },
                status: {
                    description: "Project status and health indicators",
                    fields: [
                        { name: "status", type: "string", required: true, aliases: ["Status", "PROJECT_STATUS"], validation: { enum: ["Active", "Archived", "Pending", "Cancelled", "Complete"] } },
                        { name: "phase", type: "string", required: false, aliases: ["Phase", "PROJECT_PHASE"], validation: { enum: ["Vet", "Test", "Test Markets", "Roll/Deploy", "Complete", "Pending", "Planning"] } },
                        { name: "health", type: "string", required: false, aliases: ["Health", "PROJECT_HEALTH"], validation: { enum: ["On Track", "Off Track", "At Risk", "Continuous"] } },
                        { name: "project_source", type: "string", required: true, autoPopulate: true, aliases: ["Project_Source", "source"], validation: { enum: ["Operations", "Realty", "Intake Hub", "Manual Upload", "API"] } }
                    ]
                },
                location: {
                    description: "Geographic and organizational location data",
                    fields: [
                        { name: "division", type: "string", required: false, aliases: ["Division", "DIVISION"], validation: { enum: ["EAST", "WEST", "NORTH", "SOUTH", "SOUTHEAST", "SOUTHWEST", "NHM", "SAM"] } },
                        { name: "region", type: "string", required: false, aliases: ["Region", "REGION"] },
                        { name: "market", type: "string", required: false, aliases: ["Market", "MARKET"], transformation: "normalize_market_3digit" },
                        { name: "facility", type: "integer", required: false, aliases: ["Facility", "store_number", "Store"] },
                        { name: "city", type: "string", required: false, aliases: ["City", "CITY"] },
                        { name: "state", type: "string", required: false, aliases: ["State", "STATE"] }
                    ]
                },
                time: {
                    description: "Dates, timestamps, and calendar references",
                    fields: [
                        { name: "created_date", type: "datetime", required: true, aliases: ["CREATED_TS", "created_at"], transformation: "to_iso8601" },
                        { name: "last_updated", type: "datetime", required: true, aliases: ["Last_Updated", "updated_at"], transformation: "to_iso8601" },
                        { name: "wm_week", type: "integer", required: false, aliases: ["WM_Week", "walmart_week"] },
                        { name: "fiscal_year", type: "integer", required: false, aliases: ["FY", "fiscal_year"] }
                    ]
                },
                ownership: {
                    description: "Project ownership and personnel",
                    fields: [
                        { name: "owner", type: "string", required: false, aliases: ["Owner", "PROJECT_OWNER"] },
                        { name: "director", type: "string", required: false, aliases: ["Director", "DIRECTOR"] },
                        { name: "sr_director", type: "string", required: false, aliases: ["SR_Director", "senior_director"] }
                    ]
                },
                categorization: {
                    description: "Project type and classification fields",
                    fields: [
                        { name: "project_type", type: "string", required: false, aliases: ["Project_Type", "type"] },
                        { name: "initiative_type", type: "string", required: false, aliases: ["Initiative_Type", "initiative"] },
                        { name: "business_type", type: "string", required: false, aliases: ["Business_Type"] }
                    ]
                },
                description: {
                    description: "Project descriptions and summaries",
                    fields: [
                        { name: "summary", type: "string", required: false, aliases: ["PRESENTATION_SUMMARY", "summary"] },
                        { name: "overview", type: "string", required: false, aliases: ["OVERVIEW", "description"] }
                    ]
                }
            }
        };
    }
};
