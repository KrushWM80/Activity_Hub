# Calendar Dimension Integration Summary

## 🎯 Your Calendar Query Integration

Your provided calendar dimension query has been successfully integrated into the data pipeline system. Here's how it enhances your final visualization table:

### 📅 Original Calendar Query
```sql
SELECT CALENDAR_DATE, CAL_YEAR_NBR, FISCAL_YEAR_NBR, WM_WEEK_NBR, WM_QTR_NAME, WM_YEAR_NBR, 
       Today, Week_Day, Date_Day_number,
       date_add(current_date(), INTERVAL -(Date_Day_Number) DAY) as THE_DAY
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
    WHERE CALENDAR_DATE >= DATE_ADD(current_date, INTERVAL -7 YEAR)
      AND CALENDAR_DATE < DATE_ADD(current_date, INTERVAL 4 YEAR)
)
```

## 🔗 Integration with Primary Data

### Join Strategy
The calendar dimension joins with your primary store operations data on:
```sql
LEFT JOIN calendar_dim 
ON DATE(msg_start_dt) = CALENDAR_DATE
```

### Combined Query Example
```python
combined_config = {
    "primary_query": """
        SELECT *, 
               CURRENT_DATETIME('America/Chicago') as Last_Updated,
               DATE(msg_start_dt) as msg_date
        FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
        WHERE msg_start_dt >= DATE_ADD(CURRENT_DATE(), INTERVAL -40 DAY)
    """,
    "additional_tables": [
        {
            "name": "calendar_enhanced",
            "query": "YOUR_CALENDAR_QUERY_HERE"
        }
    ],
    "joins": [
        {
            "table": "calendar_enhanced", 
            "type": "left",
            "left_on": "msg_date",
            "right_on": "CALENDAR_DATE"
        }
    ]
}
```

## 📊 Enhanced Final Table Structure

After integration, your final visualization table includes:

### Original Store Operations Fields
- `msg_id` - Message identifier
- `store_nbr` - Store number
- `msg_type_cd` - Message type code  
- `msg_priority` - Message priority (1-10)
- `msg_start_dt` - Message start datetime
- `msg_end_dt` - Message end datetime
- `Last_Updated` - Current Chicago timezone timestamp

### Enhanced Calendar Fields
- `CALENDAR_DATE` - Calendar date
- `CAL_YEAR_NBR` - Calendar year
- `FISCAL_YEAR_NBR` - Walmart fiscal year
- `WM_WEEK_NBR` - Walmart week number (1-52)
- `WM_QTR_NAME` - Walmart quarter (Q1, Q2, Q3, Q4)
- `WM_YEAR_NBR` - Walmart year number
- `Today` - Current date
- `Week_Day` - Current day of week
- `Date_Day_number` - Custom day numbering (Sat=1, Sun=2, Mon=3...)
- `THE_DAY` - Calculated week boundary date

### Calculated Enhancement Fields
- `fiscal_quarter_year` - "Q1 FY2025" format
- `walmart_week_label` - "WW01" format  
- `is_current_fiscal_year` - Boolean flag
- `walmart_weekend` - Saturday/Sunday flag using custom numbering
- `days_from_today` - Days between calendar date and today

## 🎛️ Pipeline Configuration Examples

### 1. Basic Calendar Integration
```python
basic_calendar_config = {
    "primary_query": "YOUR_STORE_OPS_QUERY",
    "additional_tables": [{"name": "calendar", "query": "YOUR_CALENDAR_QUERY"}],
    "joins": [{"table": "calendar", "left_on": "msg_date", "right_on": "CALENDAR_DATE"}],
    "output": {"path": "store_ops_with_calendar", "format": "parquet"}
}
```

### 2. Fiscal Year Reporting
```python  
fiscal_config = {
    # ... same queries and joins ...
    "transformations": [
        {
            "type": "aggregate",
            "group_by": ["FISCAL_YEAR_NBR", "WM_QTR_NAME", "store_nbr"],
            "aggregations": {
                "msg_id": "count",
                "msg_priority": ["mean", "max"]
            }
        }
    ]
}
```

### 3. Weekly Trend Analysis
```python
weekly_config = {
    # ... same queries and joins ...
    "transformations": [
        {
            "type": "aggregate", 
            "group_by": ["WM_WEEK_NBR", "WM_YEAR_NBR", "msg_type_cd"],
            "aggregations": {
                "msg_id": "count",
                "store_nbr": "nunique"
            }
        }
    ]
}
```

## 📈 Visualization Benefits

### Dashboard Capabilities
1. **Fiscal Year Analysis** - Compare performance across Walmart fiscal years
2. **Walmart Week Trending** - Track weekly patterns using WM_WEEK_NBR
3. **Quarter-over-Quarter** - Analyze quarterly trends with WM_QTR_NAME  
4. **Custom Weekend Analysis** - Use Walmart's Saturday=1 day numbering
5. **Week Boundary Planning** - Leverage THE_DAY for week-end planning

### Sample Visualizations
- **Fiscal Quarter Performance**: Messages by `fiscal_quarter_year`
- **Weekly Heatmap**: `WM_WEEK_NBR` vs `msg_type_cd` 
- **Day Pattern Analysis**: `Date_Day_number` vs message volume
- **Current vs Prior Year**: Filter by `is_current_fiscal_year`

## 🚀 Usage Instructions

### Step 1: Configure Pipeline
```python
from data_pipeline import DataPipeline

pipeline = DataPipeline(config_path="pipeline_config.json")
```

### Step 2: Run Calendar-Enhanced Pipeline
```python
# Use any of the pre-built configurations
output_file = pipeline.run_pipeline(calendar_enhanced_config)
```

### Step 3: Load Results for Visualization
```python
import pandas as pd

# Load the enhanced dataset
df = pd.read_parquet(output_file)

# Now you have both operations data AND calendar dimensions
print(df[['msg_id', 'store_nbr', 'FISCAL_YEAR_NBR', 'WM_WEEK_NBR', 'walmart_weekend']].head())
```

## 📁 Generated Output Files

After running calendar-enhanced pipelines:

- `store_ops_calendar_enhanced.parquet` - Full dataset with calendar
- `fiscal_year_operations_report.xlsx` - Fiscal year summary  
- `weekly_trend_analysis_walmart_calendar.csv` - Weekly trends
- `complete_dashboard_dataset.parquet` - Visualization-ready table

## 🔍 Data Quality with Calendar

Additional validation rules for calendar integration:

```python
calendar_validation = [
    {"type": "not_null", "columns": ["FISCAL_YEAR_NBR", "WM_WEEK_NBR"]},
    {"type": "range", "column": "Date_Day_number", "min_value": 1, "max_value": 7},
    {"type": "range", "column": "FISCAL_YEAR_NBR", "min_value": 2018, "max_value": 2030}
]
```

## 💡 Key Insights Enabled

1. **Fiscal vs Calendar Analysis** - Understand how Walmart's fiscal calendar affects operations
2. **Week-over-Week Trends** - Use standardized WM_WEEK_NBR for consistent comparisons
3. **Seasonal Patterns** - Analyze by fiscal quarters that align with business cycles
4. **Weekend Operations** - Leverage custom day numbering for weekend analysis
5. **Current Period Focus** - Filter to current fiscal year/week for real-time insights

---

**The calendar dimension integration provides a comprehensive time-based framework for analyzing your store operations data, enabling sophisticated fiscal year reporting and trend analysis that aligns with Walmart's business calendar.**