/**
 * File Parser
 * Handles parsing of Excel (.xlsx, .xls) and CSV files using SheetJS
 */

const FileParser = {
    supportedFormats: ['.xlsx', '.xls', '.csv'],
    parsedData: null,
    headers: [],
    rows: [],
    fileName: '',
    fileSize: 0,

    /**
     * Parse a file
     * @param {File} file - The file to parse
     * @returns {Promise<Object>} - Parsed data with headers and rows
     */
    async parseFile(file) {
        this.fileName = file.name;
        this.fileSize = file.size;

        const extension = this.getFileExtension(file.name);
        
        if (!this.supportedFormats.includes(extension)) {
            throw new Error(`Unsupported file format: ${extension}. Supported formats: ${this.supportedFormats.join(', ')}`);
        }

        const data = await this.readFile(file);
        
        if (extension === '.csv') {
            return this.parseCSV(data);
        } else {
            return this.parseExcel(data);
        }
    },

    /**
     * Read file as ArrayBuffer
     */
    readFile(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = () => reject(new Error('Failed to read file'));
            reader.readAsArrayBuffer(file);
        });
    },

    /**
     * Get file extension
     */
    getFileExtension(filename) {
        return filename.substring(filename.lastIndexOf('.')).toLowerCase();
    },

    /**
     * Parse Excel file using SheetJS
     */
    parseExcel(data) {
        try {
            // Parse workbook
            const workbook = XLSX.read(data, { type: 'array', cellDates: true });
            
            // Get first sheet
            const sheetName = workbook.SheetNames[0];
            const worksheet = workbook.Sheets[sheetName];
            
            // Convert to JSON with headers
            const jsonData = XLSX.utils.sheet_to_json(worksheet, { 
                header: 1,
                raw: false,
                dateNF: 'yyyy-mm-dd'
            });

            if (jsonData.length === 0) {
                throw new Error('The file appears to be empty');
            }

            // First row is headers
            this.headers = jsonData[0].map((h, i) => h ? String(h).trim() : `Column_${i + 1}`);
            
            // Rest are data rows
            this.rows = jsonData.slice(1).map(row => {
                const obj = {};
                this.headers.forEach((header, index) => {
                    obj[header] = row[index] !== undefined ? row[index] : null;
                });
                return obj;
            });

            // Filter out completely empty rows
            this.rows = this.rows.filter(row => 
                Object.values(row).some(val => val !== null && val !== '')
            );

            this.parsedData = {
                headers: this.headers,
                rows: this.rows,
                rowCount: this.rows.length,
                columnCount: this.headers.length,
                fileName: this.fileName,
                fileSize: this.fileSize,
                sheetName: sheetName,
                allSheets: workbook.SheetNames
            };

            return this.parsedData;
        } catch (error) {
            throw new Error(`Failed to parse Excel file: ${error.message}`);
        }
    },

    /**
     * Parse CSV data
     */
    parseCSV(data) {
        try {
            // Use SheetJS to parse CSV as well (handles various CSV formats)
            const workbook = XLSX.read(data, { type: 'array' });
            const sheetName = workbook.SheetNames[0];
            const worksheet = workbook.Sheets[sheetName];
            
            const jsonData = XLSX.utils.sheet_to_json(worksheet, { 
                header: 1,
                raw: false
            });

            if (jsonData.length === 0) {
                throw new Error('The CSV file appears to be empty');
            }

            // First row is headers
            this.headers = jsonData[0].map((h, i) => h ? String(h).trim() : `Column_${i + 1}`);
            
            // Rest are data rows
            this.rows = jsonData.slice(1).map(row => {
                const obj = {};
                this.headers.forEach((header, index) => {
                    obj[header] = row[index] !== undefined ? row[index] : null;
                });
                return obj;
            });

            // Filter out empty rows
            this.rows = this.rows.filter(row => 
                Object.values(row).some(val => val !== null && val !== '')
            );

            this.parsedData = {
                headers: this.headers,
                rows: this.rows,
                rowCount: this.rows.length,
                columnCount: this.headers.length,
                fileName: this.fileName,
                fileSize: this.fileSize
            };

            return this.parsedData;
        } catch (error) {
            throw new Error(`Failed to parse CSV file: ${error.message}`);
        }
    },

    /**
     * Get preview data (first N rows)
     */
    getPreview(numRows = 5) {
        if (!this.parsedData) return null;

        return {
            headers: this.headers,
            rows: this.rows.slice(0, numRows),
            totalRows: this.rows.length
        };
    },

    /**
     * Get column statistics
     */
    getColumnStats() {
        if (!this.parsedData) return null;

        const stats = {};
        
        this.headers.forEach(header => {
            const values = this.rows.map(row => row[header]).filter(v => v !== null && v !== '');
            const uniqueValues = [...new Set(values)];
            
            stats[header] = {
                name: header,
                totalValues: values.length,
                uniqueValues: uniqueValues.length,
                nullCount: this.rows.length - values.length,
                sampleValues: uniqueValues.slice(0, 5),
                inferredType: this.inferColumnType(values)
            };
        });

        return stats;
    },

    /**
     * Infer column data type from values
     */
    inferColumnType(values) {
        if (values.length === 0) return 'unknown';

        const sample = values.slice(0, 100); // Check first 100 values
        
        let numberCount = 0;
        let dateCount = 0;
        let boolCount = 0;

        sample.forEach(val => {
            const str = String(val).trim().toLowerCase();
            
            // Check for boolean
            if (['true', 'false', 'yes', 'no', '1', '0'].includes(str)) {
                boolCount++;
            }
            
            // Check for number
            if (!isNaN(parseFloat(val)) && isFinite(val)) {
                numberCount++;
            }
            
            // Check for date patterns
            if (this.looksLikeDate(str)) {
                dateCount++;
            }
        });

        const threshold = sample.length * 0.8; // 80% threshold

        if (boolCount >= threshold) return 'boolean';
        if (numberCount >= threshold) return 'number';
        if (dateCount >= threshold) return 'date';
        return 'string';
    },

    /**
     * Check if a string looks like a date
     */
    looksLikeDate(str) {
        // Common date patterns
        const datePatterns = [
            /^\d{4}-\d{2}-\d{2}$/, // YYYY-MM-DD
            /^\d{2}\/\d{2}\/\d{4}$/, // MM/DD/YYYY
            /^\d{2}-\d{2}-\d{4}$/, // MM-DD-YYYY
            /^\d{1,2}\/\d{1,2}\/\d{2,4}$/, // M/D/YY or M/D/YYYY
            /^\w{3}\s+\d{1,2},?\s+\d{4}$/, // Mon DD, YYYY
        ];

        return datePatterns.some(pattern => pattern.test(str));
    },

    /**
     * Transform data using a mapping configuration
     */
    transformData(mappings) {
        if (!this.parsedData) return null;

        return this.rows.map(row => {
            const transformed = {};
            
            Object.entries(mappings).forEach(([targetField, mapping]) => {
                if (mapping.sourceColumn) {
                    let value = row[mapping.sourceColumn];
                    
                    // Apply transformation if specified
                    if (mapping.transformation && value !== null && value !== '') {
                        value = this.applyTransformation(value, mapping.transformation);
                    }
                    
                    transformed[targetField] = value;
                } else if (mapping.defaultValue !== undefined) {
                    transformed[targetField] = mapping.defaultValue;
                }
            });

            return transformed;
        });
    },

    /**
     * Apply a transformation to a value
     */
    applyTransformation(value, transformation) {
        switch (transformation) {
            case 'to_integer':
                const intVal = parseInt(value, 10);
                return isNaN(intVal) ? null : intVal;
            
            case 'to_float':
                const floatVal = parseFloat(value);
                return isNaN(floatVal) ? null : floatVal;
            
            case 'to_string':
                return String(value).trim();
            
            case 'uppercase':
                return String(value).toUpperCase().trim();
            
            case 'lowercase':
                return String(value).toLowerCase().trim();
            
            case 'normalize_market_3digit':
                const num = parseInt(value, 10);
                return isNaN(num) ? null : String(num).padStart(3, '0');
            
            case 'to_date':
                try {
                    const date = new Date(value);
                    return isNaN(date.getTime()) ? null : date.toISOString().split('T')[0];
                } catch {
                    return null;
                }
            
            case 'to_iso8601':
                try {
                    const date = new Date(value);
                    return isNaN(date.getTime()) ? null : date.toISOString();
                } catch {
                    return null;
                }
            
            default:
                return value;
        }
    },

    /**
     * Export data to JSON
     */
    exportToJSON() {
        if (!this.parsedData) return null;
        return JSON.stringify(this.rows, null, 2);
    },

    /**
     * Clear parsed data
     */
    clear() {
        this.parsedData = null;
        this.headers = [];
        this.rows = [];
        this.fileName = '';
        this.fileSize = 0;
    }
};
