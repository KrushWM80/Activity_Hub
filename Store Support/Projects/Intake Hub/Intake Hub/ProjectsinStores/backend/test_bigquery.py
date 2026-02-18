# Test BigQuery Connection
# Run this to verify you can connect to BigQuery before starting the dashboard

from google.cloud import bigquery
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_connection():
    """Test BigQuery connection"""
    print("=" * 60)
    print("Testing BigQuery Connection")
    print("=" * 60)
    print()
    
    project_id = os.getenv("GCP_PROJECT_ID", "wmt-assetprotection-prod")
    dataset = os.getenv("BIGQUERY_DATASET", "Store_Support_Dev")
    table = os.getenv("BIGQUERY_TABLE", "IH_Intake_Data")
    
    print(f"Project: {project_id}")
    print(f"Dataset: {dataset}")
    print(f"Table: {table}")
    print()
    
    try:
        # Initialize client
        print("Initializing BigQuery client...")
        client = bigquery.Client(project=project_id)
        print("✅ Client initialized")
        print()
        
        # Test query
        print("Running test query...")
        query = f"""
        SELECT 
            COUNT(*) as total_projects,
            COUNT(DISTINCT CASE WHEN status = 'Active' THEN project_id END) as active_projects,
            COUNT(DISTINCT CASE WHEN project_source = 'Intake Hub' THEN project_id END) as intake_hub_projects,
            COUNT(DISTINCT CASE WHEN project_source = 'Realty' THEN project_id END) as realty_projects
        FROM `{project_id}.{dataset}.{table}`
        """
        
        result = list(client.query(query).result())[0]
        
        print("✅ Query successful!")
        print()
        print("Results:")
        print(f"  Total Projects: {result.total_projects}")
        print(f"  Active Projects: {result.active_projects}")
        print(f"  Intake Hub: {result.intake_hub_projects}")
        print(f"  Realty: {result.realty_projects}")
        print()
        
        # Test getting sample data
        print("Fetching sample project...")
        sample_query = f"""
        SELECT 
            project_id,
            project_source,
            title,
            division,
            region,
            status,
            store_count
        FROM `{project_id}.{dataset}.{table}`
        WHERE status = 'Active'
        LIMIT 1
        """
        
        sample = list(client.query(sample_query).result())
        if sample:
            row = sample[0]
            print("✅ Sample project retrieved:")
            print(f"  ID: {row.project_id}")
            print(f"  Title: {row.title}")
            print(f"  Source: {row.project_source}")
            print(f"  Division: {row.division}")
            print(f"  Status: {row.status}")
            print()
        
        print("=" * 60)
        print("✅ SUCCESS! BigQuery connection is working!")
        print("=" * 60)
        print()
        print("You can now start the dashboard with: python main.py")
        return True
        
    except Exception as e:
        print("=" * 60)
        print("❌ ERROR: Could not connect to BigQuery")
        print("=" * 60)
        print()
        print(f"Error details: {e}")
        print()
        print("Troubleshooting:")
        print("1. Make sure you're authenticated:")
        print("   gcloud auth application-default login")
        print()
        print("2. Verify project access:")
        print("   gcloud config set project wmt-assetprotection-prod")
        print()
        print("3. Check you have BigQuery permissions")
        print()
        print("4. The dashboard will work with mock data if BigQuery is unavailable")
        return False

if __name__ == "__main__":
    test_connection()
