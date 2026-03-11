"""BigQuery service for Store Meeting Planner"""
import os
import uuid
from datetime import datetime, date, timedelta
from typing import Optional
from google.cloud import bigquery


PROJECT_ID = os.getenv("GCP_PROJECT_ID", "wmt-assetprotection-prod")
DATASET_ID = os.getenv("BIGQUERY_DATASET", "Store_Support_Dev")

# Table references
AMP_TABLE = f"`{PROJECT_ID}.{DATASET_ID}.Output - AMP ALL 2`"
REQUEST_TABLE = f"`{PROJECT_ID}.{DATASET_ID}.store_meeting_request_data`"
CAL_DIM_TABLE = f"`{PROJECT_ID}.{DATASET_ID}.Cal_Dim_Data`"
STORE_CUR_TABLE = f"`{PROJECT_ID}.{DATASET_ID}.Store_Cur_Data`"

REGULAR_MAX_SLOTS = 20
PROTECTED_MAX_SLOTS = 10


class DatabaseService:
    def __init__(self):
        self.client = None
        self._connect()

    def _connect(self):
        try:
            creds_path = os.getenv(
                "GOOGLE_APPLICATION_CREDENTIALS",
                os.path.expanduser("~\\AppData\\Roaming\\gcloud\\application_default_credentials.json")
            )
            if os.path.exists(creds_path):
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path
            self.client = bigquery.Client(project=PROJECT_ID)
            print(f"[DB] Connected to BigQuery project: {PROJECT_ID}")
        except Exception as e:
            print(f"[DB] BigQuery connection error: {e}")
            self.client = None

    def is_connected(self) -> bool:
        return self.client is not None

    def _run_query(self, query: str, params: list = None) -> list:
        if not self.client:
            print("[DB] No BigQuery client available")
            return []
        try:
            job_config = bigquery.QueryJobConfig()
            if params:
                job_config.query_parameters = params
            result = self.client.query(query, job_config=job_config)
            return [dict(row) for row in result]
        except Exception as e:
            print(f"[DB] Query error: {e}")
            return []

    # =========================================
    # CALENDAR & PROTECTED WEEKS
    # =========================================

    def get_calendar_events(self, start_date: str, end_date: str) -> list:
        """Get AMP Calendar Events for display on the calendar."""
        query = f"""
            SELECT
                event_id,
                Activity_Title as title,
                Message_Type as message_type,
                Start_Date as start_date,
                End_Date as end_date,
                Business_Area as business_area,
                Author as author,
                Store_Cnt as store_cnt,
                WM_Week as wm_week,
                WM_Year as wm_year,
                Web_Preview as preview_url
            FROM {AMP_TABLE}
            WHERE Message_Type = 'Calendar Event'
              AND Message_Status = 'Published'
              AND Start_Date <= @end_date
              AND End_Date >= @start_date
            ORDER BY Start_Date
        """
        params = [
            bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
            bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
        ]
        rows = self._run_query(query, params)
        for row in rows:
            title = (row.get("title") or "").lower()
            row["is_protected_week"] = "protected week" in title
        return rows

    def get_protected_weeks(self, fiscal_year: int) -> list:
        """Get Protected Week dates from AMP ALL 2."""
        query = f"""
            SELECT DISTINCT
                Activity_Title as title,
                Start_Date as start_date,
                End_Date as end_date,
                WM_Week as wm_week,
                WM_Year as wm_year
            FROM {AMP_TABLE}
            WHERE LOWER(Activity_Title) LIKE '%protected week%'
              AND Message_Type = 'Calendar Event'
              AND Message_Status = 'Published'
              AND CAST(WM_Year AS INT64) = @fiscal_year
            ORDER BY Start_Date
        """
        params = [
            bigquery.ScalarQueryParameter("fiscal_year", "INT64", fiscal_year),
        ]
        return self._run_query(query, params)

    def get_protected_week_dates(self) -> set:
        """Returns a set of date strings (YYYY-MM-DD) that fall in protected weeks."""
        query = f"""
            SELECT DISTINCT
                Start_Date as pw_start,
                End_Date as pw_end
            FROM {AMP_TABLE}
            WHERE LOWER(Activity_Title) LIKE '%protected week%'
              AND Message_Type = 'Calendar Event'
              AND Message_Status = 'Published'
        """
        rows = self._run_query(query)
        protected_dates = set()
        for row in rows:
            start = row.get("pw_start")
            end = row.get("pw_end")
            if start and end:
                current = start
                while current <= end:
                    protected_dates.add(current.isoformat() if hasattr(current, 'isoformat') else str(current))
                    current += timedelta(days=1)
        return protected_dates

    def get_slot_availability(self, start_date: str, end_date: str) -> list:
        """Get slot availability for a date range."""
        query = f"""
            SELECT
                DATE(`Start Date`) as request_date,
                COUNT(*) as approved_count
            FROM {REQUEST_TABLE}
            WHERE Status = 'Approved'
              AND DATE(`Start Date`) >= @start_date
              AND DATE(`Start Date`) <= @end_date
            GROUP BY DATE(`Start Date`)
        """
        params = [
            bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
            bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
        ]
        approved = {str(r["request_date"]): r["approved_count"] for r in self._run_query(query, params)}

        protected_dates = self.get_protected_week_dates()

        cal_query = f"""
            SELECT
                CALENDAR_DATE,
                WM_WEEK_NBR,
                FISCAL_YEAR_NBR,
                WM_YEAR_NBR
            FROM {CAL_DIM_TABLE}
            WHERE CALENDAR_DATE >= @start_date
              AND CALENDAR_DATE <= @end_date
            ORDER BY CALENDAR_DATE
        """
        cal_rows = self._run_query(cal_query, params)

        slots = []
        for row in cal_rows:
            cal_date = str(row["CALENDAR_DATE"])
            is_protected = cal_date in protected_dates
            day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            try:
                dt = datetime.strptime(cal_date, "%Y-%m-%d")
                dow = day_names[dt.weekday()]
            except Exception:
                dow = ""

            slots.append({
                "date": cal_date,
                "day_of_week": dow,
                "approved_count": approved.get(cal_date, 0),
                "max_slots": PROTECTED_MAX_SLOTS if is_protected else REGULAR_MAX_SLOTS,
                "is_protected_week": is_protected,
                "wm_week": row.get("WM_WEEK_NBR"),
                "fiscal_year": row.get("FISCAL_YEAR_NBR"),
            })
        return slots

    # =========================================
    # REQUESTS CRUD
    # =========================================

    def _normalize_request_row(self, row: dict) -> dict:
        """Normalize BQ space-named columns to underscore keys for the API."""
        mapping = {
            "AMP Activity": "AMP_Activity",
            "AMP Activity URL": "AMP_Activity_URL",
            "Start Date": "Start_Date",
            "End Date": "End_Date",
            "Meeting Duration": "Meeting_Duration",
            "Meeting Type": "Meeting_Type",
            "Impacted Shift": "Impacted_Shift",
            "Store Selection": "Store_Selection",
            "Meeting Reoccurrence": "Meeting_Reoccurrence",
            "Meeting Link": "Meeting_Link",
            "Start Time": "Start_Time",
            "AMP Input": "AMP_Input",
            "Meeting Day of the Week": "Meeting_Day_of_the_Week",
            "Submission Start time": "Submission_Start_time",
            "Color Tag": "Color_Tag",
            "Compliance Asset Id": "Compliance_Asset_Id",
            "Completion time": "Completion_time",
            "Created By": "Created_By",
            "Modified By": "Modified_By",
            "Planner Cadence": "Planner_Cadence",
            "Primary Language": "Primary_Language",
            "Role Type": "Role_Type",
        }
        normalized = {}
        for k, v in row.items():
            new_key = mapping.get(k, k)
            normalized[new_key] = v
        return normalized

    def _add_source_info(self, row: dict) -> dict:
        """Add source and preview_url derived fields."""
        row["source"] = "AMP" if row.get("AMP_Activity") else "Form"
        if row.get("AMP_Activity") and row.get("AMP_Activity_URL"):
            url = row["AMP_Activity_URL"]
            row["preview_url"] = url.replace("/message/", "/preview/") if "/message/" in url else ""
        else:
            row["preview_url"] = ""
        return row

    def get_all_requests(self, status: str = None, source: str = None,
                         meeting_type: str = None, start_date: str = None,
                         end_date: str = None) -> list:
        """Admin: get all requests with optional filters."""
        conditions = ["1=1"]
        params = []

        if status:
            conditions.append("Status = @status")
            params.append(bigquery.ScalarQueryParameter("status", "STRING", status))
        if meeting_type:
            conditions.append("`Meeting Type` = @meeting_type")
            params.append(bigquery.ScalarQueryParameter("meeting_type", "STRING", meeting_type))
        if start_date:
            conditions.append("DATE(`Start Date`) >= @filter_start")
            params.append(bigquery.ScalarQueryParameter("filter_start", "DATE", start_date))
        if end_date:
            conditions.append("DATE(`Start Date`) <= @filter_end")
            params.append(bigquery.ScalarQueryParameter("filter_end", "DATE", end_date))

        where = " AND ".join(conditions)
        query = f"""
            SELECT *
            FROM {REQUEST_TABLE}
            WHERE {where}
            ORDER BY
                CASE Status
                    WHEN 'Review' THEN 1
                    WHEN 'Pending' THEN 2
                    WHEN 'Needs Changes' THEN 3
                    WHEN 'Approved' THEN 4
                    WHEN 'Rejected' THEN 5
                END,
                `Start Date` DESC
        """
        rows = self._run_query(query, params if params else None)
        return [self._add_source_info(self._normalize_request_row(r)) for r in rows]

    def get_user_requests(self, email: str) -> list:
        """Get requests for a specific user."""
        query = f"""
            SELECT *
            FROM {REQUEST_TABLE}
            WHERE LOWER(Email) = LOWER(@email)
            ORDER BY `Start Date` DESC
        """
        params = [bigquery.ScalarQueryParameter("email", "STRING", email)]
        rows = self._run_query(query, params)
        return [self._add_source_info(self._normalize_request_row(r)) for r in rows]

    def submit_request(self, data: dict, email: str, name: str) -> dict:
        """Insert a new meeting request from the intake form."""
        now = datetime.utcnow().isoformat()
        request_id = str(uuid.uuid4())[:8].upper()

        # Keys must match BQ column names (with spaces)
        row = {
            "ID": request_id,
            "Title": data.get("Title", ""),
            "Email": email,
            "Name": name,
            "AMP Activity": data.get("AMP_Activity", False),
            "AMP Activity URL": data.get("AMP_Activity_URL", ""),
            "Start Date": data.get("Start_Date"),
            "End Date": data.get("End_Date"),
            "Meeting Duration": data.get("Meeting_Duration"),
            "Meeting Type": data.get("Meeting_Type", ""),
            "Impacted Shift": data.get("Impacted_Shift"),
            "Store Selection": data.get("Store_Selection", ""),
            "Meeting Reoccurrence": data.get("Meeting_Reoccurrence", "None"),
            "Status": "Review",
            "Submission Start time": now,
            "Created": now,
            "Created By": email,
            "Modified": now,
            "Modified By": email,
            "AMP Input": "",
            "Start Time": "",
            "Meeting Link": "",
            "Planner Cadence": "",
            "Primary Language": "",
            "Role Type": "",
            "Meeting Day of the Week": "",
            "Color Tag": "",
            "Compliance Asset Id": "",
            "Completion time": "",
            "Version": "1",
        }

        # Derive day of week from start date
        try:
            dt = datetime.strptime(str(data.get("Start_Date", "")), "%Y-%m-%d")
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            row["Meeting Day of the Week"] = days[dt.weekday()]
        except Exception:
            pass

        table_ref = f"{PROJECT_ID}.{DATASET_ID}.store_meeting_request_data"
        errors = self.client.insert_rows_json(table_ref, [row])
        if errors:
            print(f"[DB] Insert errors: {errors}")
            return {"error": str(errors)}
        return {"id": request_id, "status": "Review"}

    def update_request(self, request_id: str, updates: dict, admin_email: str) -> dict:
        """Admin: update a request (status, comment, start_time, meeting_link)."""
        set_clauses = ["Modified = @modified", "`Modified By` = @admin_email"]
        params = [
            bigquery.ScalarQueryParameter("request_id", "STRING", request_id),
            bigquery.ScalarQueryParameter("modified", "STRING", datetime.utcnow().isoformat()),
            bigquery.ScalarQueryParameter("admin_email", "STRING", admin_email),
        ]

        if "status" in updates:
            set_clauses.append("Status = @new_status")
            params.append(bigquery.ScalarQueryParameter("new_status", "STRING", updates["status"]))
        if "start_time" in updates and updates["start_time"]:
            set_clauses.append("`Start Time` = @start_time")
            params.append(bigquery.ScalarQueryParameter("start_time", "STRING", updates["start_time"]))
        if "meeting_link" in updates and updates["meeting_link"]:
            set_clauses.append("`Meeting Link` = @meeting_link")
            params.append(bigquery.ScalarQueryParameter("meeting_link", "STRING", updates["meeting_link"]))
        if "comment" in updates and updates["comment"]:
            set_clauses.append("`AMP Input` = CONCAT(IFNULL(`AMP Input`, ''), @comment_entry)")
            comment_entry = f"\n[{datetime.utcnow().strftime('%Y-%m-%d %H:%M')} | {admin_email}] {updates['comment']}"
            params.append(bigquery.ScalarQueryParameter("comment_entry", "STRING", comment_entry))

        set_clause = ", ".join(set_clauses)
        query = f"""
            UPDATE {REQUEST_TABLE}
            SET {set_clause}
            WHERE ID = @request_id
        """
        self._run_query(query, params)
        return {"id": request_id, "updated": True}

    def complete_pending_request(self, request_id: str, updates: dict, user_email: str) -> dict:
        """User completes missing fields on a Pending request."""
        set_clauses = ["Modified = @modified", "`Modified By` = @user_email"]
        params = [
            bigquery.ScalarQueryParameter("request_id", "STRING", request_id),
            bigquery.ScalarQueryParameter("modified", "STRING", datetime.utcnow().isoformat()),
            bigquery.ScalarQueryParameter("user_email", "STRING", user_email),
        ]

        # BQ column name (with spaces) -> param type, API key
        field_map = {
            "Meeting Type": ("STRING", "Meeting_Type"),
            "Impacted Shift": ("INT64", "Impacted_Shift"),
            "Store Selection": ("STRING", "Store_Selection"),
            "Meeting Duration": ("INT64", "Meeting_Duration"),
            "Start Date": ("STRING", "Start_Date"),
            "End Date": ("STRING", "End_Date"),
        }

        for bq_col, (field_type, api_key) in field_map.items():
            if api_key in updates and updates[api_key] is not None:
                param_name = api_key.lower()
                set_clauses.append(f"`{bq_col}` = @{param_name}")
                params.append(bigquery.ScalarQueryParameter(param_name, field_type, updates[api_key]))

        # Check completeness
        from models import check_completeness
        current = self.get_request_by_id(request_id)
        is_complete = False
        if current:
            merged = {**current, **{k: v for k, v in updates.items() if v is not None}}
            is_complete, missing = check_completeness(merged)
            if is_complete:
                set_clauses.append("Status = 'Review'")
                set_clauses.append("`AMP Input` = ''")
            else:
                missing_str = f"Missing: {', '.join(missing)}"
                set_clauses.append("`AMP Input` = @missing_note")
                params.append(bigquery.ScalarQueryParameter("missing_note", "STRING", missing_str))

        set_clause = ", ".join(set_clauses)
        query = f"""
            UPDATE {REQUEST_TABLE}
            SET {set_clause}
            WHERE ID = @request_id
        """
        self._run_query(query, params)
        return {"id": request_id, "status": "Review" if is_complete else "Pending"}

    def get_request_by_id(self, request_id: str) -> dict:
        query = f"SELECT * FROM {REQUEST_TABLE} WHERE ID = @request_id LIMIT 1"
        params = [bigquery.ScalarQueryParameter("request_id", "STRING", request_id)]
        rows = self._run_query(query, params)
        return self._normalize_request_row(rows[0]) if rows else None

    # =========================================
    # AMP INGESTION
    # =========================================

    def get_amp_meeting_planner_events(self) -> list:
        """Get AMP events that contain Meeting Planner data in Keyword_Tags."""
        query = f"""
            SELECT
                event_id,
                Activity_Title as title,
                Message_Type as message_type,
                Start_Date as start_date,
                End_Date as end_date,
                Business_Area as business_area,
                Author as author,
                Author_email as activity_email,
                Store_Cnt as store_cnt,
                WM_Week as wm_week,
                WM_Year as wm_year,
                Keyword_Tags as keywords,
                Web_Preview as preview_url,
                Edit_Link as edit_link,
                MP_Date as mp_date,
                MP_Duration as mp_duration,
                MP_Start_Datetime as mp_start_datetime,
                MP_End_Datetime as mp_end_datetime,
                MP_Timezone as mp_timezone
            FROM {AMP_TABLE}
            WHERE LOWER(Keyword_Tags) LIKE '%meeting planner%'
              AND Message_Status = 'Published'
            ORDER BY Start_Date DESC
        """
        return self._run_query(query)

    def get_existing_amp_urls(self) -> set:
        """Get AMP Activity URLs already in store_meeting_request_data."""
        query = f"""
            SELECT DISTINCT `AMP Activity URL`
            FROM {REQUEST_TABLE}
            WHERE `AMP Activity` = TRUE
              AND `AMP Activity URL` IS NOT NULL
              AND `AMP Activity URL` != ''
        """
        rows = self._run_query(query)
        return {r["AMP Activity URL"] for r in rows}

    def _to_bq_keys(self, row: dict) -> dict:
        """Convert underscore API keys back to BQ space-named columns."""
        reverse_mapping = {
            "AMP_Activity": "AMP Activity",
            "AMP_Activity_URL": "AMP Activity URL",
            "Start_Date": "Start Date",
            "End_Date": "End Date",
            "Meeting_Duration": "Meeting Duration",
            "Meeting_Type": "Meeting Type",
            "Impacted_Shift": "Impacted Shift",
            "Store_Selection": "Store Selection",
            "Meeting_Reoccurrence": "Meeting Reoccurrence",
            "Meeting_Link": "Meeting Link",
            "Start_Time": "Start Time",
            "AMP_Input": "AMP Input",
            "Meeting_Day_of_the_Week": "Meeting Day of the Week",
            "Submission_Start_time": "Submission Start time",
            "Color_Tag": "Color Tag",
            "Compliance_Asset_Id": "Compliance Asset Id",
            "Completion_time": "Completion time",
            "Created_By": "Created By",
            "Modified_By": "Modified By",
            "Planner_Cadence": "Planner Cadence",
            "Primary_Language": "Primary Language",
            "Role_Type": "Role Type",
        }
        return {reverse_mapping.get(k, k): v for k, v in row.items()}

    def insert_amp_request(self, row: dict) -> bool:
        """Insert a single AMP-sourced request into store_meeting_request_data."""
        bq_row = self._to_bq_keys(row)
        table_ref = f"{PROJECT_ID}.{DATASET_ID}.store_meeting_request_data"
        errors = self.client.insert_rows_json(table_ref, [bq_row])
        if errors:
            print(f"[DB] AMP insert error: {errors}")
            return False
        return True

    # =========================================
    # STORE DATA
    # =========================================

    def get_store_data(self) -> list:
        """Get store reference data for form dropdowns."""
        query = f"""
            SELECT DISTINCT
                CAST(store_number AS STRING) as store_number,
                city, state, division, region, market
            FROM {STORE_CUR_TABLE}
            ORDER BY store_number
            LIMIT 5000
        """
        return self._run_query(query)

    # =========================================
    # CALENDAR DIMENSION
    # =========================================

    def get_calendar_dim(self, start_date: str, end_date: str) -> list:
        query = f"""
            SELECT
                CALENDAR_DATE,
                WM_WEEK_NBR,
                FISCAL_YEAR_NBR,
                WM_QTR_NAME,
                WM_YEAR_NBR
            FROM {CAL_DIM_TABLE}
            WHERE CALENDAR_DATE >= @start_date
              AND CALENDAR_DATE <= @end_date
            ORDER BY CALENDAR_DATE
        """
        params = [
            bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
            bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
        ]
        return self._run_query(query, params)

    # =========================================
    # MEETING TRACKER REPORT (Admin)
    # =========================================

    def get_meeting_tracker_report(self, start_date: str = None, end_date: str = None) -> list:
        """Get approved meetings formatted for the Calls to Stores report."""
        conditions = ["Status = 'Approved'"]
        params = []
        if start_date:
            conditions.append("DATE(`Start Date`) >= @report_start")
            params.append(bigquery.ScalarQueryParameter("report_start", "DATE", start_date))
        if end_date:
            conditions.append("DATE(`Start Date`) <= @report_end")
            params.append(bigquery.ScalarQueryParameter("report_end", "DATE", end_date))
        where = " AND ".join(conditions)

        query = f"""
            SELECT
                r.Title as description,
                r.`Meeting Type` as type_of_meeting,
                r.`Start Date` as date,
                r.`Meeting Day of the Week` as day,
                r.`Start Time` as time,
                r.`Store Selection` as store_audience,
                r.Name as author,
                r.Email as author_email,
                c.WM_WEEK_NBR as wm_week,
                c.FISCAL_YEAR_NBR as fiscal_year
            FROM {REQUEST_TABLE} r
            LEFT JOIN {CAL_DIM_TABLE} c
                ON DATE(r.`Start Date`) = c.CALENDAR_DATE
            WHERE {where}
            ORDER BY c.WM_WEEK_NBR, r.`Start Date`, r.`Start Time`
        """
        return self._run_query(query, params if params else None)
