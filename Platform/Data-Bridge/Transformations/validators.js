/**
 * Data Bridge Validators
 * 
 * Validation functions for ensuring data conforms to schema requirements.
 * Used during data ingestion to validate records before import.
 */

const DataBridgeValidators = {

    /**
     * Validate a value against a schema field definition
     * 
     * @param {*} value - The value to validate
     * @param {Object} fieldDef - The field definition from the schema
     * @returns {Object} - { valid: boolean, errors: string[] }
     */
    validateField: function(value, fieldDef) {
        const errors = [];
        const { name, type, required, validation } = fieldDef;

        // Check required
        if (required && (value === null || value === undefined || value === '')) {
            errors.push(`${name} is required`);
            return { valid: false, errors };
        }

        // Skip further validation if value is empty and not required
        if (value === null || value === undefined || value === '') {
            return { valid: true, errors: [] };
        }

        // Type validation
        const typeError = this.validateType(value, type, name);
        if (typeError) errors.push(typeError);

        // Custom validation rules
        if (validation) {
            const validationErrors = this.applyValidation(value, validation, name);
            errors.push(...validationErrors);
        }

        return { valid: errors.length === 0, errors };
    },

    /**
     * Validate value type
     */
    validateType: function(value, type, fieldName) {
        switch (type) {
            case 'string':
                if (typeof value !== 'string') {
                    return `${fieldName} must be a string`;
                }
                break;
            case 'integer':
                if (!Number.isInteger(Number(value))) {
                    return `${fieldName} must be an integer`;
                }
                break;
            case 'float':
                if (isNaN(parseFloat(value))) {
                    return `${fieldName} must be a number`;
                }
                break;
            case 'boolean':
                const boolStr = String(value).toLowerCase();
                if (!['true', 'false', '1', '0', 'yes', 'no'].includes(boolStr)) {
                    return `${fieldName} must be a boolean`;
                }
                break;
            case 'date':
            case 'datetime':
                const date = new Date(value);
                if (isNaN(date.getTime())) {
                    return `${fieldName} must be a valid date`;
                }
                break;
        }
        return null;
    },

    /**
     * Apply validation rules from schema
     */
    applyValidation: function(value, validation, fieldName) {
        const errors = [];

        // Enum validation
        if (validation.enum && !validation.enum.includes(value)) {
            errors.push(`${fieldName} must be one of: ${validation.enum.join(', ')}`);
        }

        // Pattern (regex) validation
        if (validation.pattern) {
            const regex = new RegExp(validation.pattern);
            if (!regex.test(String(value))) {
                errors.push(`${fieldName} does not match required pattern: ${validation.pattern}`);
            }
        }

        // String length validation
        if (validation.minLength !== undefined && String(value).length < validation.minLength) {
            errors.push(`${fieldName} must be at least ${validation.minLength} characters`);
        }
        if (validation.maxLength !== undefined && String(value).length > validation.maxLength) {
            errors.push(`${fieldName} must not exceed ${validation.maxLength} characters`);
        }

        // Numeric range validation
        if (validation.minimum !== undefined && Number(value) < validation.minimum) {
            errors.push(`${fieldName} must be at least ${validation.minimum}`);
        }
        if (validation.maximum !== undefined && Number(value) > validation.maximum) {
            errors.push(`${fieldName} must not exceed ${validation.maximum}`);
        }

        return errors;
    },

    /**
     * Validate an entire record against a schema
     * 
     * @param {Object} record - The data record to validate
     * @param {Object} schema - The schema definition
     * @returns {Object} - { valid: boolean, errors: { fieldName: string[] } }
     */
    validateRecord: function(record, schema) {
        const allErrors = {};
        let hasErrors = false;

        // Iterate through all schema categories
        for (const category of Object.values(schema.columns)) {
            for (const fieldDef of category.fields) {
                const value = record[fieldDef.name];
                const result = this.validateField(value, fieldDef);
                
                if (!result.valid) {
                    allErrors[fieldDef.name] = result.errors;
                    hasErrors = true;
                }
            }
        }

        return { valid: !hasErrors, errors: allErrors };
    },

    /**
     * Validate a batch of records
     * 
     * @param {Array} records - Array of records to validate
     * @param {Object} schema - The schema definition
     * @returns {Object} - { valid: number, invalid: number, errors: Array }
     */
    validateBatch: function(records, schema) {
        const results = {
            valid: 0,
            invalid: 0,
            errors: []
        };

        records.forEach((record, index) => {
            const result = this.validateRecord(record, schema);
            if (result.valid) {
                results.valid++;
            } else {
                results.invalid++;
                results.errors.push({
                    rowIndex: index,
                    errors: result.errors
                });
            }
        });

        return results;
    },

    /**
     * Get summary of required fields from schema
     */
    getRequiredFields: function(schema) {
        const required = [];
        for (const category of Object.values(schema.columns)) {
            for (const fieldDef of category.fields) {
                if (fieldDef.required) {
                    required.push({
                        name: fieldDef.name,
                        type: fieldDef.type,
                        description: fieldDef.description
                    });
                }
            }
        }
        return required;
    },

    /**
     * Find matching alias for a source column name
     */
    findColumnByAlias: function(sourceColumnName, schema) {
        for (const category of Object.values(schema.columns)) {
            for (const fieldDef of category.fields) {
                if (fieldDef.name === sourceColumnName) {
                    return fieldDef;
                }
                if (fieldDef.aliases && fieldDef.aliases.includes(sourceColumnName)) {
                    return fieldDef;
                }
            }
        }
        return null;
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DataBridgeValidators;
}
