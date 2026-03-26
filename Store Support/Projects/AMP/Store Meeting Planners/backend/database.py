"""BigQuery service for Store Meeting Planner"""
# Reloaded: March 26, 2026
import os
import re
import uuid
from datetime import datetime, date, timedelta
from typing import Optional
from google.cloud import bigquery


PROJECT_ID = os.getenv("GCP_PROJECT_ID", "wmt-assetprotection-prod")
DATASET_ID = os.getenv("BIGQUERY_DATASET", "Store_Support_Dev")

# Table references
AMP_TABLE = f"`{PROJECT_ID}.{DATASET_ID}.Output - AMP ALL 2`"
AMP_RAW_TABLE = f"`{PROJECT_ID}.{DATASET_ID}.AMP2 Data`"
AMP_HEADLINE_TABLE = f"`{PROJECT_ID}.{DATASET_ID}.AMP2 Headline`"
REQUEST_TABLE = f"`{PROJECT_ID}.{DATASET_ID}.store_meeting_request_data`"
CAL_DIM_TABLE = f"`{PROJECT_ID}.{DATASET_ID}.Cal_Dim_Data`"
STORE_CUR_TABLE = f"`{PROJECT_ID}.{DATASET_ID}.Store_Cur_Data`"
COSMOS_TABLE = "`wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`"

# msg_type_nm mapping in AMP2 Data (raw Cosmos)
# 0 = Calendar Events, 1 = Store Updates
AMP_RAW_TYPE_MAP = {"0": "Calendar Events", "1": "Store Updates"}

# Meeting detection patterns for compliance scanning
# Derived from keyword analysis of 132 known meeting request message bodies
# HIGH: Any single match = flag as likely meeting (strong indicators)
_HIGH_PATTERNS = [
    re.compile(r'meeting\s*id\s*[:\s]\s*\d{3,}', re.I),        # Meeting ID with digits (38% of known)
    re.compile(r'passcode\s*[:\s]\s*\S+', re.I),                # Passcode (8%)
    re.compile(r'zoom\.(us|com)/[jw]/\d+', re.I),               # Zoom join URL
    re.compile(r'zoom\.us/my/\S+', re.I),                        # Zoom personal room
    re.compile(r'teams\.microsoft\.com/.+/meetup-join', re.I),   # Teams join link
    re.compile(r'webex\.\w+\.com/\S+', re.I),                   # WebEx link
    re.compile(r'(?:dial|call)[\s-]in\s*(?:number|info)', re.I), # Dial-in info
    re.compile(r'\d{3}[\s.-]\d{3,4}[\s.-]\d{4}.*(?:pin|code|access)', re.I),  # Phone + PIN
    re.compile(r'office\s+hours', re.I),                         # "Office Hours" (31% of known)
    re.compile(r'(?:kickoff|kick-off)\s+(?:call|meeting)?', re.I),  # Kickoff (in titles)
]
# MEDIUM: Need 2+ matches to flag (weaker/contextual indicators)
_MED_PATTERNS = [
    re.compile(r'join\s+(?:the\s+)?(?:call|meeting|session|us)', re.I),   # "Join the call/us" (19%)
    re.compile(r'attend\s+(?:the\s+)?(?:call|meeting|session)', re.I),    # "Attend the meeting" (12%)
    re.compile(r'conference\s*(?:call|bridge|line)', re.I),               # Conference call
    re.compile(r'(?:deployment|admin|installation|evaluation)\s*call', re.I),  # Specific call types (12%)
    re.compile(r'listening\s+session', re.I),                              # Listening session
    re.compile(r'\bregister\b.*(?:call|meeting|session|webinar)', re.I),  # Register for event (15%)
    re.compile(r'(?:virtual|live)\s+(?:session|meeting|event|training)', re.I),  # Virtual session (15%)
    re.compile(r'\btraining\b.*(?:call|session|meeting|zoom|teams)', re.I),  # Training with meeting (27%)
    re.compile(r'(?:weekly|bi-weekly|recurring)\s+(?:call|meeting)', re.I),  # Recurring call
    re.compile(r'\bzoom\b', re.I),                                         # Any mention of Zoom (23%)
    re.compile(r'\b(?:phone|dial)\s*(?:number|:)', re.I),                  # Phone number reference (23%)
    re.compile(r'(?:pre-launch|launch)\s+(?:call|meeting|actions?)', re.I),  # Launch call
    re.compile(r'\bhost(?:ing)?\s+(?:a\s+)?(?:call|meeting|session)', re.I),  # Hosting a call (8%)
    re.compile(r'\bschedule[ds]?\s+(?:a\s+)?(?:call|meeting)', re.I),      # Scheduled call
    re.compile(r'(?:support|update|champion)\s+call', re.I),               # Support/update call
]

# Active statuses for AMP Calendar Events / Store Updates display
# Excludes only Draft and Denied (not meaningful for calendar display)
AMP_ACTIVE_STATUSES = (
    "'Awaiting ATC Approval','Awaiting Comms Approval','Review for Publish review',"
    "'Review for Publish review - No Comms','Published','Expired',"
    "'ATC final review','Awaiting Business Review','Awaiting Legal Approval'"
)

REGULAR_MAX_SLOTS = 20
PROTECTED_MAX_SLOTS = 10


class DatabaseService:
    def __init__(self):
        self.client = None
        self._amp_table_status = None  # None=unchecked, 'primary', 'fallback'
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
            # Quick connectivity check
            list(self.client.query("SELECT 1").result())
            print(f"[DB] Connected to BigQuery project: {PROJECT_ID}")
        except Exception as e:
            print(f"[DB] BigQuery connection error: {e}")
            self.client = None

    def is_connected(self) -> bool:
        if not self.client:
            self._connect()
        return self.client is not None

    def _check_amp_table(self) -> str:
        """Check if Output - AMP ALL 2 has data; if not, use AMP2 Data fallback.
        Returns 'primary' or 'fallback'. Caches result for 10 minutes."""
        if self._amp_table_status and hasattr(self, '_amp_check_time'):
            if (datetime.utcnow() - self._amp_check_time).total_seconds() < 600:
                return self._amp_table_status
        rows = self._run_query(f"SELECT 1 FROM {AMP_TABLE} LIMIT 1")
        if rows:
            self._amp_table_status = 'primary'
        else:
            print("[DB] Output - AMP ALL 2 is empty — using AMP2 Data fallback")
            self._amp_table_status = 'fallback'
        self._amp_check_time = datetime.utcnow()
        return self._amp_table_status

    @staticmethod
    def _to_timestamp_str(val) -> str:
        """Convert a date string or value to TIMESTAMP-compatible format."""
        if not val:
            return ""
        s = str(val)
        # If it's just a date (YYYY-MM-DD), append time component
        if len(s) == 10 and s[4] == "-" and s[7] == "-":
            return f"{s} 00:00:00"
        return s

    def _run_query(self, query: str, params: list = None) -> list:
        if not self.client:
            print("[DB] No BigQuery client — attempting reconnect...")
            self._connect()
        if not self.client:
            print("[DB] Reconnect failed, no BigQuery client available")
            return []
        try:
            job_config = bigquery.QueryJobConfig()
            if params:
                job_config.query_parameters = params
            result = self.client.query(query, job_config=job_config)
            return [dict(row) for row in result]
        except Exception as e:
            print(f"[DB] Query error: {e} — attempting reconnect...")
            self._connect()
            if not self.client:
                return []
            try:
                job_config = bigquery.QueryJobConfig()
                if params:
                    job_config.query_parameters = params
                result = self.client.query(query, job_config=job_config)
                return [dict(row) for row in result]
            except Exception as e2:
                print(f"[DB] Query retry failed: {e2}")
                return []

    # =========================================
    # CALENDAR & PROTECTED WEEKS
    # =========================================

    def get_calendar_events(self, start_date: str, end_date: str) -> list:
        """Get AMP Calendar Events for display on the calendar (deduplicated)."""
        source = self._check_amp_table()
        if source == 'primary':
            query = f"""
                SELECT
                    MIN(event_id) as event_id,
                    Activity_Title as title,
                    'Calendar Events' as message_type,
                    Start_Date as start_date,
                    End_Date as end_date,
                    MAX(Business_Area) as business_area,
                    MAX(Author) as author,
                    MAX(Store_Cnt) as store_cnt,
                    MAX(WM_Week) as wm_week,
                    MAX(WM_Year) as wm_year,
                    MAX(Web_Preview) as preview_url
                FROM {AMP_TABLE}
                WHERE Message_Type = 'Calendar Events'
                  AND Message_Status IN ({AMP_ACTIVE_STATUSES})
                  AND Start_Date <= @end_date
                  AND End_Date >= @start_date
                GROUP BY Activity_Title, Start_Date, End_Date
                ORDER BY Start_Date
            """
        else:
            query = f"""
                SELECT
                    MIN(event_id) as event_id,
                    actv_title_home_ofc_nm as title,
                    'Calendar Events' as message_type,
                    msg_start_dt as start_date,
                    msg_end_dt as end_date,
                    MAX(bus_domain_nm) as business_area,
                    MAX(tag_user_nm) as author,
                    0 as store_cnt,
                    NULL as wm_week,
                    NULL as wm_year,
                    NULL as preview_url
                FROM {AMP_RAW_TABLE}
                WHERE msg_type_nm = '0'
                  AND msg_leg_status_nm IN ('APPROVED', 'REQUESTED')
                  AND msg_start_dt <= @end_date
                  AND msg_end_dt >= @start_date
                GROUP BY actv_title_home_ofc_nm, msg_start_dt, msg_end_dt
                ORDER BY msg_start_dt
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
        """Get Protected Week dates (deduplicated)."""
        source = self._check_amp_table()
        if source == 'primary':
            query = f"""
                SELECT
                    'Protected Week' as title,
                    Start_Date as start_date,
                    End_Date as end_date,
                    MAX(WM_Week) as wm_week,
                    MAX(WM_Year) as wm_year
                FROM {AMP_TABLE}
                WHERE LOWER(Activity_Title) LIKE '%protected week%'
                  AND Message_Type = 'Calendar Events'
                  AND Message_Status IN ({AMP_ACTIVE_STATUSES})
                  AND CAST(WM_Year AS INT64) = @fiscal_year
                GROUP BY Start_Date, End_Date
                ORDER BY Start_Date
            """
        else:
            query = f"""
                SELECT
                    'Protected Week' as title,
                    msg_start_dt as start_date,
                    msg_end_dt as end_date,
                    NULL as wm_week,
                    NULL as wm_year
                FROM {AMP_RAW_TABLE}
                WHERE LOWER(actv_title_home_ofc_nm) LIKE '%protected week%'
                  AND msg_leg_status_nm IN ('APPROVED', 'REQUESTED')
                GROUP BY msg_start_dt, msg_end_dt
                ORDER BY msg_start_dt
            """
        params = [
            bigquery.ScalarQueryParameter("fiscal_year", "INT64", fiscal_year),
        ]
        return self._run_query(query, params)

    def get_protected_week_dates(self) -> set:
        """Returns a set of date strings (YYYY-MM-DD) that fall in protected weeks."""
        source = self._check_amp_table()
        if source == 'primary':
            query = f"""
                SELECT
                    Start_Date as pw_start,
                    End_Date as pw_end
                FROM {AMP_TABLE}
                WHERE LOWER(Activity_Title) LIKE '%protected week%'
                  AND Message_Type = 'Calendar Events'
                  AND Message_Status IN ({AMP_ACTIVE_STATUSES})
                GROUP BY Start_Date, End_Date
            """
        else:
            query = f"""
                SELECT
                    msg_start_dt as pw_start,
                    msg_end_dt as pw_end
                FROM {AMP_RAW_TABLE}
                WHERE LOWER(actv_title_home_ofc_nm) LIKE '%protected week%'
                  AND msg_leg_status_nm IN ('APPROVED', 'REQUESTED')
                GROUP BY msg_start_dt, msg_end_dt
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
        """Get slot availability for a date range.
        Counts approved meetings (including recurring monthly expansions) against slots."""
        # Direct approved counts for this date range
        query = f"""
            SELECT
                DATE(SAFE_CAST(`Start Date` AS TIMESTAMP)) as request_date,
                COUNT(*) as approved_count
            FROM {REQUEST_TABLE}
            WHERE Status = 'Approved'
              AND DATE(SAFE_CAST(`Start Date` AS TIMESTAMP)) >= @start_date
              AND DATE(SAFE_CAST(`Start Date` AS TIMESTAMP)) <= @end_date
            GROUP BY DATE(SAFE_CAST(`Start Date` AS TIMESTAMP))
        """
        params = [
            bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
            bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
        ]
        approved = {str(r["request_date"]): r["approved_count"] for r in self._run_query(query, params)}

        # Expand recurring monthly approved meetings into this date range
        recurring_counts = self._get_recurring_approved_counts(start_date, end_date)
        for date_str, count in recurring_counts.items():
            approved[date_str] = approved.get(date_str, 0) + count

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

    def _get_recurring_approved_counts(self, start_date: str, end_date: str) -> dict:
        """Expand recurring approved meetings (Weekly, Bi-Weekly, Monthly) into
        date counts for the given range. Returns {date_str: additional_count}."""
        query = f"""
            SELECT
                Title,
                DATE(SAFE_CAST(`Start Date` AS TIMESTAMP)) as original_date,
                DATE(SAFE_CAST(`End Date` AS TIMESTAMP)) as end_date,
                `Meeting Reoccurrence` as reoccurrence
            FROM {REQUEST_TABLE}
            WHERE Status = 'Approved'
              AND `Meeting Reoccurrence` IS NOT NULL
              AND `Meeting Reoccurrence` NOT IN ('', 'None')
        """
        rows = self._run_query(query)
        if not rows:
            return {}

        try:
            range_start = datetime.strptime(start_date, "%Y-%m-%d").date()
            range_end = datetime.strptime(end_date, "%Y-%m-%d").date()
        except Exception:
            return {}

        counts = {}
        for row in rows:
            orig = row.get("original_date")
            if not orig:
                continue
            if hasattr(orig, 'date'):
                orig = orig.date()
            elif isinstance(orig, str):
                try:
                    orig = datetime.strptime(str(orig)[:10], "%Y-%m-%d").date()
                except Exception:
                    continue

            # Cap end of recurrence at the meeting's End Date or 1 yr from start
            meeting_end = row.get("end_date")
            if meeting_end:
                if hasattr(meeting_end, 'date'):
                    meeting_end = meeting_end.date()
                elif isinstance(meeting_end, str):
                    try:
                        meeting_end = datetime.strptime(str(meeting_end)[:10], "%Y-%m-%d").date()
                    except Exception:
                        meeting_end = None
            if not meeting_end:
                meeting_end = orig + timedelta(days=365)

            reoccurrence = (row.get("reoccurrence") or "").strip()
            occurrences = self._expand_occurrences(orig, meeting_end, reoccurrence)

            for occ_date in occurrences:
                if occ_date == orig:
                    continue  # Original date already counted by direct query
                if range_start <= occ_date <= range_end:
                    ds = occ_date.isoformat()
                    counts[ds] = counts.get(ds, 0) + 1

        return counts

    @staticmethod
    def _expand_occurrences(start: date, end: date, reoccurrence: str) -> list:
        """Generate all occurrence dates from start to end based on reoccurrence type."""
        import calendar as cal_mod
        dates = [start]
        reoccurrence_lower = reoccurrence.lower()

        if reoccurrence_lower == 'weekly':
            current = start + timedelta(weeks=1)
            while current <= end:
                dates.append(current)
                current += timedelta(weeks=1)
        elif reoccurrence_lower == 'bi-weekly':
            current = start + timedelta(weeks=2)
            while current <= end:
                dates.append(current)
                current += timedelta(weeks=2)
        elif reoccurrence_lower == 'monthly':
            day_of_month = start.day
            current = start
            while True:
                if current.month == 12:
                    next_month = current.replace(year=current.year + 1, month=1, day=1)
                else:
                    next_month = current.replace(month=current.month + 1, day=1)
                max_day = cal_mod.monthrange(next_month.year, next_month.month)[1]
                actual_day = min(day_of_month, max_day)
                current = next_month.replace(day=actual_day)
                if current > end:
                    break
                dates.append(current)
        elif reoccurrence_lower == 'quarterly':
            day_of_month = start.day
            current = start
            while True:
                new_month = current.month + 3
                new_year = current.year
                while new_month > 12:
                    new_month -= 12
                    new_year += 1
                max_day = cal_mod.monthrange(new_year, new_month)[1]
                actual_day = min(day_of_month, max_day)
                current = date(new_year, new_month, actual_day)
                if current > end:
                    break
                dates.append(current)
        elif reoccurrence_lower == 'yearly':
            current = start
            while True:
                try:
                    current = current.replace(year=current.year + 1)
                except ValueError:
                    current = current.replace(year=current.year + 1, day=28)
                if current > end:
                    break
                dates.append(current)

        return dates

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
            conditions.append("DATE(SAFE_CAST(`Start Date` AS TIMESTAMP)) >= @filter_start")
            params.append(bigquery.ScalarQueryParameter("filter_start", "DATE", start_date))
        if end_date:
            conditions.append("DATE(SAFE_CAST(`Start Date` AS TIMESTAMP)) <= @filter_end")
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
                SAFE_CAST(`Start Date` AS TIMESTAMP) DESC
        """
        rows = self._run_query(query, params if params else None)
        return [self._add_source_info(self._normalize_request_row(r)) for r in rows]

    def get_user_requests(self, email: str) -> list:
        """Get requests for a specific user."""
        query = f"""
            SELECT *
            FROM {REQUEST_TABLE}
            WHERE LOWER(Email) = LOWER(@email)
            ORDER BY SAFE_CAST(`Start Date` AS TIMESTAMP) DESC
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
            "Start Date": self._to_timestamp_str(data.get("Start_Date")),
            "End Date": self._to_timestamp_str(data.get("End_Date")),
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
        source = self._check_amp_table()
        if source == 'primary':
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
                  AND Message_Status IN ({AMP_ACTIVE_STATUSES})
                ORDER BY Start_Date DESC
            """
        else:
            query = f"""
                SELECT
                    event_id,
                    actv_title_home_ofc_nm as title,
                    CASE msg_type_nm WHEN '0' THEN 'Calendar Events' ELSE 'Store Updates' END as message_type,
                    msg_start_dt as start_date,
                    msg_end_dt as end_date,
                    bus_domain_nm as business_area,
                    tag_user_nm as author,
                    tag_user_email_id as activity_email,
                    0 as store_cnt,
                    NULL as wm_week,
                    NULL as wm_year,
                    msg_kw_array as keywords,
                    NULL as preview_url,
                    NULL as edit_link,
                    NULL as mp_date,
                    NULL as mp_duration,
                    NULL as mp_start_datetime,
                    NULL as mp_end_datetime,
                    NULL as mp_timezone
                FROM {AMP_RAW_TABLE}
                WHERE LOWER(IFNULL(msg_kw_array, '')) LIKE '%meeting planner%'
                  AND msg_leg_status_nm IN ('APPROVED', 'REQUESTED')
                ORDER BY msg_start_dt DESC
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

    def get_existing_request_titles(self) -> list:
        """Get all request titles + IDs + AMP URLs for dedup during AMP sync."""
        query = f"""
            SELECT ID, LOWER(TRIM(Title)) as title_lower,
                   `AMP Activity URL` as amp_url
            FROM {REQUEST_TABLE}
        """
        rows = self._run_query(query)
        return [{"id": r["ID"], "title_lower": r["title_lower"] or "", "amp_url": r.get("amp_url") or ""} for r in rows]

    def link_amp_url_to_request(self, request_id: str, amp_url: str):
        """Update a Form-submitted request with its matching AMP URL."""
        query = f"""
            UPDATE {REQUEST_TABLE}
            SET `AMP Activity` = TRUE,
                `AMP Activity URL` = @amp_url,
                Modified = @modified
            WHERE ID = @request_id
        """
        params = [
            bigquery.ScalarQueryParameter("amp_url", "STRING", amp_url),
            bigquery.ScalarQueryParameter("modified", "STRING", datetime.utcnow().isoformat()),
            bigquery.ScalarQueryParameter("request_id", "STRING", request_id),
        ]
        self._run_query(query, params)

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
        """Get approved meetings formatted for the Calls to Stores report.
        Expands recurring meetings into duplicate rows for each occurrence.
        Includes store_count from AMP ALL 2 via URL matching."""
        conditions = ["Status = 'Approved'"]
        params = []
        if start_date:
            conditions.append("DATE(SAFE_CAST(`Start Date` AS TIMESTAMP)) >= @report_start")
            params.append(bigquery.ScalarQueryParameter("report_start", "DATE", start_date))
        if end_date:
            conditions.append("DATE(SAFE_CAST(`Start Date` AS TIMESTAMP)) <= @report_end")
            params.append(bigquery.ScalarQueryParameter("report_end", "DATE", end_date))
        where = " AND ".join(conditions)

        query = f"""
            SELECT
                r.Title as description,
                r.`Meeting Type` as type_of_meeting,
                SAFE_CAST(r.`Start Date` AS TIMESTAMP) as date,
                DATE(SAFE_CAST(r.`End Date` AS TIMESTAMP)) as end_date_raw,
                r.`Meeting Day of the Week` as day,
                r.`Start Time` as time,
                r.`Store Selection` as store_audience,
                r.Name as author,
                r.Email as author_email,
                r.Status as status,
                c.WM_WEEK_NBR as wm_week,
                c.FISCAL_YEAR_NBR as fiscal_year,
                r.`AMP Activity URL` as amp_url,
                r.`Meeting Reoccurrence` as reoccurrence
            FROM {REQUEST_TABLE} r
            LEFT JOIN {CAL_DIM_TABLE} c
                ON DATE(SAFE_CAST(r.`Start Date` AS TIMESTAMP)) = c.CALENDAR_DATE
            WHERE {where}
            ORDER BY c.FISCAL_YEAR_NBR DESC, c.WM_WEEK_NBR DESC, SAFE_CAST(r.`Start Date` AS TIMESTAMP) ASC, r.`Start Time`
        """
        rows = self._run_query(query, params if params else None)

        # Build a lookup for store counts from AMP ALL 2 keyed by event_id
        amp_store_counts = self._get_amp_store_counts()

        # Build calendar dim lookup for expanded dates
        cal_lookup = self._get_cal_dim_lookup()

        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        expanded_rows = []
        for row in rows:
            amp_url = row.get("amp_url") or ""
            store_count = None
            if amp_url:
                parts = amp_url.rstrip("/").split("/")
                if len(parts) >= 3:
                    event_id = parts[-3]
                    store_count = amp_store_counts.get(event_id)
            row["store_count"] = store_count

            reoccurrence = (row.get("reoccurrence") or "").strip()
            if reoccurrence and reoccurrence not in ("", "None"):
                # Expand this recurring meeting
                orig_date = row.get("date")
                if orig_date:
                    if hasattr(orig_date, 'date'):
                        orig = orig_date.date()
                    else:
                        try:
                            orig = datetime.strptime(str(orig_date)[:10], "%Y-%m-%d").date()
                        except Exception:
                            orig = None

                    meeting_end = row.get("end_date_raw")
                    if meeting_end:
                        if hasattr(meeting_end, 'date'):
                            meeting_end = meeting_end.date()
                        elif isinstance(meeting_end, str):
                            try:
                                meeting_end = datetime.strptime(str(meeting_end)[:10], "%Y-%m-%d").date()
                            except Exception:
                                meeting_end = None
                    if not meeting_end and orig:
                        meeting_end = orig + timedelta(days=365)

                    if orig and meeting_end:
                        # Add the original row first
                        expanded_rows.append(row)

                        # Generate additional occurrences (skip original)
                        occurrences = self._expand_occurrences(orig, meeting_end, reoccurrence)
                        for occ_date in occurrences:
                            if occ_date == orig:
                                continue
                            if start_date:
                                try:
                                    filt_start = datetime.strptime(start_date, "%Y-%m-%d").date()
                                    if occ_date < filt_start:
                                        continue
                                except Exception:
                                    pass
                            if end_date:
                                try:
                                    filt_end = datetime.strptime(end_date, "%Y-%m-%d").date()
                                    if occ_date > filt_end:
                                        continue
                                except Exception:
                                    pass

                            occ_str = occ_date.isoformat()
                            cal_info = cal_lookup.get(occ_str, {})
                            new_row = dict(row)
                            new_row["date"] = occ_str
                            new_row["day"] = day_names[occ_date.weekday()]
                            new_row["wm_week"] = cal_info.get("WM_WEEK_NBR", row.get("wm_week"))
                            new_row["fiscal_year"] = cal_info.get("FISCAL_YEAR_NBR", row.get("fiscal_year"))
                            expanded_rows.append(new_row)
                        continue  # Already added original above

            expanded_rows.append(row)

        # Sort expanded rows: fiscal year DESC, wm_week DESC, date ASC
        def sort_key(r):
            fy = r.get("fiscal_year") or 0
            wk = r.get("wm_week") or 0
            d = str(r.get("date") or "")[:10]
            t = r.get("time") or ""
            return (-fy, -wk, d, t)
        expanded_rows.sort(key=sort_key)

        # Remove end_date_raw from output
        for row in expanded_rows:
            row.pop("end_date_raw", None)

        return expanded_rows

    def _get_cal_dim_lookup(self) -> dict:
        """Get a lookup of date -> {WM_WEEK_NBR, FISCAL_YEAR_NBR} from Cal_Dim_Data."""
        query = f"""
            SELECT CALENDAR_DATE, WM_WEEK_NBR, FISCAL_YEAR_NBR
            FROM {CAL_DIM_TABLE}
        """
        rows = self._run_query(query)
        result = {}
        for r in rows:
            d = str(r.get("CALENDAR_DATE", ""))
            result[d] = {"WM_WEEK_NBR": r.get("WM_WEEK_NBR"), "FISCAL_YEAR_NBR": r.get("FISCAL_YEAR_NBR")}
        return result

    def _get_amp_store_counts(self) -> dict:
        """Get a mapping of event_id -> Store_Cnt from AMP ALL 2 or fallback."""
        source = self._check_amp_table()
        if source == 'primary':
            query = f"""
                SELECT DISTINCT event_id, Store_Cnt
                FROM {AMP_TABLE}
                WHERE event_id IS NOT NULL
            """
        else:
            # AMP2 Data doesn't have Store_Cnt; count from Store Activity
            query = f"""
                SELECT event_id, COUNT(DISTINCT store_org_cd) as Store_Cnt
                FROM `{PROJECT_ID}.{DATASET_ID}.AMP 2 Store Activity`
                WHERE event_id IS NOT NULL
                GROUP BY event_id
            """
        rows = self._run_query(query)
        result = {}
        for r in rows:
            eid = str(r.get("event_id", ""))
            cnt = r.get("Store_Cnt")
            if eid and cnt is not None:
                try:
                    result[eid] = int(cnt)
                except (ValueError, TypeError):
                    result[eid] = cnt
        return result

    # -------------------------------------------------
    # Compliance Scan: find AMP events with meeting
    # content that lack a Meeting Planner request
    # -------------------------------------------------

    def scan_compliance_gaps(self) -> dict:
        """Scan AMP Store Updates for meetings missing from Meeting Planner."""
        source = self._check_amp_table()
        # Step 1: Get distinct AMP events (Store Updates + Calendar Events)
        if source == 'primary':
            q_events = f"""
                SELECT DISTINCT
                    a.event_id,
                    a.Activity_Title,
                    a.Message_Type,
                    a.Message_Status,
                    a.Author_email,
                    a.Store_Cnt,
                    CAST(a.Start_Date AS STRING) AS Start_Date,
                    CAST(a.End_Date AS STRING) AS End_Date,
                    a.Business_Area
                FROM {AMP_TABLE} a
                WHERE a.Start_Date >= DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH)
                  AND a.Message_Type IN ('Store Updates', 'Calendar Events')
                  AND a.Message_Status IN ({AMP_ACTIVE_STATUSES})
                  AND a.event_id IS NOT NULL
            """
        else:
            q_events = f"""
                SELECT DISTINCT
                    a.event_id,
                    a.actv_title_home_ofc_nm AS Activity_Title,
                    CASE a.msg_type_nm WHEN '0' THEN 'Calendar Events' ELSE 'Store Updates' END AS Message_Type,
                    a.msg_leg_status_nm AS Message_Status,
                    a.tag_user_email_id AS Author_email,
                    0 AS Store_Cnt,
                    CAST(a.msg_start_dt AS STRING) AS Start_Date,
                    CAST(a.msg_end_dt AS STRING) AS End_Date,
                    a.bus_domain_nm AS Business_Area
                FROM {AMP_RAW_TABLE} a
                WHERE a.msg_start_dt >= DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH)
                  AND a.msg_type_nm IN ('0', '1')
                  AND a.msg_leg_status_nm IN ('APPROVED', 'REQUESTED')
                  AND a.event_id IS NOT NULL
            """
        events = self._run_query(q_events)
        event_map = {}
        for e in events:
            eid = e.get("event_id")
            if eid and eid not in event_map:
                event_map[eid] = dict(e)

        if not event_map:
            return {"flagged": [], "total_scanned": 0, "scan_date": datetime.utcnow().isoformat()}

        # Step 2: Get message bodies from Cosmos
        event_ids = list(event_map.keys())
        body_map = {}
        batch_size = 50
        for i in range(0, len(event_ids), batch_size):
            batch = event_ids[i:i + batch_size]
            id_list = ", ".join(f"'{eid}'" for eid in batch)
            q_body = f"""
                SELECT event_id, msg_txt
                FROM {COSMOS_TABLE}
                WHERE event_id IN ({id_list})
            """
            for row in self._run_query(q_body):
                eid = row.get("event_id")
                msg_txt = row.get("msg_txt")
                body_text = ""
                if msg_txt and isinstance(msg_txt, dict):
                    arr = msg_txt.get("array", [])
                    if arr:
                        raw_html = str(arr[0])
                        body_text = re.sub(r'<[^>]+>', ' ', raw_html)
                        body_text = re.sub(r'\s+', ' ', body_text).strip()
                body_map[eid] = body_text

        # Step 3: Detect meeting content with two-tier patterns
        # Check BOTH body text AND title for meeting indicators
        _TITLE_PATTERNS = [
            re.compile(r'office\s+hours', re.I),
            re.compile(r'(?:kickoff|kick-off)\b', re.I),
            re.compile(r'\bcall\b', re.I),
            re.compile(r'\bbroadcast\b', re.I),
            re.compile(r'listening\s+session', re.I),
            re.compile(r'\bwebinar\b', re.I),
            re.compile(r'town[\s-]*hall', re.I),
            re.compile(r'brown\s+bag', re.I),
            re.compile(r'\bdemo\b', re.I),
            re.compile(r'q\s*[&+]\s*a\b', re.I),
            re.compile(r'pre[\s-]*launch\s+actions', re.I),
        ]
        flagged = []
        # Scan events with bodies
        for eid, body in body_map.items():
            text = body or ""
            title = (event_map.get(eid, {}).get("Activity_Title") or "")
            # Check body for HIGH/MED patterns
            high = [p.pattern for p in _HIGH_PATTERNS if text and p.search(text)]
            med = [p.pattern for p in _MED_PATTERNS if text and p.search(text)]
            # Also check title for meeting-indicating patterns
            title_hits = [p.pattern for p in _TITLE_PATTERNS if p.search(title)]
            if title_hits and not high:
                # Title match counts as HIGH confidence
                high = title_hits
            if high or len(med) >= 2:
                meta = event_map.get(eid, {})
                flagged.append({
                    "event_id": eid,
                    "title": meta.get("Activity_Title", ""),
                    "message_type": meta.get("Message_Type", ""),
                    "status": meta.get("Message_Status", ""),
                    "author": meta.get("Author_email", ""),
                    "start_date": str(meta.get("Start_Date", ""))[:10],
                    "end_date": str(meta.get("End_Date", ""))[:10],
                    "area": meta.get("Business_Area", ""),
                    "stores": meta.get("Store_Cnt", 0),
                    "confidence": "HIGH" if high else "MEDIUM",
                    "matched_patterns": (high or []) + med,
                    "body_preview": (text or title)[:300],
                })
        # Also scan events without bodies (title-only detection)
        for eid in event_map:
            if eid in body_map:
                continue  # Already processed
            title = (event_map[eid].get("Activity_Title") or "")
            title_hits = [p.pattern for p in _TITLE_PATTERNS if p.search(title)]
            if title_hits:
                meta = event_map[eid]
                flagged.append({
                    "event_id": eid,
                    "title": meta.get("Activity_Title", ""),
                    "message_type": meta.get("Message_Type", ""),
                    "status": meta.get("Message_Status", ""),
                    "author": meta.get("Author_email", ""),
                    "start_date": str(meta.get("Start_Date", ""))[:10],
                    "end_date": str(meta.get("End_Date", ""))[:10],
                    "area": meta.get("Business_Area", ""),
                    "stores": meta.get("Store_Cnt", 0),
                    "confidence": "HIGH",
                    "matched_patterns": title_hits,
                    "body_preview": f"[Title match] {title}",
                })

        # Step 4: Exclude events already tracked in Meeting Planner
        # Match by title (fuzzy) and by AMP Activity URL (event_id in URL)
        q_existing = f"""
            SELECT DISTINCT LOWER(TRIM(Title)) as title_lower,
                   `AMP Activity URL` as amp_url
            FROM {REQUEST_TABLE}
        """
        existing_titles = set()
        existing_event_ids = set()
        for r in self._run_query(q_existing):
            t = r.get("title_lower")
            if t:
                existing_titles.add(t)
            url = r.get("amp_url") or ""
            # Extract event_id UUID from AMP URL
            eid_match = re.search(r'/(message|preview)/([a-f0-9-]{36})/', url)
            if eid_match:
                existing_event_ids.add(eid_match.group(2))

        missing = []
        for f in flagged:
            # Check if event_id is already tracked via AMP URL
            if f["event_id"] in existing_event_ids:
                continue
            # Check title fuzzy match
            title_l = f["title"].strip().lower()
            tracked = any(
                title_l in et or et in title_l
                for et in existing_titles
            )
            if not tracked:
                missing.append(f)

        return {
            "flagged": missing,
            "total_scanned": len(event_map),
            "total_with_bodies": len(body_map),
            "total_flagged_before_filter": len(flagged),
            "scan_date": datetime.utcnow().isoformat(),
        }
