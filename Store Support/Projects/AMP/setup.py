"""
Installation and Setup Script for Store Operations Data Pipeline
Author: GitHub Copilot
Date: October 24, 2025
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required Python packages"""
    requirements = [
        'pandas>=1.5.0',
        'numpy>=1.21.0', 
        'google-cloud-bigquery>=3.0.0',
        'pyarrow>=8.0.0',  # For parquet support
        'openpyxl>=3.0.0',  # For Excel support
        'sqlalchemy>=1.4.0',
        'db-dtypes>=1.0.0',  # For BigQuery data types
        'matplotlib>=3.5.0',  # For visualizations
        'seaborn>=0.11.0',  # Enhanced plotting
        'plotly>=5.0.0',  # Interactive charts
        'folium>=0.12.0',  # Geographic mapping
        'geopandas>=0.10.0',  # Geographic analysis
        'xlsxwriter>=3.0.0',  # Enhanced Excel support
        'fastparquet>=0.8.0'  # Alternative parquet engine
    ]
    
    print("Installing required packages...")
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False
    
    return True

def create_directory_structure():
    """Create necessary directory structure"""
    directories = [
        'output',
        'logs',
        'config',
        'temp'
    ]
    
    print("Creating directory structure...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def setup_authentication():
    """Setup Google Cloud authentication instructions"""
    print("\n" + "="*60)
    print("GOOGLE CLOUD AUTHENTICATION SETUP")
    print("="*60)
    print("""
To use this pipeline with Google BigQuery, you need to set up authentication:

1. Install Google Cloud SDK:
   https://cloud.google.com/sdk/docs/install

2. Authenticate with your Google Cloud account:
   gcloud auth application-default login

3. Set your default project:
   gcloud config set project YOUR_PROJECT_ID

4. Alternatively, set the GOOGLE_APPLICATION_CREDENTIALS environment variable:
   set GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json

For more information, visit:
https://cloud.google.com/docs/authentication/getting-started
    """)

def main():
    """Main setup function"""
    print("Store Operations Data Pipeline Setup")
    print("="*50)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed during package installation")
        return
    
    # Create directories
    create_directory_structure()
    
    # Show authentication setup
    setup_authentication()
    
    print("\n✅ Setup completed successfully!")
    print("\nNext steps:")
    print("1. Configure your Google Cloud authentication")
    print("2. Update pipeline_config.json with your project details")
    print("3. Run: python pipeline_examples.py")

if __name__ == "__main__":
    main()