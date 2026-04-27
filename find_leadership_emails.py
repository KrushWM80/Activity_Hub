#!/usr/bin/env python3
"""
Find Matt Farnworth and Kristine Torres in Intake Hub Data
"""

from google.cloud import bigquery
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
    os.environ.get('APPDATA', ''), 'gcloud', 'application_default_credentials.json'
)

client = bigquery.Client(project='wmt-assetprotection-prod')

def find_leadership_emails():
    """Search Intake Hub for Matt Farnworth and Kristine Torres"""
    
    print("=" * 80)
    print("SEARCHING INTAKE HUB FOR LEADERSHIP CHAIN EMAILS")
    print("=" * 80)
    
    # Search for all three people
    names_to_find = [
        'Kendall Rush',
        'Matt Farnworth',
        'Kristine Torres'
    ]
    
    for name in names_to_find:
        print(f"\n[SEARCHING] {name}")
        print("-" * 80)
        
        query = f"""
        SELECT DISTINCT
            Owner,
            Project_Title,
            CAST(Intake_Card_Nbr AS STRING) as Intake_Card_Nbr,
            Project_Update_Date
        FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
        WHERE Owner LIKE '%{name}%'
           OR Initiative_Lead LIKE '%{name}%'
        LIMIT 10
        """
        
        try:
            results = list(client.query(query).result())
            
            if results:
                print(f"✓ Found {len(results)} record(s):")
                for i, row in enumerate(results[:5], 1):
                    print(f"  {i}. Owner: {row['Owner']}")
                    print(f"     Project: {row['Project_Title']}")
                    print(f"     Card #: {row['Intake_Card_Nbr']}")
            else:
                print(f"✗ No records found for {name}")
        
        except Exception as e:
            print(f"✗ Error: {e}")
    
    # Now search for emails specifically
    print("\n" + "=" * 80)
    print("SEARCHING FOR EMAIL ADDRESSES")
    print("=" * 80)
    
    email_query = """
    SELECT DISTINCT
        Owner,
        Email,
        Project_Title
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
    WHERE Owner IN ('Kendall Rush', 'Matt Farnworth', 'Kristine Torres')
       OR Email LIKE '%farnworth%'
       OR Email LIKE '%torres%'
       OR Email LIKE '%rush%'
    LIMIT 20
    """
    
    try:
        results = list(client.query(email_query).result())
        
        print(f"\n✓ Found {len(results)} record(s):\n")
        
        emails_found = {}
        for row in results:
            owner = row['Owner']
            email = row['Email']
            
            if owner and email:
                if owner not in emails_found:
                    print(f"{owner}: {email}")
                    emails_found[owner] = email
        
        print("\n" + "=" * 80)
        print("EMAIL SUMMARY")
        print("=" * 80)
        for owner, email in emails_found.items():
            print(f"  {owner}: {email}")
            
        return emails_found
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return {}


if __name__ == '__main__':
    find_leadership_emails()
