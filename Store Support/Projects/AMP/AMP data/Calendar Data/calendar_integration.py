"""
Calendar Dimension Integration Examples
Author: GitHub Copilot
Date: October 24, 2025

This script demonstrates various ways to integrate the calendar dimension
with your store operations data for enhanced time-based analysis.
"""

from data_pipeline import DataPipeline
import pandas as pd
from datetime import datetime
import json

def create_fiscal_reporting_pipeline():
    """
    Create a pipeline specifically for fiscal year reporting using calendar dimension
    """
    print("=== Fiscal Year Reporting Pipeline ===")
    
    pipeline = DataPipeline(config_path="pipeline_config.json")
    
    fiscal_config = {
        "name": "Fiscal Year Store Operations Report",
        "primary_query": """
            SELECT *, 
                   CURRENT_DATETIME('America/Chicago') as Last_Updated,
                   DATE(msg_start_dt) as msg_date,
                   EXTRACT(HOUR FROM msg_start_dt) as msg_hour,
                   EXTRACT(DAYOFWEEK FROM msg_start_dt) as msg_dayofweek
            FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
            WHERE msg_start_dt >= DATE_ADD(CURRENT_DATE(), INTERVAL -40 DAY)
        """,
        "additional_tables": [
            {
                "name": "walmart_calendar",
                "query": """
                    SELECT CALENDAR_DATE, CAL_YEAR_NBR, FISCAL_YEAR_NBR, WM_WEEK_NBR, WM_QTR_NAME, WM_YEAR_NBR, 
                           Today, Week_Day, Date_Day_number,
                           date_add(current_date(), INTERVAL -(Date_Day_Number) DAY) as THE_DAY
                    FROM (
                        SELECT CALENDAR_DATE, CAL_YEAR_NBR, FISCAL_YEAR_NBR, WM_WEEK_NBR, WM_QTR_NAME, WM_YEAR_NBR, 
                               current_date() as Today,
                               extract(dayofweek from current_date) as Week_Day,
                               CASE 
                                   WHEN extract(dayofweek from current_date)=7 THEN 1
                                   WHEN extract(dayofweek from current_date)=1 THEN 2
                                   WHEN extract(dayofweek from current_date)=2 THEN 3
                                   WHEN extract(dayofweek from current_date)=3 THEN 4
                                   WHEN extract(dayofweek from current_date)=4 THEN 5
                                   WHEN extract(dayofweek from current_date)=5 THEN 6
                                   WHEN extract(dayofweek from current_date)=6 THEN 7
                               END as Date_Day_Number
                        FROM `wmt-edw-prod.US_CORE_DIM_VM.CALENDAR_DIM`
                        WHERE CALENDAR_DATE >= DATE_ADD(current_date(), INTERVAL -7 YEAR)
                          AND CALENDAR_DATE < DATE_ADD(current_date(), INTERVAL 4 YEAR)
                    )
                """
            }
        ],
        "joins": [
            {
                "table": "walmart_calendar",
                "type": "left",
                "left_on": "msg_date",
                "right_on": "CALENDAR_DATE"
            }
        ],
        "transformations": [
            {
                "type": "calculate_column",
                "column_name": "fiscal_period_label",
                "expression": "'FY' + FISCAL_YEAR_NBR.astype(str) + '-' + WM_QTR_NAME"
            },
            {
                "type": "calculate_column",
                "column_name": "walmart_week_label", 
                "expression": "'WW' + WM_WEEK_NBR.astype(str).str.zfill(2)"
            },
            {
                "type": "calculate_column",
                "column_name": "is_current_walmart_week",
                "expression": "WM_WEEK_NBR == pd.to_datetime(THE_DAY).dt.isocalendar().week"
            },
            {
                "type": "calculate_column",
                "column_name": "days_until_week_end",
                "expression": "7 - Date_Day_Number"
            }
        ],
        "output": {
            "path": "fiscal_year_operations_report",
            "format": "excel"
        }
    }
    
    return fiscal_config

def create_weekly_trend_pipeline():
    """
    Create a pipeline for weekly trend analysis using Walmart week numbering
    """
    print("\n=== Weekly Trend Analysis Pipeline ===")
    
    weekly_config = {
        "name": "Weekly Trend Analysis with Walmart Calendar",
        "primary_query": """
            SELECT *, 
                   CURRENT_DATETIME('America/Chicago') as Last_Updated,
                   DATE(msg_start_dt) as msg_date
            FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
            WHERE msg_start_dt >= DATE_ADD(CURRENT_DATE(), INTERVAL -40 DAY)
        """,
        "additional_tables": [
            {
                "name": "calendar_weekly",
                "query": """
                    SELECT CALENDAR_DATE, CAL_YEAR_NBR, FISCAL_YEAR_NBR, WM_WEEK_NBR, WM_QTR_NAME, WM_YEAR_NBR, 
                           Today, Week_Day, Date_Day_number,
                           date_add(current_date(), INTERVAL -(Date_Day_Number) DAY) as THE_DAY
                    FROM (
                        SELECT CALENDAR_DATE, CAL_YEAR_NBR, FISCAL_YEAR_NBR, WM_WEEK_NBR, WM_QTR_NAME, WM_YEAR_NBR, 
                               current_date() as Today,
                               extract(dayofweek from current_date) as Week_Day,
                               CASE 
                                   WHEN extract(dayofweek from current_date)=7 THEN 1
                                   WHEN extract(dayofweek from current_date)=1 THEN 2
                                   WHEN extract(dayofweek from current_date)=2 THEN 3
                                   WHEN extract(dayofweek from current_date)=3 THEN 4
                                   WHEN extract(dayofweek from current_date)=4 THEN 5
                                   WHEN extract(dayofweek from current_date)=5 THEN 6
                                   WHEN extract(dayofweek from current_date)=6 THEN 7
                               END as Date_Day_Number
                        FROM `wmt-edw-prod.US_CORE_DIM_VM.CALENDAR_DIM`
                        WHERE CALENDAR_DATE >= DATE_ADD(current_date(), INTERVAL -7 YEAR)
                          AND CALENDAR_DATE < DATE_ADD(current_date(), INTERVAL 4 YEAR)
                    )
                """
            }
        ],
        "joins": [
            {
                "table": "calendar_weekly",
                "type": "left", 
                "left_on": "msg_date",
                "right_on": "CALENDAR_DATE"
            }
        ],
        "transformations": [
            {
                "type": "aggregate",
                "group_by": ["WM_WEEK_NBR", "WM_YEAR_NBR", "msg_type_cd"],
                "aggregations": {
                    "msg_id": "count",
                    "store_nbr": "nunique",
                    "msg_priority": ["mean", "max"]
                }
            },
            {
                "type": "rename_columns",
                "mapping": {
                    "msg_id": "total_messages_per_week",
                    "store_nbr": "unique_stores_affected",
                    "msg_priority_mean": "avg_priority",
                    "msg_priority_max": "max_priority"
                }
            },
            {
                "type": "calculate_column",
                "column_name": "week_identifier",
                "expression": "'WW' + WM_WEEK_NBR.astype(str).str.zfill(2) + '-' + WM_YEAR_NBR.astype(str)"
            }
        ],
        "output": {
            "path": "weekly_trend_analysis_walmart_calendar",
            "format": "csv"
        }
    }
    
    return weekly_config

def create_day_of_week_analysis():
    """
    Create analysis based on the custom day numbering logic from calendar dimension
    """
    print("\n=== Day of Week Analysis Pipeline ===")
    
    dow_config = {
        "name": "Day of Week Analysis with Custom Numbering",
        "primary_query": """
            SELECT *, 
                   CURRENT_DATETIME('America/Chicago') as Last_Updated,
                   DATE(msg_start_dt) as msg_date,
                   EXTRACT(DAYOFWEEK FROM msg_start_dt) as standard_dayofweek
            FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
            WHERE msg_start_dt >= DATE_ADD(CURRENT_DATE(), INTERVAL -40 DAY)
        """,
        "additional_tables": [
            {
                "name": "calendar_dow", 
                "query": """
                    SELECT CALENDAR_DATE, CAL_YEAR_NBR, FISCAL_YEAR_NBR, WM_WEEK_NBR, WM_QTR_NAME, WM_YEAR_NBR, 
                           Today, Week_Day, Date_Day_number,
                           date_add(current_date(), INTERVAL -(Date_Day_Number) DAY) as THE_DAY,
                           CASE Date_Day_Number
                               WHEN 1 THEN 'Saturday'
                               WHEN 2 THEN 'Sunday' 
                               WHEN 3 THEN 'Monday'
                               WHEN 4 THEN 'Tuesday'
                               WHEN 5 THEN 'Wednesday'
                               WHEN 6 THEN 'Thursday'
                               WHEN 7 THEN 'Friday'
                           END as walmart_day_name
                    FROM (
                        SELECT CALENDAR_DATE, CAL_YEAR_NBR, FISCAL_YEAR_NBR, WM_WEEK_NBR, WM_QTR_NAME, WM_YEAR_NBR, 
                               current_date() as Today,
                               extract(dayofweek from current_date) as Week_Day,
                               CASE 
                                   WHEN extract(dayofweek from current_date)=7 THEN 1  -- Saturday = 1
                                   WHEN extract(dayofweek from current_date)=1 THEN 2  -- Sunday = 2
                                   WHEN extract(dayofweek from current_date)=2 THEN 3  -- Monday = 3
                                   WHEN extract(dayofweek from current_date)=3 THEN 4  -- Tuesday = 4
                                   WHEN extract(dayofweek from current_date)=4 THEN 5  -- Wednesday = 5
                                   WHEN extract(dayofweek from current_date)=5 THEN 6  -- Thursday = 6
                                   WHEN extract(dayofweek from current_date)=6 THEN 7  -- Friday = 7
                               END as Date_Day_Number
                        FROM `wmt-edw-prod.US_CORE_DIM_VM.CALENDAR_DIM`
                        WHERE CALENDAR_DATE >= DATE_ADD(current_date(), INTERVAL -7 YEAR)
                          AND CALENDAR_DATE < DATE_ADD(current_date(), INTERVAL 4 YEAR)
                    )
                """
            }
        ],
        "joins": [
            {
                "table": "calendar_dow",
                "type": "left",
                "left_on": "msg_date", 
                "right_on": "CALENDAR_DATE"
            }
        ],
        "transformations": [
            {
                "type": "calculate_column",
                "column_name": "is_weekend_walmart",
                "expression": "Date_Day_Number.isin([1, 2])"  # Saturday and Sunday
            },
            {
                "type": "calculate_column", 
                "column_name": "is_weekday_walmart",
                "expression": "Date_Day_Number.isin([3, 4, 5, 6, 7])"  # Monday through Friday
            },
            {
                "type": "aggregate",
                "group_by": ["walmart_day_name", "msg_type_cd"],
                "aggregations": {
                    "msg_id": "count",
                    "msg_priority": "mean",
                    "store_nbr": "nunique"
                }
            }
        ],
        "output": {
            "path": "day_of_week_analysis_walmart_calendar",
            "format": "parquet"
        }
    }
    
    return dow_config

def create_dashboard_ready_table():
    """
    Create a comprehensive table ready for dashboard visualization
    """
    print("\n=== Dashboard-Ready Table Pipeline ===")
    
    dashboard_config = {
        "name": "Complete Dashboard Dataset with Calendar Enhancement",
        "primary_query": """
            SELECT *, 
                   CURRENT_DATETIME('America/Chicago') as Last_Updated,
                   DATE(msg_start_dt) as msg_date,
                   EXTRACT(HOUR FROM msg_start_dt) as msg_hour
            FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
            WHERE msg_start_dt >= DATE_ADD(CURRENT_DATE(), INTERVAL -40 DAY)
        """,
        "additional_tables": [
            {
                "name": "calendar_complete",
                "query": """
                    SELECT CALENDAR_DATE, CAL_YEAR_NBR, FISCAL_YEAR_NBR, WM_WEEK_NBR, WM_QTR_NAME, WM_YEAR_NBR, 
                           Today, Week_Day, Date_Day_number,
                           date_add(current_date(), INTERVAL -(Date_Day_Number) DAY) as THE_DAY
                    FROM (
                        SELECT CALENDAR_DATE, CAL_YEAR_NBR, FISCAL_YEAR_NBR, WM_WEEK_NBR, WM_QTR_NAME, WM_YEAR_NBR, 
                               current_date() as Today,
                               extract(dayofweek from current_date) as Week_Day,
                               CASE 
                                   WHEN extract(dayofweek from current_date)=7 THEN 1
                                   WHEN extract(dayofweek from current_date)=1 THEN 2
                                   WHEN extract(dayofweek from current_date)=2 THEN 3
                                   WHEN extract(dayofweek from current_date)=3 THEN 4
                                   WHEN extract(dayofweek from current_date)=4 THEN 5
                                   WHEN extract(dayofweek from current_date)=5 THEN 6
                                   WHEN extract(dayofweek from current_date)=6 THEN 7
                               END as Date_Day_Number
                        FROM `wmt-edw-prod.US_CORE_DIM_VM.CALENDAR_DIM`
                        WHERE CALENDAR_DATE >= DATE_ADD(current_date(), INTERVAL -7 YEAR)
                          AND CALENDAR_DATE < DATE_ADD(current_date(), INTERVAL 4 YEAR)
                    )
                """
            },
            {
                "name": "store_business_unit",
                "query": """
                    SELECT
                        CAST(business_unit_nbr AS NUMERIC) AS STORE_NBR,
                        physical_city AS CITY_NAME,
                        LEFT(physical_zip_code,5) AS POSTAL_CODE,
                        region_code AS REGION_NBR,
                        martket_code AS MARKET_AREA_NBR,
                        format_code,
                        CASE subdivision_code
                            WHEN 'A' THEN 'SOUTHEAST BU'
                            WHEN 'B' THEN 'SOUTHWEST BU'
                            WHEN 'C' THEN 'FORMAT DEVELOPMENT'
                            WHEN 'D' THEN 'STORE NO 8'
                            WHEN 'E' THEN 'NORTH BU'
                            WHEN 'F' THEN 'EAST BU'
                            WHEN 'G' THEN 'RETAIL SUBDIVISION G'
                            WHEN 'M' THEN 'WEST BU'
                            WHEN 'O' THEN 'NHM BU'
                            WHEN 'X' THEN 'US Retail SD X'
                            WHEN 'I' THEN 'PR BU'
                            WHEN 'Z' THEN 'RX Facilities'
                            ELSE subdivision_code
                        END AS SUBDIV_NAME,
                        banner_code AS BANNER_CODE,
                        banner_desc AS BANNER_DESC,
                        banner_code AS STORE_TYPE_CODE,
                        banner_desc AS STORE_TYPE_DESC,
                        bu_status_code AS OPEN_STATUS_CODE,
                        bu_status_desc AS OPEN_STATUS_DESC,
                        physical_county AS COUNTY_NAME,
                        physical_country_code AS COUNTRY_CODE,
                        physical_state_code AS STATE_PROV_CODE,
                        LATITUDE AS LATITUDE_DGR,
                        longitude AS LONGITUDE_DGR
                    FROM `wmt-loc-cat-prod.catalog_location_views.businessunit_view`
                    WHERE physical_country_code = 'US'
                        AND base_division_desc = "WAL-MART STORES INC."
                        AND bu_status_desc != 'CLOSED'
                        AND Date(operational_open_start_date) <= date_add(current_date(), Interval 90 day)
                """
            }
        ],
        "joins": [
            {
                "table": "calendar_complete",
                "type": "left",
                "left_on": "msg_date",
                "right_on": "CALENDAR_DATE"
            },
            {
                "table": "store_business_unit",
                "type": "left",
                "left_on": "store_nbr",
                "right_on": "STORE_NBR"
            }
        ],
        "transformations": [
            # Calendar-based transformations
            {
                "type": "calculate_column",
                "column_name": "fiscal_quarter_year",
                "expression": "WM_QTR_NAME + ' FY' + FISCAL_YEAR_NBR.astype(str)"
            },
            {
                "type": "calculate_column",
                "column_name": "walmart_week_full",
                "expression": "'WW' + WM_WEEK_NBR.astype(str).str.zfill(2) + '-' + WM_YEAR_NBR.astype(str)"
            },
            {
                "type": "calculate_column",
                "column_name": "is_current_fiscal_year",
                "expression": "FISCAL_YEAR_NBR == (pd.Timestamp.now().year + (1 if pd.Timestamp.now().month >= 2 else 0))"
            },
            {
                "type": "calculate_column",
                "column_name": "days_from_today",
                "expression": "(pd.Timestamp.now().normalize() - pd.to_datetime(CALENDAR_DATE)).dt.days"
            },
            # Business logic transformations  
            {
                "type": "calculate_column",
                "column_name": "urgency_level",
                "expression": "pd.cut(msg_priority, bins=[0, 3, 6, 8, 10], labels=['Low', 'Medium', 'High', 'Critical'])"
            },
            {
                "type": "calculate_column",
                "column_name": "is_business_hours",
                "expression": "(msg_hour >= 8) & (msg_hour <= 17)"
            },
            {
                "type": "calculate_column",
                "column_name": "walmart_weekend",
                "expression": "Date_Day_Number.isin([1, 2])"
            }
        ],
        "validation": [
            {
                "type": "not_null",
                "columns": ["FISCAL_YEAR_NBR", "WM_WEEK_NBR", "msg_id", "store_nbr"]
            },
            {
                "type": "range",
                "column": "Date_Day_Number", 
                "min_value": 1,
                "max_value": 7
            }
        ],
        "output": {
            "path": "complete_dashboard_dataset",
            "format": "parquet"
        }
    }
    
    return dashboard_config

def main():
    """
    Main function to demonstrate all calendar integration examples
    """
    print("Calendar Dimension Integration Examples")
    print("=" * 60)
    print("Demonstrating integration of Walmart calendar dimension")
    print("with store operations data for enhanced analytics\n")
    
    pipeline = DataPipeline(config_path="pipeline_config.json")
    
    # Create all configuration examples
    configs = {
        "fiscal_reporting": create_fiscal_reporting_pipeline(),
        "weekly_trends": create_weekly_trend_pipeline(), 
        "day_of_week": create_day_of_week_analysis(),
        "dashboard_ready": create_dashboard_ready_table()
    }
    
    # Save configuration templates
    with open('calendar_pipeline_configs.json', 'w') as f:
        json.dump(configs, f, indent=2, default=str)
    
    print("✅ Created calendar integration configurations:")
    print("   - Fiscal year reporting pipeline")
    print("   - Weekly trend analysis with Walmart weeks")
    print("   - Day-of-week analysis with custom numbering")
    print("   - Complete dashboard-ready dataset")
    
    print(f"\n📁 Configuration templates saved to: calendar_pipeline_configs.json")
    
    print("\n🎯 Key Calendar Dimension Features:")
    print("   ✅ Fiscal year vs calendar year analysis")
    print("   ✅ Walmart week numbering (WW01-WW52)")
    print("   ✅ Custom day-of-week numbering (Saturday=1)")
    print("   ✅ Quarter and period calculations")
    print("   ✅ Day calculations from current date")
    print("   ✅ THE_DAY field for week boundaries")
    
    print("\n🚀 To run these pipelines:")
    print("   1. Set up BigQuery authentication")
    print("   2. Load desired config: pipeline.run_pipeline(configs['fiscal_reporting'])")
    print("   3. Or run all: python pipeline_examples.py")
    
    print("\n📊 Output files will include:")
    print("   - fiscal_year_operations_report.xlsx")
    print("   - weekly_trend_analysis_walmart_calendar.csv")
    print("   - day_of_week_analysis_walmart_calendar.parquet")
    print("   - complete_dashboard_dataset.parquet")

if __name__ == "__main__":
    main()