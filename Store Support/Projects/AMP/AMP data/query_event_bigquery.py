"""
Query specific event from BigQuery and display results
Event ID: 5b635469-0694-4a39-bbe8-ee873d3d22b5
"""

from google.cloud import bigquery
import pandas as pd
from tabulate import tabulate

def query_specific_event():
    # Initialize BigQuery client
    client = bigquery.Client(project='wmt-assetprotection-prod')
    
    query = """
    SELECT 
      -- Event Core Information
      e.event_id,
      e.msg_id as message_id,
      e.actv_title_home_ofc_nm as message_title,
      e.msg_txt as message_description,
      e.msg_start_dt as message_start_date,
      e.msg_end_dt as message_end_date,
      
      -- Classification
      e.bus_domain_nm as business_area,
      e.actv_type_nm as activity_type,
      e.msg_type_nm as message_type,
      e.msg_status_id as message_status,
      e.priority_status_ind as priority_level,
      
      -- Store & Location
      e.trgt_store_nbr_array as store_array,
      
      -- Calendar Information
      c.FISCAL_YEAR_NBR as FY,
      c.WM_WEEK_NBR as WM_WEEK,
      c.WM_QTR_NAME as QUARTER,
      c.CALENDAR_DATE,
      
      -- Audit Fields
      e.create_user as created_by,
      e.create_ts as created_datetime,
      e.upd_user as modified_by,
      e.upd_ts as modified_datetime,
      e.src_rcv_ts as published_datetime,
      e.msg_hide_ind as hidden_status,
      
      -- System Fields
      e.msg_leg_status_nm as workflow_stage

    FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT` e

    -- Join with Calendar Dimension for date/week info
    LEFT JOIN `wmt-edw-prod.US_CORE_DIM_VM.CALENDAR_DIM` c
      ON CAST(e.msg_start_dt AS DATE) = c.CALENDAR_DATE

    WHERE e.event_id = '5b635469-0694-4a39-bbe8-ee873d3d22b5'

    ORDER BY e.create_ts DESC
    LIMIT 1;
    """
    
    print("Executing BigQuery query for event_id: 5b635469-0694-4a39-bbe8-ee873d3d22b5")
    print("=" * 100)
    
    try:
        # Execute query
        df = client.query(query).to_dataframe()
        
        if df.empty:
            print("\n❌ No data found for this event_id")
            print("The event may not exist or may be in a different table.")
            return None
            
        print(f"\n✅ Found {len(df)} record(s)\n")
        
        # Create mapping table
        column_mapping = {
            'event_id': 'e.event_id',
            'message_id': 'e.msg_id',
            'message_title': 'e.actv_title_home_ofc_nm',
            'message_description': 'e.msg_txt',
            'message_start_date': 'e.msg_start_dt',
            'message_end_date': 'e.msg_end_dt',
            'business_area': 'e.bus_domain_nm',
            'activity_type': 'e.actv_type_nm',
            'message_type': 'e.msg_type_nm',
            'message_status': 'e.msg_status_id',
            'priority_level': 'e.priority_status_ind',
            'store_array': 'e.trgt_store_nbr_array',
            'FY': 'c.FISCAL_YEAR_NBR',
            'WM_WEEK': 'c.WM_WEEK_NBR',
            'QUARTER': 'c.WM_QTR_NAME',
            'CALENDAR_DATE': 'c.CALENDAR_DATE',
            'created_by': 'e.create_user',
            'created_datetime': 'e.create_ts',
            'modified_by': 'e.upd_user',
            'modified_datetime': 'e.upd_ts',
            'published_datetime': 'e.src_rcv_ts',
            'hidden_status': 'e.msg_hide_ind',
            'workflow_stage': 'e.msg_leg_status_nm'
        }
        
        # Build results table
        results = []
        for col in df.columns:
            value = df[col].iloc[0]
            source_col = column_mapping.get(col, col)
            results.append({
                'Output Column': col,
                'Source Column': source_col,
                'Value': str(value)[:100] if pd.notna(value) else 'NULL'
            })
        
        # Display as table
        print("\n" + "=" * 100)
        print("QUERY RESULTS - Event Data Mapping")
        print("=" * 100 + "\n")
        print(tabulate(results, headers='keys', tablefmt='grid', maxcolwidths=[25, 40, 60]))
        
        # Save to CSV for reference
        results_df = pd.DataFrame(results)
        output_file = 'event_5b635469_data_output.csv'
        results_df.to_csv(output_file, index=False)
        print(f"\n✅ Results saved to: {output_file}")
        
        # Also save full dataframe
        full_output = 'event_5b635469_full_data.csv'
        df.to_csv(full_output, index=False)
        print(f"✅ Full data saved to: {full_output}")
        
        return df
        
    except Exception as e:
        print(f"\n❌ Error querying BigQuery: {str(e)}")
        print("\nPossible issues:")
        print("1. Authentication not configured (run: gcloud auth application-default login)")
        print("2. No access to wmt-assetprotection-prod project")
        print("3. Table names may have changed")
        print("4. Network/firewall issues")
        return None

if __name__ == "__main__":
    query_specific_event()
