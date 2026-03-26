from google.cloud import bigquery
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

try:
    client = bigquery.Client(project='wmt-assetprotection-prod')
    
    # Check IH_Intake_Data table
    table_id = 'Store_Support_Dev.IH_Intake_Data'
    table = client.get_table(table_id)
    
    print('Fields in IH_Intake_Data table:')
    print('=' * 80)
    for i, field in enumerate(table.schema, 1):
        print(f'{i:2d}. {field.name:<40} {str(field.field_type):<12}')
        
except Exception as e:
    print(f'ERROR: {e}')
    import traceback
    traceback.print_exc()
