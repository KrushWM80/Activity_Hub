#!/usr/bin/env python3
from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Check projects for Kristine, Matt, and Kendall
for owner in ['Kristine Torres', 'Matt Farnworth', 'Kendall Rush']:
    sql = f"""
    SELECT COUNT(*) as count
    FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
    WHERE owner = '{owner}'
    """
    result = list(client.query(sql).result())
    print(f"{owner}: {result[0]['count']} projects")
