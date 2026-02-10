/**
 * Data Bridge Transformations
 * 
 * Transformation functions for normalizing data from various sources
 * to match the canonical schema definitions.
 * 
 * These transformations are referenced in mapping files and executed
 * during data ingestion.
 */

const DataBridgeTransformations = {
    
    /**
     * Type Conversions
     */
    to_integer: (value) => {
        if (value === null || value === undefined || value === '') return null;
        const parsed = parseInt(value, 10);
        return isNaN(parsed) ? null : parsed;
    },

    to_float: (value) => {
        if (value === null || value === undefined || value === '') return null;
        const parsed = parseFloat(value);
        return isNaN(parsed) ? null : parsed;
    },

    to_string: (value) => {
        if (value === null || value === undefined) return null;
        return String(value).trim();
    },

    to_boolean: (value) => {
        if (value === null || value === undefined) return null;
        if (typeof value === 'boolean') return value;
        const str = String(value).toLowerCase().trim();
        if (['true', 'yes', '1', 'y'].includes(str)) return true;
        if (['false', 'no', '0', 'n'].includes(str)) return false;
        return null;
    },

    /**
     * Date/Time Conversions
     */
    to_date: (value) => {
        if (!value) return null;
        try {
            const date = new Date(value);
            if (isNaN(date.getTime())) return null;
            return date.toISOString().split('T')[0]; // YYYY-MM-DD
        } catch {
            return null;
        }
    },

    to_iso8601: (value) => {
        if (!value) return null;
        try {
            const date = new Date(value);
            if (isNaN(date.getTime())) return null;
            return date.toISOString();
        } catch {
            return null;
        }
    },

    /**
     * String Transformations
     */
    uppercase: (value) => {
        if (!value) return null;
        return String(value).toUpperCase().trim();
    },

    lowercase: (value) => {
        if (!value) return null;
        return String(value).toLowerCase().trim();
    },

    trim: (value) => {
        if (!value) return null;
        return String(value).trim();
    },

    /**
     * Business-Specific Transformations
     */
    normalize_market_3digit: (value) => {
        // Normalize market to 3-digit format with leading zeros
        // Examples: 8 → "008", 45 → "045", 101 → "101"
        if (value === null || value === undefined || value === '') return null;
        const num = parseInt(value, 10);
        if (isNaN(num)) return null;
        return String(num).padStart(3, '0');
    },

    normalize_division: (value) => {
        // Normalize division to uppercase standard format
        if (!value) return null;
        const divisions = ['EAST', 'WEST', 'NORTH', 'SOUTH', 'SOUTHEAST', 'SOUTHWEST', 'NHM', 'SAM'];
        const normalized = String(value).toUpperCase().trim();
        return divisions.includes(normalized) ? normalized : normalized;
    },

    normalize_status: (value) => {
        // Normalize status values to standard format
        if (!value) return null;
        const str = String(value).toLowerCase().trim();
        const statusMap = {
            'active': 'Active',
            'archived': 'Archived',
            'pending': 'Pending',
            'cancelled': 'Cancelled',
            'canceled': 'Cancelled',
            'complete': 'Complete',
            'completed': 'Complete'
        };
        return statusMap[str] || value;
    },

    normalize_phase: (value) => {
        // Normalize project phase values
        if (!value) return null;
        const str = String(value).toLowerCase().trim();
        const phaseMap = {
            'poc': 'POC/POT',
            'pot': 'POC/POT',
            'poc/pot': 'POC/POT',
            'test': 'Test',
            'testing': 'Test',
            'mkt scale': 'Mkt Scale',
            'market scale': 'Mkt Scale',
            'roll': 'Roll/Deploy',
            'deploy': 'Roll/Deploy',
            'roll/deploy': 'Roll/Deploy',
            'rollout': 'Roll/Deploy',
            'complete': 'Complete',
            'completed': 'Complete',
            'pending': 'Pending',
            'planning': 'Planning'
        };
        return phaseMap[str] || value;
    },

    /**
     * Intake Hub Specific Transformations
     */
    resolve_project_id: (record) => {
        // Priority: PROJECT_ID → Intake_Card → 'R-' + Facility (for Realty)
        if (record.PROJECT_ID) return String(record.PROJECT_ID);
        if (record.Intake_Card) return String(record.Intake_Card);
        if (record.Facility) return `R-${record.Facility}`;
        return null;
    },

    resolve_title: (record) => {
        // Priority: PROJECT_TITLE → Title → Project_Type + Initiative_Type → 'Untitled'
        if (record.PROJECT_TITLE) return String(record.PROJECT_TITLE).trim();
        if (record.Title) return String(record.Title).trim();
        if (record.Project_Type && record.Initiative_Type) {
            return `${record.Project_Type} - ${record.Initiative_Type}`;
        }
        if (record.Initiative_Type) return String(record.Initiative_Type).trim();
        return 'Untitled';
    },

    /**
     * Apply a transformation by name
     */
    apply: function(transformationName, value, record = null) {
        if (!transformationName) return value;
        
        const fn = this[transformationName];
        if (!fn) {
            console.warn(`Unknown transformation: ${transformationName}`);
            return value;
        }

        // Some transformations need the full record context
        if (['resolve_project_id', 'resolve_title'].includes(transformationName)) {
            return fn(record || { [transformationName]: value });
        }
        
        return fn(value);
    },

    /**
     * Apply value mapping (enum translation)
     */
    applyValueMapping: function(value, valueMapping) {
        if (!valueMapping || !value) return value;
        return valueMapping[value] || valueMapping[String(value)] || value;
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DataBridgeTransformations;
}
