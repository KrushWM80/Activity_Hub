"""Test script to check Realty projects in BigQuery"""
from google.cloud import bigquery
import os

def test_realty_projects():
    client = bigquery.Client(project="wmt-assetprotection-prod")
    
    # Check distinct Project_Source values
    query1 = """
        SELECT DISTINCT Project_Source, COUNT(*) as count
        FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
        WHERE Status = 'Active'
        GROUP BY Project_Source
        ORDER BY count DESC
    """
    
    print("=== Project Sources ===")
    result1 = client.query(query1).to_dataframe()
    print(result1)
    
    # Check for Realty projects specifically
    query2 = """
        SELECT 
            CAST(Intake_Card AS STRING) as project_id,
            Title,
            Project_Source,
            Status
        FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
        WHERE Status = 'Active' 
        AND Project_Source LIKE '%ealty%'
        LIMIT 10
    """
    
    print("\n=== Sample Realty Projects ===")
    result2 = client.query(query2).to_dataframe()
    print(result2)
    
    # Count Realty projects
    query3 = """
        SELECT COUNT(DISTINCT Intake_Card) as realty_count
        FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
        WHERE Status = 'Active' 
        AND Project_Source = 'Realty'
    """
    
    print("\n=== Realty Project Count ===")
    result3 = client.query(query3).to_dataframe()
    print(result3)

if __name__ == "__main__":
    test_realty_projects()
