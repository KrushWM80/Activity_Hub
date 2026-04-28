#!/usr/bin/env python3
"""
Pricing Operations Callouts - BigQuery DDL Setup
Initialize BigQuery tables for callouts and email recipients

Usage:
  python setup_bigquery.py [--project <project_id>] [--dataset <dataset_id>]
"""

import sys
import logging
from pathlib import Path
from google.cloud import bigquery
import argparse

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================

BQ_PROJECT = 'wmt-pricingops-analytics'
BQ_DATASET = 'Pricing_Ops'

def create_tables(project=None, dataset=None):
    """Create BigQuery tables"""
    if project is None:
        project = BQ_PROJECT
    if dataset is None:
        dataset = BQ_DATASET
    
    logger.info(f'Connecting to BigQuery project: {project}')
    client = bigquery.Client(project=project)
    
    # ────────────────────────────────────────────────────────────────────────
    # Table 1: Weekly_Callouts
    # ────────────────────────────────────────────────────────────────────────
    
    table_id_callouts = f'{project}.{dataset}.Weekly_Callouts'
    
    schema_callouts = [
        bigquery.SchemaField('id', 'STRING', mode='REQUIRED', description='Unique callout ID'),
        bigquery.SchemaField('wm_week', 'INTEGER', mode='REQUIRED', description='Walmart week number (1-53)'),
        bigquery.SchemaField('title', 'STRING', mode='NULLABLE', description='Callout title'),
        bigquery.SchemaField('content', 'STRING', mode='REQUIRED', description='Callout content/description'),
        bigquery.SchemaField('created_date', 'TIMESTAMP', mode='REQUIRED', description='When callout was created'),
        bigquery.SchemaField('created_by', 'STRING', mode='REQUIRED', description='User who created callout'),
        bigquery.SchemaField('last_modified_date', 'TIMESTAMP', mode='REQUIRED', description='Last modification timestamp'),
        bigquery.SchemaField('status', 'STRING', mode='NULLABLE', description='Status: active, archived, deleted'),
    ]
    
    try:
        client.get_table(table_id_callouts)
        logger.info(f'✓ Table {table_id_callouts} already exists')
    except Exception as e:
        if 'Not found' in str(e):
            table = bigquery.Table(table_id_callouts, schema=schema_callouts)
            table.description = 'Weekly pricing callouts by Walmart week'
            client.create_table(table)
            logger.info(f'✓ Created table {table_id_callouts}')
            
            # Add clustering
            try:
                table.clustering_fields = ['wm_week']
                client.update_table(table, ['clustering_fields'])
                logger.info(f'✓ Added clustering on wm_week')
            except:
                pass
        else:
            raise
    
    # ────────────────────────────────────────────────────────────────────────
    # Table 2: Callout_Email_Recipients
    # ────────────────────────────────────────────────────────────────────────
    
    table_id_recipients = f'{project}.{dataset}.Callout_Email_Recipients'
    
    schema_recipients = [
        bigquery.SchemaField('id', 'STRING', mode='REQUIRED', description='Unique recipient ID'),
        bigquery.SchemaField('email', 'STRING', mode='REQUIRED', description='Email address'),
        bigquery.SchemaField('added_date', 'TIMESTAMP', mode='REQUIRED', description='When recipient was added'),
        bigquery.SchemaField('is_active', 'BOOLEAN', mode='REQUIRED', description='Whether recipient is active'),
    ]
    
    try:
        client.get_table(table_id_recipients)
        logger.info(f'✓ Table {table_id_recipients} already exists')
    except Exception as e:
        if 'Not found' in str(e):
            table = bigquery.Table(table_id_recipients, schema=schema_recipients)
            table.description = 'Email recipients for weekly callouts email'
            client.create_table(table)
            logger.info(f'✓ Created table {table_id_recipients}')
        else:
            raise
    
    logger.info('✓ All tables initialized successfully')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pricing Callouts BigQuery Setup')
    parser.add_argument('--project', help='BigQuery project ID', default=BQ_PROJECT)
    parser.add_argument('--dataset', help='BigQuery dataset ID', default=BQ_DATASET)
    args = parser.parse_args()
    
    try:
        create_tables(project=args.project, dataset=args.dataset)
        logger.info('✓ Setup complete!')
        sys.exit(0)
    except Exception as e:
        logger.error(f'Setup failed: {e}', exc_info=True)
        sys.exit(1)
