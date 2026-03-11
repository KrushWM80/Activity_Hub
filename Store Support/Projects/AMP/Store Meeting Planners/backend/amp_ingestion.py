"""AMP Auto-Ingestion Service for Store Meeting Planner
Automatically ingests Meeting Planner events from AMP ALL 2 table.
"""
import uuid
import re
from datetime import datetime
from typing import Optional
from database import DatabaseService
from models import check_completeness


def parse_keywords(keywords: str) -> dict:
    """Parse AMP Keywords field to extract Meeting Planner data.

    Keywords format: "EventType - Date - TimeRange - Timezone, field2, field3, field4, field5, field6"
    """
    result = {
        "event_type": "",
        "mp_date": "",
        "mp_start_time": "",
        "mp_end_time": "",
        "mp_timezone": "",
        "mp_duration": None,
    }

    if not keywords or "Meeting Planner" not in keywords:
        return result

    try:
        # Split by comma — first part has the main data
        parts = [p.strip() for p in keywords.split(",")]
        if not parts:
            return result

        # Split 1: "EventType - Date - TimeRange - Timezone"
        split1 = parts[0]
        dash_parts = [p.strip() for p in split1.split(" - ")]

        if len(dash_parts) >= 1:
            result["event_type"] = dash_parts[0]  # "Meeting Planner"

        if len(dash_parts) >= 2:
            result["mp_date"] = dash_parts[1]  # "January 15 2026"

        if len(dash_parts) >= 3:
            time_range = dash_parts[2]  # "9:00 AM to 10:00 AM"
            time_parts = [t.strip() for t in time_range.split(" to ")]
            if len(time_parts) >= 1:
                result["mp_start_time"] = time_parts[0]
            if len(time_parts) >= 2:
                result["mp_end_time"] = time_parts[1]

        if len(dash_parts) >= 4:
            result["mp_timezone"] = dash_parts[3]  # "CST"

        # Compute duration in minutes
        if result["mp_date"] and result["mp_start_time"] and result["mp_end_time"]:
            try:
                date_str = result["mp_date"]
                start_str = f"{date_str}, {result['mp_start_time']}"
                end_str = f"{date_str}, {result['mp_end_time']}"
                # Try multiple date formats
                for fmt in ["%B %d %Y, %I:%M %p", "%B %d %Y, %I:%M%p"]:
                    try:
                        start_dt = datetime.strptime(start_str, fmt)
                        end_dt = datetime.strptime(end_str, fmt)
                        duration = int((end_dt - start_dt).total_seconds() / 60)
                        if duration > 0:
                            result["mp_duration"] = duration
                        break
                    except ValueError:
                        continue
            except Exception:
                pass

    except Exception as e:
        print(f"[AMP] Keywords parsing error: {e}")

    return result


def build_amp_url(event_id: str, wm_week: str, wm_year: str) -> str:
    """Build AMP message URL."""
    return f"https://amp2-cms.prod.walmart.com/message/{event_id}/{wm_week}/{wm_year}"


def build_preview_url(event_id: str, wm_week: str, wm_year: str) -> str:
    """Build AMP preview URL."""
    return f"https://amp2-cms.prod.walmart.com/preview/{event_id}/{wm_week}/{wm_year}"


def derive_day_of_week(date_value) -> str:
    """Derive day of week from a date value."""
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    try:
        if isinstance(date_value, str):
            dt = datetime.strptime(date_value, "%Y-%m-%d")
        elif hasattr(date_value, 'weekday'):
            dt = date_value
        else:
            return ""
        return days[dt.weekday()]
    except Exception:
        return ""


def map_amp_to_request(event: dict, parsed: dict) -> dict:
    """Map AMP event data to store_meeting_request_data row."""
    now = datetime.utcnow().isoformat()
    request_id = str(uuid.uuid4())[:8].upper()

    event_id = str(event.get("event_id", ""))
    wm_week = str(event.get("wm_week", ""))
    wm_year = str(event.get("wm_year", ""))

    amp_url = build_amp_url(event_id, wm_week, wm_year) if event_id else ""

    # Determine store selection from store count
    store_cnt = event.get("store_cnt")
    store_selection = ""
    if store_cnt and int(store_cnt) > 4000:
        store_selection = "All Stores"

    # Get duration — prefer parsed Keywords, fallback to BQ MP columns
    duration = parsed.get("mp_duration")
    if not duration and event.get("mp_duration"):
        try:
            duration = int(event["mp_duration"])
        except (ValueError, TypeError):
            pass

    # Start/End dates
    start_date = event.get("start_date")
    end_date = event.get("end_date")
    if start_date and hasattr(start_date, 'isoformat'):
        start_date = start_date.isoformat()
    if end_date and hasattr(end_date, 'isoformat'):
        end_date = end_date.isoformat()

    # Author info
    author_email = event.get("activity_email", "") or ""
    author_name = event.get("author", "") or ""

    row = {
        "ID": request_id,
        "Title": event.get("title", ""),
        "Email": author_email,
        "Name": author_name,
        "AMP_Activity": True,
        "AMP_Activity_URL": amp_url,
        "Start_Date": str(start_date) if start_date else "",
        "End_Date": str(end_date) if end_date else "",
        "Meeting_Duration": duration,
        "Meeting_Type": "",  # NOT available from AMP
        "Impacted_Shift": None,  # NOT available from AMP
        "Store_Selection": store_selection,
        "Meeting_Reoccurrence": "None",
        "Meeting_Day_of_the_Week": derive_day_of_week(start_date) if start_date else "",
        "Start_Time": parsed.get("mp_start_time", "") or str(event.get("mp_start_datetime", "") or ""),
        "Meeting_Link": "",
        "Planner_Cadence": "",
        "Primary_Language": "",
        "Role_Type": "",
        "Color_Tag": "",
        "Compliance_Asset_Id": "",
        "Submission_Start_time": now,
        "Completion_time": "",
        "Created": now,
        "Created_By": "AMP Auto-Sync",
        "Modified": now,
        "Modified_By": "AMP Auto-Sync",
        "Version": "1",
        "AMP_Input": "",  # Will be updated below with missing fields
        "Status": "Pending",  # Default; upgraded to Review if all fields present
    }

    return row


def run_amp_sync(db: DatabaseService) -> dict:
    """Main sync function — queries AMP, maps events, inserts new records.
    Returns summary of sync results."""
    print("[AMP Sync] Starting AMP auto-ingestion...")

    # Get existing AMP URLs to prevent duplicates
    existing_urls = db.get_existing_amp_urls()
    print(f"[AMP Sync] Found {len(existing_urls)} existing AMP records")

    # Get AMP events with Meeting Planner keywords
    amp_events = db.get_amp_meeting_planner_events()
    print(f"[AMP Sync] Found {len(amp_events)} AMP Meeting Planner events")

    stats = {"total": len(amp_events), "new": 0, "skipped": 0, "errors": 0}

    for event in amp_events:
        event_id = str(event.get("event_id", ""))
        wm_week = str(event.get("wm_week", ""))
        wm_year = str(event.get("wm_year", ""))

        # Build URL for duplicate check
        amp_url = build_amp_url(event_id, wm_week, wm_year) if event_id else ""

        if amp_url and amp_url in existing_urls:
            stats["skipped"] += 1
            continue

        # Parse Keywords for additional field data
        keywords = event.get("keywords", "") or ""
        parsed = parse_keywords(keywords)

        # Map to intake row
        row = map_amp_to_request(event, parsed)

        # Check completeness
        is_complete, missing = check_completeness(row)
        if is_complete:
            row["Status"] = "Review"
            row["AMP_Input"] = ""
        else:
            row["Status"] = "Pending"
            row["AMP_Input"] = f"Missing: {', '.join(missing)}"

        # Insert
        success = db.insert_amp_request(row)
        if success:
            stats["new"] += 1
            existing_urls.add(amp_url)  # Track for this batch
            print(f"[AMP Sync] Inserted: {row['Title']} (Status: {row['Status']})")
        else:
            stats["errors"] += 1

    print(f"[AMP Sync] Complete — New: {stats['new']}, Skipped: {stats['skipped']}, Errors: {stats['errors']}")
    return stats
