/**
 * Projects Validator - Schema-based Validation
 * 
 * Uses the Projects Schema from Admin/Data-Bridge/Schemas/projects-schema.json
 * to validate project data before storage
 */

const fs = require('fs');
const path = require('path');

class ProjectsValidator {
  constructor(schemaPath = '../../../Interface/Admin/Data-Bridge/Schemas/projects-schema.json') {
    try {
      const fullPath = path.resolve(__dirname, schemaPath);
      this.schema = JSON.parse(fs.readFileSync(fullPath, 'utf8'));
      this.requiredFields = this.extractRequiredFields();
    } catch (error) {
      console.error('Failed to load projects schema:', error.message);
      this.schema = null;
      this.requiredFields = [];
    }
  }

  /**
   * Extract all required fields from schema
   */
  extractRequiredFields() {
    if (!this.schema || !this.schema.columns) {
      return [];
    }

    const required = [];
    Object.values(this.schema.columns).forEach(category => {
      if (category.fields) {
        category.fields.forEach(field => {
          if (field.required) {
            required.push(field.name);
          }
        });
      }
    });

    return required;
  }

  /**
   * Get field definition from schema
   */
  getFieldDefinition(fieldName) {
    if (!this.schema || !this.schema.columns) {
      return null;
    }

    for (const category of Object.values(this.schema.columns)) {
      if (category.fields) {
        const field = category.fields.find(f => f.name === fieldName);
        if (field) {
          return field;
        }
      }
    }

    return null;
  }

  /**
   * Validate single field
   */
  validateField(fieldName, value) {
    const field = this.getFieldDefinition(fieldName);

    if (!field) {
      return { valid: true, warning: `Field ${fieldName} not recognized in schema` };
    }

    // Check required
    if (field.required && (value === null || value === undefined || value === '')) {
      return { valid: false, error: `${fieldName} is required` };
    }

    // Check type
    if (value !== null && value !== undefined && value !== '') {
      const typeError = this.checkType(value, field.type);
      if (typeError) {
        return { valid: false, error: typeError };
      }

      // Check enum if present
      if (field.validation && field.validation.enum) {
        if (!field.validation.enum.includes(value)) {
          return {
            valid: false,
            error: `${fieldName} must be one of: ${field.validation.enum.join(', ')}`
          };
        }
      }

      // Check length constraints
      if (field.type === 'string' && field.validation) {
        if (field.validation.minLength && value.length < field.validation.minLength) {
          return { valid: false, error: `${fieldName} must be at least ${field.validation.minLength} characters` };
        }
        if (field.validation.maxLength && value.length > field.validation.maxLength) {
          return { valid: false, error: `${fieldName} must be at most ${field.validation.maxLength} characters` };
        }
        if (field.validation.pattern) {
          const regex = new RegExp(field.validation.pattern);
          if (!regex.test(value)) {
            return { valid: false, error: `${fieldName} format is invalid (pattern: ${field.validation.pattern})` };
          }
        }
      }

      // Check numeric constraints
      if ((field.type === 'integer' || field.type === 'float') && field.validation) {
        const numValue = parseFloat(value);
        if (field.validation.minimum !== undefined && numValue < field.validation.minimum) {
          return { valid: false, error: `${fieldName} must be at least ${field.validation.minimum}` };
        }
        if (field.validation.maximum !== undefined && numValue > field.validation.maximum) {
          return { valid: false, error: `${fieldName} must be at most ${field.validation.maximum}` };
        }
      }
    }

    return { valid: true };
  }

  /**
   * Check if value matches expected type
   */
  checkType(value, expectedType) {
    const typeMap = {
      'string': 'string',
      'integer': 'number',
      'float': 'number',
      'boolean': 'boolean',
      'date': 'string',
      'datetime': 'string',
      'array': 'object',
      'object': 'object'
    };

    const jsType = typeof value;
    const expectedJsType = typeMap[expectedType];

    if (jsType !== expectedJsType) {
      // Allow string representations
      if (expectedType === 'integer') {
        if (!Number.isInteger(parseInt(value))) {
          return `${expectedType} expected`;
        }
      } else if (expectedType === 'float') {
        if (isNaN(parseFloat(value))) {
          return `${expectedType} expected`;
        }
      } else if (expectedType === 'date' || expectedType === 'datetime') {
        if (isNaN(Date.parse(value))) {
          return `Valid ${expectedType} expected`;
        }
      }
    }

    return null;
  }

  /**
   * Validate entire project object
   */
  validateProject(projectData, isCreating = true) {
    const errors = [];
    const warnings = [];

    if (!projectData || typeof projectData !== 'object') {
      return {
        valid: false,
        errors: ['Project data must be an object']
      };
    }

    // Check required fields
    for (const requiredField of this.requiredFields) {
      if (!(requiredField in projectData) || projectData[requiredField] === null || projectData[requiredField] === undefined) {
        errors.push(`Missing required field: ${requiredField}`);
      }
    }

    // Validate individual fields
    for (const [fieldName, value] of Object.entries(projectData)) {
      const result = this.validateField(fieldName, value);
      
      if (!result.valid) {
        errors.push(result.error);
      } else if (result.warning) {
        warnings.push(result.warning);
      }
    }

    return {
      valid: errors.length === 0,
      errors,
      warnings
    };
  }

  /**
   * Get schema information for UI form generation
   */
  getSchemaInfo() {
    if (!this.schema) {
      return null;
    }

    return {
      title: this.schema.title,
      description: this.schema.description,
      columns: this.schema.columns,
      metadata: this.schema.metadata
    };
  }

  /**
   * Get fields by category for form rendering
   */
  getFieldsByCategory() {
    if (!this.schema || !this.schema.columns) {
      return {};
    }

    const result = {};
    for (const [categoryName, categoryData] of Object.entries(this.schema.columns)) {
      result[categoryName] = {
        description: categoryData.description,
        fields: categoryData.fields || []
      };
    }

    return result;
  }
}

module.exports = ProjectsValidator;
