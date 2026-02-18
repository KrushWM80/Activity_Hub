"""
Enhanced Google Cloud Function for Multi-Source AMP Data Sync
Monitors AMP Events, Calendar, and Store dimensions with different frequencies
"""

import functions_framework
from google.cloud import bigquery
import logging
from datetime import datetime, date
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@functions_framework.http
def enhanced_amp_sync_trigger(request):
    """HTTP Cloud Function for enhanced multi-source synchronization"""
    
    try:
        # Initialize BigQuery client
        client = bigquery.Client()
        
        # Get request parameters
        request_json = request.get_json(silent=True)
        force_full_refresh = request_json.get('force_full_refresh', False) if request_json else False
        
        logger.info("Starting enhanced multi-source AMP data sync...")
        
        # Call the enhanced stored procedure
        if force_full_refresh:
            query = "CALL `wmt-assetprotection-prod.Store_Support.full_refresh_proc`();"
            logger.info("Forcing full refresh of all data sources")
        else:
            query = "CALL `wmt-assetprotection-prod.Store_Support.enhanced_amp_sync_proc`();"
        
        # Execute the procedure
        start_time = datetime.now()
        query_job = client.query(query)
        query_job.result()  # Wait for completion
        end_time = datetime.now()
        
        duration = (end_time - start_time).total_seconds()
        
        logger.info(f"Enhanced AMP data sync completed in {duration} seconds")
        
        # Get latest sync status
        status_query = """
        SELECT 
          trigger_type,
          records_updated,
          additional_info,
          success
        FROM `wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Update_Log`
        ORDER BY update_timestamp DESC 
        LIMIT 1
        """
        
        status_result = client.query(status_query).result()
        status_info = {}
        for row in status_result:
            status_info = {
                'trigger_type': row.trigger_type,
                'records_updated': row.records_updated,
                'additional_info': json.loads(row.additional_info) if row.additional_info else {},
                'success': row.success
            }
            break
        
        return {
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'duration_seconds': duration,
            'sync_info': status_info,
            'message': 'Enhanced multi-source AMP data sync completed successfully'
        }, 200
        
    except Exception as e:
        logger.error(f"Error in enhanced AMP data sync: {str(e)}")
        
        # Log the error to BigQuery
        try:
            error_query = f"""
            INSERT INTO `wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Update_Log`
            (update_timestamp, records_updated, trigger_type, success, error_message)
            VALUES (CURRENT_TIMESTAMP(), 0, 'ERROR', FALSE, '{str(e)}');
            """
            client.query(error_query)
        except:
            pass  # Don't fail on logging errors
        
        return {
            'status': 'error',
            'timestamp': datetime.now().isoformat(),
            'message': str(e)
        }, 500

@functions_framework.cloud_event
def enhanced_amp_sync_scheduled(cloud_event):
    """Scheduled function for multi-source monitoring"""
    
    try:
        # Initialize BigQuery client
        client = bigquery.Client()
        
        # Determine sync type based on date
        today = date.today()
        is_month_start = today.day <= 3
        
        logger.info(f"Starting scheduled sync - Month start: {is_month_start}")
        
        # Call appropriate procedure
        if is_month_start:
            # Comprehensive check including dimensions
            query = "CALL `wmt-assetprotection-prod.Store_Support.enhanced_amp_sync_proc`();"
            logger.info("Running comprehensive sync (including dimension checks)")
        else:
            # AMP events only
            query = """
            DECLARE last_update TIMESTAMP;
            SET last_update = (
                SELECT MAX(PARSE_DATETIME('%m/%d/%Y %l:%M:%S %p', `Last Updated`))
                FROM `wmt-assetprotection-prod.Store_Support.AMP_Data_Final`
            );
            CALL `wmt-assetprotection-prod.Store_Support.incremental_amp_update_proc`(last_update);
            """
            logger.info("Running AMP-only incremental sync")
        
        # Execute the procedure
        start_time = datetime.now()
        query_job = client.query(query)
        query_job.result()  # Wait for completion
        end_time = datetime.now()
        
        duration = (end_time - start_time).total_seconds()
        
        logger.info(f"Scheduled enhanced sync completed in {duration} seconds")
        
    except Exception as e:
        logger.error(f"Error in scheduled enhanced sync: {str(e)}")
        
        # Log the error to BigQuery
        try:
            error_query = f"""
            INSERT INTO `wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Update_Log`
            (update_timestamp, records_updated, trigger_type, success, error_message)
            VALUES (CURRENT_TIMESTAMP(), 0, 'SCHEDULED_ERROR', FALSE, '{str(e)}');
            """
            client.query(error_query)
        except:
            pass  # Don't fail on logging errors

@functions_framework.http
def monthly_dimension_refresh(request):
    """Manual trigger for monthly dimension refresh"""
    
    try:
        client = bigquery.Client()
        
        logger.info("Starting manual monthly dimension refresh...")
        
        # Force full refresh
        query = "CALL `wmt-assetprotection-prod.Store_Support.full_refresh_proc`();"
        
        start_time = datetime.now()
        query_job = client.query(query)
        query_job.result()
        end_time = datetime.now()
        
        duration = (end_time - start_time).total_seconds()
        
        logger.info(f"Monthly dimension refresh completed in {duration} seconds")
        
        return {
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'duration_seconds': duration,
            'message': 'Monthly dimension refresh completed successfully'
        }, 200
        
    except Exception as e:
        logger.error(f"Error in monthly dimension refresh: {str(e)}")
        return {
            'status': 'error',
            'timestamp': datetime.now().isoformat(),
            'message': str(e)
        }, 500
