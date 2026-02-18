# Data Caching Options for Projects in Stores

## Problem
Querying BigQuery for every request is slow (2-5 seconds). Need faster data access.

---

## Option 1: Local JSON File Cache (Simplest)
- A background job runs every 5-15 minutes
- Pulls data from BigQuery and saves to a local `.json` file
- Dashboard reads from the JSON file (instant) instead of BigQuery

**Pros:**
- Simple to implement
- No extra dependencies

**Cons:**
- File can get large with 100K+ records
- No query flexibility (must load entire file)

---

## Option 2: SQLite Local Database ⭐ (IMPLEMENTED)
- A lightweight database file stored locally (`projects_cache.db`)
- Background sync pulls from BigQuery every 15 minutes
- Dashboard queries SQLite (milliseconds) instead of BigQuery (seconds)

**Pros:**
- Fast queries (milliseconds)
- Can filter/sort locally
- Small footprint
- Data persists across restarts

**Cons:**
- Slightly more complex setup

**Implementation:**
- `sqlite_cache.py` - manages the SQLite database
- Background thread syncs from BigQuery every 15 minutes
- API endpoints hit SQLite first, fall back to BigQuery if needed

---

## Option 3: In-Memory Cache with File Backup
- Keep all data in Python memory
- Save to disk on shutdown, reload on startup
- Background thread refreshes from BQ periodically

**Pros:**
- Fastest possible reads (everything in RAM)

**Cons:**
- Uses more RAM
- Data lost if server crashes before save

---

## Recommendation
**Option 2 (SQLite)** provides the best balance of:
- Speed (millisecond queries)
- Reliability (persists to disk)
- Flexibility (SQL queries still work)
- Memory efficiency (doesn't load everything into RAM)

---

## Architecture (Option 2)

```
┌─────────────────────────────────────────────────────────┐
│                    User Request                          │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                   FastAPI Server                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │              SQLite Cache                        │    │
│  │  • projects_cache.db                            │    │
│  │  • Queries return in milliseconds               │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────┬───────────────────────────────────┘
                      │
         Background Sync (every 15 min)
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                   BigQuery                               │
│  • wmt-assetprotection-prod.Store_Support_Dev           │
│  • IH_Intake_Data table                                 │
└─────────────────────────────────────────────────────────┘
```

---

## Files Created
- `backend/sqlite_cache.py` - SQLite cache manager
- `backend/projects_cache.db` - SQLite database file (auto-created)

## Configuration
- Sync interval: 15 minutes (configurable in sqlite_cache.py)
- Cache file location: `backend/projects_cache.db`
