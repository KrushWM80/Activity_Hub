# Store Alignment Data Integration

This folder contains all store alignment and data comparison files for AMP (Asset Management Program).

## Files in this folder:

### 📊 **Tableau Integration Files:**
- **tableau_schema_extracted.json** - Extracted Tableau schema data
- **tableau_schema_extractor.py** - Python script to extract Tableau schemas
- **amp_bigquery_tableau_integration.py** - BigQuery-Tableau integration script
- **amp_bigquery_integration_tableau_aligned_20251027_233101.sql** - SQL for Tableau-aligned BigQuery integration

### 🔄 **Data Comparison Files:**
- **csv_bigquery_comparison.py** - Python script for CSV-BigQuery data comparison
- **amp_csv_bigquery_comparison_csv_bigquery_comparison.json** - Comparison results and mapping data

## Purpose

These files are used for:
- Aligning BigQuery data with Tableau dashboards
- Data schema extraction and comparison
- Store data synchronization across systems
- CSV to BigQuery migration and validation
- Ensuring data consistency between different platforms

## Key Functionality

### 🎯 **Store Alignment:**
- Schema mapping between different data sources
- Data structure standardization
- Cross-platform data validation

### 📈 **Tableau Integration:**
- Schema extraction from Tableau workbooks
- BigQuery-Tableau data alignment
- Dashboard data source management

### 🔍 **Data Comparison:**
- CSV vs BigQuery data validation
- Data quality checks
- Migration verification tools

## Usage

This folder is organized for reuse in other projects that require:
- Multi-platform data integration
- Schema alignment and mapping
- Data migration and validation
- Tableau-BigQuery connectivity
- Store data management across systems

## Related Projects

These store alignment components can be used for:
- Other dashboard projects requiring data alignment
- Data migration projects
- Multi-source data integration
- Schema mapping and validation tools
- Cross-platform data synchronization

---
*Organized on November 7, 2025 for project reusability*