# Requirements Explanation

## Core Data Processing
- **pandas>=1.5.0** - Essential for DataFrame operations, data manipulation, and transformations
- **numpy>=1.21.0** - Required for numerical operations and array processing
- **sqlalchemy>=1.4.0** - Database toolkit for SQL operations and connections

## BigQuery Integration
- **google-cloud-bigquery>=3.0.0** - Primary connector for your BigQuery data sources
- **db-dtypes>=1.0.0** - Handles BigQuery-specific data types properly

## File Format Support
- **pyarrow>=8.0.0** - High-performance Parquet file reading/writing (recommended for large datasets)
- **fastparquet>=0.8.0** - Alternative Parquet engine for better compatibility
- **openpyxl>=3.0.0** - Excel file support (.xlsx format)
- **xlsxwriter>=3.0.0** - Enhanced Excel writing with formatting options

## Visualization & Analysis
- **matplotlib>=3.5.0** - Basic plotting and chart generation
- **seaborn>=0.11.0** - Statistical data visualization (enhanced matplotlib)
- **plotly>=5.0.0** - Interactive charts and dashboards

## Geographic Analysis
- **folium>=0.12.0** - Interactive maps using your latitude/longitude data
- **geopandas>=0.10.0** - Geographic data analysis and spatial operations

## Optional Enhancements (install as needed)

### Advanced Analytics
```
scikit-learn>=1.1.0    # Machine learning and clustering
scipy>=1.8.0           # Statistical functions
statsmodels>=0.13.0    # Statistical modeling
```

### Dashboard Creation
```
streamlit>=1.20.0      # Web app dashboard creation
dash>=2.8.0            # Interactive web applications
jupyter>=1.0.0         # Notebook environment
```

### Performance Optimization
```
dask>=2023.1.0         # Parallel computing for large datasets
modin>=0.18.0          # Pandas acceleration
numba>=0.56.0          # Just-in-time compilation
```

### Additional Database Connectors
```
psycopg2>=2.9.0        # PostgreSQL connection
pymssql>=2.2.0         # SQL Server connection
cx-Oracle>=8.3.0       # Oracle database connection
```

## Installation Commands

### Minimal Installation (Core Features)
```bash
pip install pandas numpy google-cloud-bigquery pyarrow openpyxl sqlalchemy db-dtypes
```

### Complete Installation (All Features)
```bash
pip install -r requirements.txt
```

### Development Installation (with optional packages)
```bash
pip install -r requirements.txt
pip install scikit-learn scipy streamlit jupyter dask
```

## Platform-Specific Notes

### Windows
- All packages should install without issues
- For geopandas, you might need: `conda install geopandas` (if using Conda)

### macOS
- May need Xcode command line tools for some packages
- Use `brew install` for system dependencies if needed

### Linux
- May require additional system packages for geographic analysis
- Install GDAL/PROJ libraries if using geopandas

## Package Usage in Pipeline

### Data Processing
- **pandas/numpy**: Core data manipulation in all pipeline functions
- **sqlalchemy**: Database connections and SQL operations

### BigQuery Integration  
- **google-cloud-bigquery**: All extract_primary_data() and extract_additional_tables() functions
- **db-dtypes**: Proper handling of BigQuery timestamp and geography types

### Output Generation
- **pyarrow**: create_output_table() for Parquet format (default)
- **openpyxl**: create_output_table() for Excel format
- **xlsxwriter**: Enhanced Excel formatting in business reports

### Visualization
- **matplotlib/seaborn**: create_demo_visualizations() function
- **plotly**: Interactive charts in dashboard outputs
- **folium**: Geographic heat maps using store location data

### Geographic Analysis
- **geopandas**: store_location_analysis.py geographic operations
- **folium**: Interactive maps with store coordinates

## Memory and Performance Considerations

### Large Dataset Handling
For datasets > 1GB, consider:
```bash
pip install dask modin
```

### Fast I/O Operations
For frequent file operations:
```bash
pip install fastparquet tables
```

### GPU Acceleration (if available)
```bash
pip install cudf cupy  # NVIDIA RAPIDS
```

## Troubleshooting

### Common Installation Issues

**Issue**: `geopandas` installation fails
**Solution**: Use conda instead: `conda install geopandas`

**Issue**: `google-cloud-bigquery` authentication errors
**Solution**: Run `gcloud auth application-default login`

**Issue**: Memory errors with large datasets  
**Solution**: Install dask: `pip install dask` and use chunked processing

**Issue**: Excel files corrupted
**Solution**: Update openpyxl: `pip install --upgrade openpyxl`

### Version Conflicts
If you encounter version conflicts:
```bash
pip install --upgrade pip
pip install --force-reinstall -r requirements.txt
```

## Development Dependencies (Optional)

For pipeline development and testing:
```bash
pip install pytest pytest-cov black flake8 mypy jupyter
```