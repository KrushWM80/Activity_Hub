from google.cloud import bigquery
import pandas as pd

client = bigquery.Client()

def query_dl_catalog_any_field():
    query = '''
    SELECT * FROM `wmt-assetprotection-prod.Store_Support_Dev.dl_catalog`
    WHERE string_field_0 LIKE '%a0a0dwp%'
       OR string_field_1 LIKE '%a0a0dwp%'
       OR string_field_2 LIKE '%a0a0dwp%'
       OR string_field_3 LIKE '%a0a0dwp%'
       OR string_field_4 LIKE '%a0a0dwp%'
       OR string_field_5 LIKE '%a0a0dwp%'
       OR string_field_0 LIKE '%1497%'
       OR string_field_1 LIKE '%1497%'
       OR string_field_2 LIKE '%1497%'
       OR string_field_3 LIKE '%1497%'
       OR string_field_4 LIKE '%1497%'
       OR string_field_5 LIKE '%1497%'
       OR string_field_0 LIKE '%a0a0dwp.s01497.us@wal-mart.com%'
       OR string_field_1 LIKE '%a0a0dwp.s01497.us@wal-mart.com%'
       OR string_field_2 LIKE '%a0a0dwp.s01497.us@wal-mart.com%'
       OR string_field_3 LIKE '%a0a0dwp.s01497.us@wal-mart.com%'
       OR string_field_4 LIKE '%a0a0dwp.s01497.us@wal-mart.com%'
       OR string_field_5 LIKE '%a0a0dwp.s01497.us@wal-mart.com%'
    '''
    results = client.query(query).result()
    rows = [dict(row) for row in results]
    df = pd.DataFrame(rows)
    print("\nResults from dl_catalog (any field):")
    print(df if not df.empty else "No match found.")
    return df

if __name__ == "__main__":
    query_dl_catalog_any_field()
