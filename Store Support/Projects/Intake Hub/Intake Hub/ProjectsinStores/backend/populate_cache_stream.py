"""Optimized streaming cache population"""
import sys
import os
import sqlite3
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from database import DatabaseService

print("🚀 Optimized cache population with streaming\n")

db_service = DatabaseService()
if not db_service.client:
    print("❌ BigQuery client not available")
    sys.exit(1)

db_path = Path(__file__).parent / "projects_cache.db"

# Delete old
if db_path.exists():
    db_path.unlink()

# Create new
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()
cursor.execute("""CREATE TABLE projects (
    project_id TEXT, intake_card TEXT, title TEXT, project_source TEXT, division TEXT,
    region TEXT, market TEXT, store TEXT, facility TEXT, phase TEXT, wm_week INTEGER,
    fy INTEGER, status TEXT, owner TEXT, partner TEXT, store_area TEXT, business_area TEXT,
    health TEXT, business_type TEXT, associate_impact TEXT, customer_impact TEXT, last_updated TEXT
)""")

print("📊 Streaming data from BigQuery...")

query = f"""
    SELECT 
        COALESCE(CAST(Intake_Card AS STRING), CAST(PROJECT_ID AS STRING), Unique_Key, CONCAT('FAC-', CAST(Facility AS STRING))) as project_id,
        CAST(Intake_Card AS STRING) as intake_card,
        CASE
            WHEN Title IS NOT NULL AND Title != '' THEN Title
            WHEN Project_Type IS NOT NULL AND Project_Type != 'None' AND Project_Type != '' 
                 AND Initiative_Type IS NOT NULL AND Initiative_Type != '' 
                THEN CONCAT(Project_Type, ' - ', Initiative_Type)
            WHEN Initiative_Type IS NOT NULL AND Initiative_Type != '' THEN Initiative_Type
            ELSE 'Untitled'
        END as title,
        Project_Source as project_source,
        Division as division, Region as region, Market as market,
        CAST(Facility AS STRING) as store, CAST(Facility AS STRING) as facility,
        Phase as phase, WM_Week as wm_week, FY as fy, Status as status,
        COALESCE(Owner, PROJECT_OWNER, '') as owner, '' as partner,
        COALESCE(Store_Area, '') as store_area, COALESCE(Business_Area, '') as business_area,
        COALESCE(Health, PROJECT_HEALTH_DESC, PROJECT_HEALTH, '') as health,
        COALESCE(Business_Type, '') as business_type,
        COALESCE(ASSOCIATE_IMPACT_DESC, ASSOCIATE_IMPACT, '') as associate_impact,
        COALESCE(CUSTOMER_IMPACT_DESC, CUSTOMER_IMPACT, '') as customer_impact,
        COALESCE(Last_Updated, UPDATE_TS) as last_updated
    FROM `{db_service.project_id}.{db_service.dataset}.{db_service.table}`
    WHERE Status = 'Active'
    ORDER BY Title, WM_Week
"""

insert_sql = """INSERT INTO projects VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

result = db_service.client.query(query)
rows_iter = result.result()  # Get iterator instead of list

batch = []
count = 0
for row in rows_iter:
    batch.append((
        row.project_id, row.intake_card, row.title, row.project_source, row.division, row.region,
        row.market, row.store, row.facility, row.phase, row.wm_week, row.fy, row.status, row.owner,
        row.partner, row.store_area, row.business_area, row.health, row.business_type,
        row.associate_impact, row.customer_impact, row.last_updated.isoformat() if row.last_updated else None
    ))
    count += 1
    
    if len(batch) >= 10000:
        cursor.executemany(insert_sql, batch)
        print(f"  Inserted {count:,} rows...")
        batch = []

if batch:
    cursor.executemany(insert_sql, batch)

conn.commit()

# Verify
cursor.execute("SELECT COUNT(*) FROM projects")
total = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM projects WHERE project_source = 'Realty' AND project_id LIKE 'FAC-%'")
realty_fac = cursor.fetchone()[0]

conn.close()

print(f"\n✅ Complete! Total: {total:,}, Realty with FAC-: {realty_fac:,}")
if realty_fac > 0:
    print("   Restart server to load cache")
