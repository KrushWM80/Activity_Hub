/**
 * Data Validator
 * Client-side validation against the schema
 */

const DataValidator = {
    schema: null,
    validationResults: null,

    /**
     * Initialize with schema
     */
    async init() {
        // Use schema from ColumnMapper if available
        if (ColumnMapper.schema) {
            this.schema = ColumnMapper.schema;
        }
        return this;
    },

    /**
     * Validate a single value against field definition
     */
    validateField(value, fieldDef) {
        const errors = [];
        const warnings = [];

        // Check required
        if (fieldDef.required && (value === null || value === undefined || value === '')) {
            errors.push(`${fieldDef.name} is required`);
            return { valid: false, errors, warnings };
        }

        // Skip further validation if empty and not required
        if (value === null || value === undefined || value === '') {
            return { valid: true, errors: [], warnings: [] };
        }

        // Type validation
        const typeResult = this.validateType(value, fieldDef);
        if (typeResult.error) errors.push(typeResult.error);
        if (typeResult.warning) warnings.push(typeResult.warning);

        // Custom validation rules
        if (fieldDef.validation) {
            const validationResults = this.applyValidation(value, fieldDef.validation, fieldDef.name);
            errors.push(...validationResults.errors);
            warnings.push(...validationResults.warnings);
        }

        return { valid: errors.length === 0, errors, warnings };
    },

    /**
     * Validate value type
     */
    validateType(value, fieldDef) {
        const type = fieldDef.type;
        const name = fieldDef.name;

        switch (type) {
            case 'string':
                if (typeof value !== 'string' && value !== null) {
                    return { warning: `${name} will be converted to string` };
                }
                break;

            case 'integer':
                const intVal = parseInt(value, 10);
                if (isNaN(intVal)) {
                    return { error: `${name} must be a valid integer` };
                }
                if (!Number.isInteger(Number(value))) {
                    return { warning: `${name} will be rounded to integer` };
                }
                break;

            case 'float':
                if (isNaN(parseFloat(value))) {
                    return { error: `${name} must be a valid number` };
                }
                break;

            case 'boolean':
                const boolStr = String(value).toLowerCase();
                if (!['true', 'false', '1', '0', 'yes', 'no', 'y', 'n'].includes(boolStr)) {
                    return { error: `${name} must be a boolean value` };
                }
                break;

            case 'date':
            case 'datetime':
                const date = new Date(value);
                if (isNaN(date.getTime())) {
                    return { error: `${name} must be a valid date` };
                }
                break;
        }

        return {};
    },

    /**
     * Apply validation rules from schema
     */
    applyValidation(value, validation, fieldName) {
        const errors = [];
        const warnings = [];

        // Enum validation
        if (validation.enum) {
            const normalizedValue = String(value).trim();
            const normalizedEnum = validation.enum.map(e => String(e).toLowerCase());
            
            if (!normalizedEnum.includes(normalizedValue.toLowerCase())) {
                warnings.push(`${fieldName} value "${value}" not in expected values: ${validation.enum.join(', ')}`);
            }
        }

        // Pattern (regex) validation
        if (validation.pattern) {
            const regex = new RegExp(validation.pattern);
            if (!regex.test(String(value))) {
                errors.push(`${fieldName} does not match required format`);
            }
        }

        // String length validation
        if (validation.minLength !== undefined && String(value).length < validation.minLength) {
            errors.push(`${fieldName} must be at least ${validation.minLength} characters`);
        }
        if (validation.maxLength !== undefined && String(value).length > validation.maxLength) {
            warnings.push(`${fieldName} exceeds ${validation.maxLength} characters and may be truncated`);
        }

        // Numeric range validation
        if (validation.minimum !== undefined && Number(value) < validation.minimum) {
            errors.push(`${fieldName} must be at least ${validation.minimum}`);
        }
        if (validation.maximum !== undefined && Number(value) > validation.maximum) {
            errors.push(`${fieldName} must not exceed ${validation.maximum}`);
        }

        return { errors, warnings };
    },

    /**
     * Validate a single record
     */
    validateRecord(record, mappings) {
        const errors = {};
        const warnings = {};
        let hasErrors = false;
        let hasWarnings = false;

        const allFields = ColumnMapper.getAllSchemaFields();

        allFields.forEach(field => {
            const mapping = mappings[field.name];
            let value = null;

            if (mapping && mapping.sourceColumn) {
                value = record[mapping.sourceColumn];
            }

            const result = this.validateField(value, field);

            if (result.errors.length > 0) {
                errors[field.name] = result.errors;
                hasErrors = true;
            }

            if (result.warnings.length > 0) {
                warnings[field.name] = result.warnings;
                hasWarnings = true;
            }
        });

        return { valid: !hasErrors, hasWarnings, errors, warnings };
    },

    /**
     * Validate all records
     */
    validateAll(records, mappings) {
        const results = {
            totalRecords: records.length,
            validRecords: 0,
            invalidRecords: 0,
            warningRecords: 0,
            recordResults: [],
            errorSummary: {},
            warningSummary: {}
        };

        records.forEach((record, index) => {
            const result = this.validateRecord(record, mappings);
            result.rowIndex = index;
            result.originalRecord = record;

            if (result.valid) {
                results.validRecords++;
            } else {
                results.invalidRecords++;
            }

            if (result.hasWarnings) {
                results.warningRecords++;
            }

            // Aggregate errors by field
            Object.entries(result.errors).forEach(([field, fieldErrors]) => {
                if (!results.errorSummary[field]) {
                    results.errorSummary[field] = { count: 0, messages: new Set() };
                }
                results.errorSummary[field].count++;
                fieldErrors.forEach(msg => results.errorSummary[field].messages.add(msg));
            });

            // Aggregate warnings by field
            Object.entries(result.warnings).forEach(([field, fieldWarnings]) => {
                if (!results.warningSummary[field]) {
                    results.warningSummary[field] = { count: 0, messages: new Set() };
                }
                results.warningSummary[field].count++;
                fieldWarnings.forEach(msg => results.warningSummary[field].messages.add(msg));
            });

            results.recordResults.push(result);
        });

        this.validationResults = results;
        return results;
    },

    /**
     * Render validation summary
     */
    renderValidationSummary() {
        if (!this.validationResults) return;

        const results = this.validationResults;

        // Update stat numbers
        document.getElementById('valid-count').textContent = results.validRecords;
        document.getElementById('warning-count').textContent = results.warningRecords;
        document.getElementById('error-count').textContent = results.invalidRecords;

        // Render error panel if there are errors
        const errorsPanel = document.getElementById('errors-panel');
        const errorList = document.getElementById('error-list');

        if (results.invalidRecords > 0 || results.warningRecords > 0) {
            errorsPanel.classList.remove('hidden');
            errorList.innerHTML = '';

            // Show errors
            Object.entries(results.errorSummary).forEach(([field, data]) => {
                const div = document.createElement('div');
                div.className = 'error-item';
                div.innerHTML = `
                    <strong>${field}</strong>: ${data.count} error(s)
                    <br><small>${[...data.messages].join('; ')}</small>
                `;
                errorList.appendChild(div);
            });

            // Show warnings
            Object.entries(results.warningSummary).forEach(([field, data]) => {
                const div = document.createElement('div');
                div.className = 'error-item';
                div.style.background = 'var(--warning-light)';
                div.innerHTML = `
                    <strong>${field}</strong>: ${data.count} warning(s)
                    <br><small>${[...data.messages].join('; ')}</small>
                `;
                errorList.appendChild(div);
            });
        } else {
            errorsPanel.classList.add('hidden');
        }
    },

    /**
     * Render validation table
     */
    renderValidationTable(filter = 'all') {
        if (!this.validationResults) return;

        const results = this.validationResults;
        const headerEl = document.getElementById('validation-header');
        const bodyEl = document.getElementById('validation-body');

        // Get mapped columns for display
        const displayColumns = Object.entries(ColumnMapper.mappings)
            .filter(([_, m]) => m.sourceColumn)
            .map(([target, m]) => ({ target, source: m.sourceColumn }));

        // Render header
        headerEl.innerHTML = `
            <tr>
                <th>Row</th>
                <th>Status</th>
                ${displayColumns.slice(0, 6).map(c => `<th>${c.target}</th>`).join('')}
            </tr>
        `;

        // Filter records
        let recordsToShow = results.recordResults;
        if (filter === 'errors') {
            recordsToShow = recordsToShow.filter(r => !r.valid);
        } else if (filter === 'warnings') {
            recordsToShow = recordsToShow.filter(r => r.hasWarnings);
        }

        // Limit display to 100 rows for performance
        recordsToShow = recordsToShow.slice(0, 100);

        // Render body
        bodyEl.innerHTML = recordsToShow.map(result => {
            const rowClass = !result.valid ? 'has-error' : result.hasWarnings ? 'has-warning' : '';
            const status = !result.valid ? '❌ Error' : result.hasWarnings ? '⚠️ Warning' : '✅ Valid';

            const cells = displayColumns.slice(0, 6).map(c => {
                const value = result.originalRecord[c.source] || '';
                const hasError = result.errors[c.target];
                const hasWarning = result.warnings[c.target];
                const cellClass = hasError ? 'has-error' : hasWarning ? 'has-warning' : '';
                return `<td class="${cellClass}" title="${hasError ? result.errors[c.target].join(', ') : ''}">${value}</td>`;
            }).join('');

            return `
                <tr class="${rowClass}">
                    <td>${result.rowIndex + 1}</td>
                    <td>${status}</td>
                    ${cells}
                </tr>
            `;
        }).join('');
    },

    /**
     * Get valid records only
     */
    getValidRecords() {
        if (!this.validationResults) return [];
        return this.validationResults.recordResults
            .filter(r => r.valid)
            .map(r => r.originalRecord);
    },

    /**
     * Check if all required fields are mapped
     */
    checkRequiredMappings(mappings) {
        const unmapped = ColumnMapper.getUnmappedRequiredFields();
        return {
            valid: unmapped.length === 0,
            unmappedFields: unmapped.map(f => f.name)
        };
    }
};
