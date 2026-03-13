#!/usr/bin/env python3
"""Quick check: what Walmart week is March 13, 2026?"""
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'
from google.cloud import bigquery
client = bigquery.Client(project='wmt-assetprotection-prod')
q = """
SELECT DISTINCT WM_Week, FY, MIN(Start_Date) as start_dt, MAX(End_Date) as end_dt
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND CAST(WM_Week AS INT64) BETWEEN 3 AND 8
GROUP BY WM_Week, FY
ORDER BY CAST(WM_Week AS INT64)
"""
for r in client.query(q).result():
    print(f'  FY{r.FY} Week {r.WM_Week}: {r.start_dt} to {r.end_dt}')
