"""
AMP Analysis Dashboard - Python ETL Pipeline
Extracts, transforms, and loads AMP event and click data
Last Updated: February 11, 2026
"""

import pandas as pd
from google.cloud import bigquery
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Tuple
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AMPDashboardETL:
    """
    ETL Pipeline for AMP Analysis Dashboard
    Integrates AMP events with click engagement data
    """
    
    def __init__(self, project_id: str = 'wmt-assetprotection-prod'):
        """Initialize BigQuery client and configuration"""
        self.project_id = project_id
        self.client = bigquery.Client(project=project_id)
        self.dataset_id = 'Store_Support_Dev'
        
        # Data sources
        self.amp_current_table = f'{project_id}.{self.dataset_id}.`Output - AMP ALL 2`'
        self.audience_cur_table = f'{project_id}.{self.dataset_id}.`Audience Breakdown Cur`'
        self.audience_hist_table = f'{project_id}.{self.dataset_id}.`Audience Breakdown Historical`'
        self.device_cur_table = f'{project_id}.{self.dataset_id}.`Device Types Cur`'
        self.device_hist_table = f'{project_id}.{self.dataset_id}.`Device Types Historical`'
        self.time_cur_table = f'{project_id}.{self.dataset_id}.`Time Spent Cur`'
        self.time_hist_table = f'{project_id}.{self.dataset_id}.`Time Spent Historical`'
        
        # Output tables
        self.dashboard_table = f'{project_id}.{self.dataset_id}.Dashboard_AMP_Analysis'
        
    def extract_amp_data(self) -> pd.DataFrame:
        """Extract current AMP data"""
        logger.info("Extracting current AMP data...")
        query = f"""
        SELECT
            event_id,
            activity_title,
            fy,
            wm_week,
            message_type,
            activity_type,
            message_status,
            division,
            region,
            market,
            store,
            edit_link,
            preview_link,
            count_of_stores,
            status,
            store_area,
            audience,
            business_area,
            created_date,
            modified_date
        FROM {self.amp_current_table}
        WHERE event_id IS NOT NULL
            AND message_type = 'Store Update'
            AND message_status = 'Published'
        """
        
        df = self.client.query(query).to_dataframe()
        logger.info(f"Extracted {len(df)} AMP records")
        return df
    
    def extract_click_data_audience(self) -> pd.DataFrame:
        """Extract and aggregate audience breakdown click data"""
        logger.info("Extracting audience breakdown click data...")
        query = f"""
        WITH audience_current AS (
            SELECT
                event_id,
                fy,
                wm_week,
                SUM(CAST(click_count AS INT64)) AS total_clicks,
                SUM(CAST(view_count AS INT64)) AS total_views,
                COUNT(DISTINCT audience_segment) AS segment_count,
                STRING_AGG(DISTINCT audience_segment, ', ') AS segments
            FROM {self.audience_cur_table}
            WHERE event_id IS NOT NULL
            GROUP BY event_id, fy, wm_week
        ),
        audience_historical AS (
            SELECT
                event_id,
                fy,
                wm_week,
                SUM(CAST(click_count AS INT64)) AS total_clicks,
                SUM(CAST(view_count AS INT64)) AS total_views,
                COUNT(DISTINCT audience_segment) AS segment_count,
                STRING_AGG(DISTINCT audience_segment, ', ') AS segments
            FROM {self.audience_hist_table}
            WHERE event_id IS NOT NULL
            GROUP BY event_id, fy, wm_week
        )
        SELECT
            COALESCE(c.event_id, h.event_id) AS event_id,
            COALESCE(c.fy, h.fy) AS fy,
            COALESCE(c.wm_week, h.wm_week) AS wm_week,
            COALESCE(c.total_clicks, 0) + COALESCE(h.total_clicks, 0) AS audience_total_clicks,
            COALESCE(c.total_views, 0) + COALESCE(h.total_views, 0) AS audience_total_views,
            COALESCE(c.segment_count, 0) AS audience_segment_count
        FROM audience_current c
        FULL OUTER JOIN audience_historical h
            ON c.event_id = h.event_id
            AND c.fy = h.fy
            AND c.wm_week = h.wm_week
        """
        
        df = self.client.query(query).to_dataframe()
        logger.info(f"Extracted {len(df)} audience records")
        return df
    
    def extract_click_data_devices(self) -> pd.DataFrame:
        """Extract and aggregate device types click data"""
        logger.info("Extracting device types click data...")
        query = f"""
        WITH devices_current AS (
            SELECT
                event_id,
                fy,
                wm_week,
                SUM(CAST(click_count AS INT64)) AS total_clicks,
                SUM(CAST(view_count AS INT64)) AS total_views,
                COUNT(DISTINCT device_type) AS device_count,
                STRING_AGG(DISTINCT device_type, ', ') AS devices
            FROM {self.device_cur_table}
            WHERE event_id IS NOT NULL
            GROUP BY event_id, fy, wm_week
        ),
        devices_historical AS (
            SELECT
                event_id,
                fy,
                wm_week,
                SUM(CAST(click_count AS INT64)) AS total_clicks,
                SUM(CAST(view_count AS INT64)) AS total_views,
                COUNT(DISTINCT device_type) AS device_count,
                STRING_AGG(DISTINCT device_type, ', ') AS devices
            FROM {self.device_hist_table}
            WHERE event_id IS NOT NULL
            GROUP BY event_id, fy, wm_week
        )
        SELECT
            COALESCE(c.event_id, h.event_id) AS event_id,
            COALESCE(c.fy, h.fy) AS fy,
            COALESCE(c.wm_week, h.wm_week) AS wm_week,
            COALESCE(c.total_clicks, 0) + COALESCE(h.total_clicks, 0) AS device_total_clicks,
            COALESCE(c.total_views, 0) + COALESCE(h.total_views, 0) AS device_total_views,
            COALESCE(c.device_count, 0) AS device_type_count
        FROM devices_current c
        FULL OUTER JOIN devices_historical h
            ON c.event_id = h.event_id
            AND c.fy = h.fy
            AND c.wm_week = h.wm_week
        """
        
        df = self.client.query(query).to_dataframe()
        logger.info(f"Extracted {len(df)} device records")
        return df
    
    def extract_click_data_timespent(self) -> pd.DataFrame:
        """Extract and aggregate time spent click data"""
        logger.info("Extracting time spent click data...")
        query = f"""
        WITH timespent_current AS (
            SELECT
                event_id,
                fy,
                wm_week,
                SUM(CAST(click_count AS INT64)) AS total_clicks,
                SUM(CAST(view_count AS INT64)) AS total_views,
                AVG(CAST(duration_seconds AS FLOAT64)) AS avg_duration,
                MAX(CAST(duration_seconds AS INT64)) AS max_duration
            FROM {self.time_cur_table}
            WHERE event_id IS NOT NULL
            GROUP BY event_id, fy, wm_week
        ),
        timespent_historical AS (
            SELECT
                event_id,
                fy,
                wm_week,
                SUM(CAST(click_count AS INT64)) AS total_clicks,
                SUM(CAST(view_count AS INT64)) AS total_views,
                AVG(CAST(duration_seconds AS FLOAT64)) AS avg_duration,
                MAX(CAST(duration_seconds AS INT64)) AS max_duration
            FROM {self.time_hist_table}
            WHERE event_id IS NOT NULL
            GROUP BY event_id, fy, wm_week
        )
        SELECT
            COALESCE(c.event_id, h.event_id) AS event_id,
            COALESCE(c.fy, h.fy) AS fy,
            COALESCE(c.wm_week, h.wm_week) AS wm_week,
            COALESCE(c.total_clicks, 0) + COALESCE(h.total_clicks, 0) AS time_total_clicks,
            COALESCE(c.total_views, 0) + COALESCE(h.total_views, 0) AS time_total_views,
            ROUND(COALESCE(c.avg_duration, 0) + COALESCE(h.avg_duration, 0), 2) AS avg_duration_seconds
        FROM timespent_current c
        FULL OUTER JOIN timespent_historical h
            ON c.event_id = h.event_id
            AND c.fy = h.fy
            AND c.wm_week = h.wm_week
        """
        
        df = self.client.query(query).to_dataframe()
        logger.info(f"Extracted {len(df)} time spent records")
        return df
    
    def transform_and_combine(self, amp_df: pd.DataFrame, 
                             audience_df: pd.DataFrame,
                             devices_df: pd.DataFrame,
                             timespent_df: pd.DataFrame) -> pd.DataFrame:
        """Transform and combine all data sources"""
        logger.info("Transforming and combining data...")
        
        # Merge click data on event_id, fy, wm_week
        merged_df = amp_df.copy()
        
        # Merge audience data
        merged_df = merged_df.merge(
            audience_df,
            on=['event_id', 'fy', 'wm_week'],
            how='left'
        )
        
        # Merge device data
        merged_df = merged_df.merge(
            devices_df,
            on=['event_id', 'fy', 'wm_week'],
            how='left'
        )
        
        # Merge time spent data
        merged_df = merged_df.merge(
            timespent_df,
            on=['event_id', 'fy', 'wm_week'],
            how='left'
        )
        
        # Fill NaN values with 0 for click metrics
        click_columns = [
            'audience_total_clicks', 'audience_total_views', 'audience_segment_count',
            'device_total_clicks', 'device_total_views', 'device_type_count',
            'time_total_clicks', 'time_total_views', 'avg_duration_seconds'
        ]
        merged_df[click_columns] = merged_df[click_columns].fillna(0)
        
        # Calculate total clicks across all sources
        merged_df['total_clicks'] = (
            merged_df['audience_total_clicks'] + 
            merged_df['device_total_clicks'] + 
            merged_df['time_total_clicks']
        ).astype(int)
        
        # Add dashboard refresh timestamp
        merged_df['dashboard_refresh_timestamp'] = datetime.now()
        
        logger.info(f"Combined {len(merged_df)} records")
        return merged_df
    
    def load_to_bigquery(self, df: pd.DataFrame, table_id: str) -> bool:
        """Load dataframe to BigQuery table"""
        logger.info(f"Loading {len(df)} records to {table_id}...")
        
        try:
            job_config = bigquery.LoadJobConfig(
                write_disposition="WRITE_TRUNCATE",
                autodetect=True
            )
            
            job = self.client.load_table_from_dataframe(
                df,
                table_id,
                job_config=job_config
            )
            
            job.result()
            logger.info(f"Successfully loaded data to {table_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading data to BigQuery: {str(e)}")
            return False
    
    def run(self) -> bool:
        """Execute the complete ETL pipeline"""
        logger.info("=" * 60)
        logger.info("Starting AMP Dashboard ETL Pipeline")
        logger.info("=" * 60)
        
        try:
            # Extract
            amp_df = self.extract_amp_data()
            audience_df = self.extract_click_data_audience()
            devices_df = self.extract_click_data_devices()
            timespent_df = self.extract_click_data_timespent()
            
            # Transform
            dashboard_df = self.transform_and_combine(
                amp_df, audience_df, devices_df, timespent_df
            )
            
            # Load
            success = self.load_to_bigquery(dashboard_df, self.dashboard_table)
            
            if success:
                logger.info("=" * 60)
                logger.info("ETL Pipeline completed successfully")
                logger.info(f"Total records loaded: {len(dashboard_df)}")
                logger.info("=" * 60)
                return True
            else:
                logger.error("ETL Pipeline failed during load phase")
                return False
                
        except Exception as e:
            logger.error(f"ETL Pipeline execution failed: {str(e)}")
            return False


def main():
    """Main execution function"""
    etl = AMPDashboardETL(project_id='wmt-assetprotection-prod')
    success = etl.run()
    
    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
