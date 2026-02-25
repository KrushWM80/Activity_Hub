from google.cloud import bigquery

client = bigquery.Client()

def print_dl_catalog_schema():
    table_ref = client.get_table('wmt-assetprotection-prod.Store_Support_Dev.dl_catalog')
    print("\nSchema for dl_catalog:")
    for field in table_ref.schema:
        print(f"{field.name} ({field.field_type})")

if __name__ == "__main__":
    print_dl_catalog_schema()
