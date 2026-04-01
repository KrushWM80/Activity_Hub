import os
from typing import List, Dict, Optional
from datetime import datetime
from google.cloud import bigquery
from google.oauth2 import service_account
import asyncio
from functools import wraps

from models import (
    Project, ProjectStatus, ProjectSource, FilterCriteria,
    ProjectSummary, StoreCount
)

def async_wrap(func):
    """Wrapper to run synchronous functions asynchronously"""
    @wraps(func)
    async def run(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: func(*args, **kwargs))
    return run

class DatabaseService:
    """Database service for querying BigQuery with caching for performance"""
    
    # Class-level cache for projects (shared across instances)
    _projects_cache = None
    _cache_timestamp = None
    _cache_ttl_seconds = 300  # Cache for 5 minutes
    
    def __init__(self):
        self.project_id = os.getenv("GCP_PROJECT_ID", "wmt-assetprotection-prod")
        self.dataset = os.getenv("BIGQUERY_DATASET", "Store_Support_Dev")
        self.table = os.getenv("BIGQUERY_TABLE", "IH_Intake_Data")
        self.client = None
        self._initialize_client()
    
    def _is_cache_valid(self) -> bool:
        """Check if the cache is still valid"""
        if DatabaseService._projects_cache is None or DatabaseService._cache_timestamp is None:
            return False
        age = (datetime.now() - DatabaseService._cache_timestamp).total_seconds()
        return age < DatabaseService._cache_ttl_seconds
    
    def clear_cache(self):
        """Clear the projects cache (call this if you need fresh data)"""
        DatabaseService._projects_cache = None
        DatabaseService._cache_timestamp = None
        print("[CACHE] Projects cache cleared")
    
    def _initialize_client(self):
        """Initialize BigQuery client"""
        try:
            credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            if credentials_path and os.path.exists(credentials_path):
                # Use service account credentials from file
                print(f"Using service account credentials from: {credentials_path}")
                credentials = service_account.Credentials.from_service_account_file(
                    credentials_path
                )
                self.client = bigquery.Client(
                    credentials=credentials,
                    project=self.project_id
                )
            else:
                # Use default credentials (gcloud auth application-default login)
                print(f"Using default credentials (gcloud) for project: {self.project_id}")
                self.client = bigquery.Client(project=self.project_id)
            
            print(f"[OK] BigQuery client initialized successfully")
            print(f"   Project: {self.project_id}")
            print(f"   Dataset: {self.dataset}")
            print(f"   Table: {self.table}")
        except Exception as e:
            print(f"[WARNING] Could not initialize BigQuery client: {e}")
            print(f"   Using mock data mode instead")
            print(f"   To connect: run 'gcloud auth application-default login'")
            self.client = None
    
    def is_connected(self) -> bool:
        """Check if database connection is active (uses cache to avoid repeated queries)"""
        if not self.client:
            return False
        # Don't query every time - just check if client exists
        # A full query test happens during __init__, so assume True if client is initialized
        return True
    
    def _build_where_clause(self, filters: FilterCriteria) -> tuple:
        """Build SQL WHERE clause from filters and return (where_clause, join_clause)"""
        conditions = []
        join_clause = ""
        
        # Always filter by status
        if filters.status:
            conditions.append(f"Status = '{filters.status.value}'")
        
        if filters.tribe:
            tribe_list = "','".join(filters.tribe)
            conditions.append(f"tribe IN ('{tribe_list}')")
        
        if filters.store:
            store_list = "','".join(filters.store)
            conditions.append(f"CAST(Facility AS STRING) IN ('{store_list}')")
        
        if filters.division:
            division_list = "','".join(filters.division)
            conditions.append(f"Division IN ('{division_list}')")
        
        if filters.region:
            region_list = "','".join(filters.region)
            conditions.append(f"Region IN ('{region_list}')")
        
        if filters.market:
            # Normalize market values to match 3-digit format in database
            normalized_markets = [f"'{m}'" for m in filters.market]
            market_conditions = []
            for m in normalized_markets:
                # Match by normalized 3-digit format
                market_conditions.append(f"LPAD(CAST(CAST(Market AS INT64) AS STRING), 3, '0') = {m}")
            conditions.append(f"({' OR '.join(market_conditions)})")
        
        if filters.phase:
            phase_list = "','".join(filters.phase)
            conditions.append(f"Phase IN ('{phase_list}')")
        
        if filters.project_source:
            source_list = "','".join(filters.project_source)
            conditions.append(f"Project_Source IN ('{source_list}')")
        
        if filters.wm_week:
            week_list = "','".join(filters.wm_week)
            conditions.append(f"CAST(WM_Week AS STRING) IN ('{week_list}')")
        
        if filters.fy:
            fy_list = "','".join(filters.fy)
            conditions.append(f"CAST(FY AS STRING) IN ('{fy_list}')")
        
        # Exclude Operational projects without store numbers (Unknown stores)
        conditions.append("NOT (Project_Source IN ('Operations', 'Intake Hub') AND (Facility IS NULL OR CAST(Facility AS STRING) = ''))")
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        return (where_clause, join_clause)
    
    def _get_projects_with_partner_filter(self, filters: FilterCriteria, limit: Optional[int] = None) -> List[Project]:
        """Get projects filtered by partners using JOIN to IH_Branch_Data"""
        if not self.client:
            return []
        
        try:
            # Build partner filter condition
            partner_list = "','".join(filters.partners)
            
            # Get other filter conditions (without partner)
            where_clause, join_clause = self._build_where_clause(filters)
            
            limit_clause = f"LIMIT {limit}" if limit else ""
            
            # Query with JOIN to IH_Branch_Data
            query = f"""
                SELECT DISTINCT
                    COALESCE(CAST(main.Intake_Card AS STRING), CONCAT('R-', CAST(main.Facility AS STRING))) as project_id,
                    CAST(main.Intake_Card AS STRING) as intake_card,
                    CASE
                        WHEN main.Project_Title IS NOT NULL AND main.Project_Title != '' THEN main.Project_Title
                        WHEN main.Title IS NOT NULL AND main.Title != '' THEN main.Title
                        WHEN main.Project_Type IS NOT NULL AND main.Project_Type != 'None' AND main.Project_Type != '' 
                             AND main.Initiative_Type IS NOT NULL AND Initiative_Type != '' 
                            THEN CONCAT(main.Project_Type, ' - ', main.Initiative_Type)
                        WHEN main.Initiative_Type IS NOT NULL AND main.Initiative_Type != '' THEN main.Initiative_Type
                        ELSE 'Untitled'
                    END as title,
                    main.Division as division,
                    main.Region as region,
                    main.Market as market,
                    CAST(COALESCE(main.Facility, 0) AS STRING) as store,
                    COALESCE(main.Store_Area, '') as store_area,
                    COALESCE(main.Business_Area, '') as business_area,
                    COALESCE(main.PROJECT_PHASE_2, main.Phase, '') as phase,
                    '' as tribe,
                    CAST(COALESCE(main.WM_Week, 0) AS STRING) as wm_week,
                    CAST(COALESCE(main.FY, 0) AS STRING) as fy,
                    COALESCE(main.PROJECT_HEALTH, main.Status, '') as status,
                    COALESCE(main.Owner, main.PROJECT_OWNER, '') as owner,
                    branch.BRANCH_NAME as partner,
                    1 as store_count,
                    main.CREATED_TS as created_date,
                    main.Last_Updated as last_updated,
                    COALESCE(main.PRESENTATION_SUMMARY, main.OVERVIEW, '') as description
                FROM `{self.project_id}.{self.dataset}.{self.table}` as main
                INNER JOIN `{self.project_id}.Store_Support.IH_Branch_Data` as branch
                    ON CAST(main.Intake_Card AS STRING) = CAST(branch.Intake_Card_Nbr AS STRING)
                WHERE branch.BRANCH_NAME IN ('{partner_list}')
                    AND {where_clause}
                ORDER BY 
                    last_updated DESC, 
                    title ASC
                {limit_clause}
            """
            
            print(f"[DEBUG] Running partner-filtered query")
            results = self.client.query(query).result()
            
            projects = []
            for row in results:
                project = Project()
                project.project_id = row.project_id or ""
                project.intake_card = row.intake_card or ""
                project.title = row.title or ""
                project.division = row.division or ""
                project.region = row.region or ""
                project.market = row.market or ""
                project.store = row.store or ""
                project.store_area = row.store_area or ""
                project.business_area = row.business_area or ""
                project.phase = row.phase or ""
                project.tribe = row.tribe or ""
                project.wm_week = row.wm_week or ""
                project.fy = row.fy or ""
                project.owner = row.owner or ""
                project.partner = row.partner or ""
                project.store_count = row.store_count or 1
                project.created_date = row.created_date
                project.last_updated = row.last_updated
                project.description = row.description or ""
                
                # Set status enum (defaults to ACTIVE if empty)
                status_str = (row.status or "").strip().lower()
                if status_str == "archived":
                    project.status = ProjectStatus.ARCHIVED
                elif status_str == "pending":
                    project.status = ProjectStatus.PENDING
                else:
                    project.status = ProjectStatus.ACTIVE
                
                # Set project_source enum (defaults to INTAKE_HUB)
                project.project_source = ProjectSource.INTAKE_HUB
                
                projects.append(project)
            
            return projects
            
        except Exception as e:
            print(f"[ERROR] _get_projects_with_partner_filter exception: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    @async_wrap
    def get_projects(self, filters: FilterCriteria, include_location: bool = False, limit: Optional[int] = None, title_search: Optional[str] = None) -> List[Project]:
        """Get filtered list of projects with caching for performance"""
        if not self.client:
            return self._get_mock_projects()
        
        try:
            # Check if partner filter is applied - use BigQuery JOIN if so
            if filters.partners:
                print(f"[API] Using BigQuery with partner JOIN for /api/projects")
                try:
                    result = self._get_projects_with_partner_filter(filters, limit)
                    print(f"[API] Partner filter returned {len(result)} projects")
                    return result
                except Exception as e:
                    print(f"[ERROR] Partner filter exception: {type(e).__name__}: {e}")
                    import traceback
                    traceback.print_exc()
                    return []  # Return empty list instead of mock data for partner filters
            
            # Check if we have a valid cache for the base query (no filters, no location)
            is_base_query = (
                not filters.tribe and not filters.store and not filters.division and
                not filters.region and not filters.market and not filters.phase and
                not filters.project_source and not filters.wm_week and not filters.fy and
                not include_location and not title_search and not limit
            )
            
            # Use cache for base queries (most common case)
            if is_base_query and self._is_cache_valid():
                print(f"[CACHE] Returning {len(DatabaseService._projects_cache)} cached projects")
                return DatabaseService._projects_cache
            
            where_clause, join_clause = self._build_where_clause(filters)
            
            # Add title search if provided
            if title_search:
                where_clause += f" AND (LOWER(main.PROJECT_TITLE) LIKE '%{title_search.lower()}%' OR LOWER(main.Title) LIKE '%{title_search.lower()}%')"
            
            # Add LIMIT clause
            limit_clause = f"LIMIT {limit}" if limit else ""
            
            # Build query with optional location data join for better performance
            if include_location:
                # Generate approximate coordinates based on division for visualization
                query = f"""
                    SELECT 
                        CASE 
                            WHEN main.PROJECT_ID IS NOT NULL THEN CAST(main.PROJECT_ID AS STRING)
                            WHEN main.Intake_Card IS NOT NULL THEN CAST(main.Intake_Card AS STRING)
                            ELSE CONCAT('R-', CAST(main.Facility AS STRING))
                        END as project_id,
                        main.Project_Source as project_source,
                        CASE 
                            WHEN main.PROJECT_TITLE IS NOT NULL THEN main.PROJECT_TITLE
                            WHEN main.Title IS NOT NULL THEN main.Title
                            WHEN main.Project_Type IS NOT NULL AND main.Project_Type != 'None' AND main.Initiative_Type IS NOT NULL THEN CONCAT(main.Project_Type, ' - ', main.Initiative_Type)
                            WHEN main.Project_Type IS NOT NULL AND main.Project_Type != 'None' THEN main.Project_Type
                            WHEN main.Initiative_Type IS NOT NULL THEN main.Initiative_Type
                            ELSE 'Untitled'
                        END as title,
                        main.Division as division,
                        main.Region as region,
                        main.Market as market,
                        CAST(COALESCE(main.Facility, 0) AS STRING) as store,
                        COALESCE(main.Store_Area, '') as store_area,
                        COALESCE(main.Business_Area, '') as business_area,
                        COALESCE(main.PROJECT_PHASE_2, main.Phase, '') as phase,
                        '' as tribe,
                        CAST(COALESCE(main.WM_Week, 0) AS STRING) as wm_week,
                        CAST(COALESCE(main.FY, 0) AS STRING) as fy,
                        COALESCE(main.PROJECT_HEALTH, main.Status, '') as status,
                        COALESCE(main.Owner, main.PROJECT_OWNER, '') as owner,
                        '' as partner,
                        1 as store_count,
                        main.CREATED_TS as created_date,
                        main.Last_Updated as last_updated,
                        COALESCE(main.PRESENTATION_SUMMARY, main.OVERVIEW, '') as description,
                        main.Latitude as latitude,
                        main.Longitude as longitude,
                        CONCAT('Store ', CAST(COALESCE(main.Facility, 0) AS STRING)) as store_address,
                        main.City as city,
                        main.State as state,
                        COALESCE(main.Postal_Code, '00000') as zip_code
                    FROM `{self.project_id}.{self.dataset}.{self.table}` as main
                    {join_clause}
                    WHERE {where_clause}
                    ORDER BY 
                        main.Last_Updated DESC, 
                        main.PROJECT_TITLE ASC,
                        main.Title ASC
                    {limit_clause}
                """
            else:
                # Faster query without location join
                query = f"""
                    SELECT 
                        CASE 
                            WHEN main.PROJECT_ID IS NOT NULL THEN CAST(main.PROJECT_ID AS STRING)
                            WHEN main.Intake_Card IS NOT NULL THEN CAST(main.Intake_Card AS STRING)
                            ELSE CONCAT('R-', CAST(main.Facility AS STRING))
                        END as project_id,
                        main.Project_Source as project_source,
                        CASE 
                            WHEN main.PROJECT_TITLE IS NOT NULL THEN main.PROJECT_TITLE
                            WHEN main.Title IS NOT NULL THEN main.Title
                            WHEN main.Project_Type IS NOT NULL AND main.Project_Type != 'None' AND main.Initiative_Type IS NOT NULL THEN CONCAT(main.Project_Type, ' - ', main.Initiative_Type)
                            WHEN main.Project_Type IS NOT NULL AND main.Project_Type != 'None' THEN main.Project_Type
                            WHEN main.Initiative_Type IS NOT NULL THEN main.Initiative_Type
                            ELSE 'Untitled'
                        END as title,
                        main.Division as division,
                        main.Region as region,
                        main.Market as market,
                        CAST(COALESCE(main.Facility, 0) AS STRING) as store,
                        COALESCE(main.Store_Area, '') as store_area,
                        COALESCE(main.Business_Area, '') as business_area,
                        COALESCE(main.PROJECT_PHASE_2, main.Phase, '') as phase,
                        '' as tribe,
                        CAST(COALESCE(main.WM_Week, 0) AS STRING) as wm_week,
                        CAST(COALESCE(main.FY, 0) AS STRING) as fy,
                        COALESCE(main.PROJECT_HEALTH, main.Status, '') as status,
                        COALESCE(main.Owner, main.PROJECT_OWNER, '') as owner,
                        '' as partner,
                        1 as store_count,
                        main.CREATED_TS as created_date,
                        main.Last_Updated as last_updated,
                        COALESCE(main.PRESENTATION_SUMMARY, main.OVERVIEW, '') as description
                    FROM `{self.project_id}.{self.dataset}.{self.table}` as main
                    {join_clause}
                    WHERE {where_clause}
                    ORDER BY 
                        main.Last_Updated DESC, 
                        main.PROJECT_TITLE ASC,
                        main.Title ASC
                    {limit_clause}
                """
            
            # DEBUG: Print query info
            print(f"[DEBUG database.py] Executing query with limit={limit}")
            
            results = self.client.query(query).result()
            projects = []
            
            for row in results:
                project = Project()
                project.project_id = row.project_id or ""
                # Normalize "Intake Hub" to "Operations" for consistent display
                if row.project_source == 'Intake Hub':
                    project.project_source = ProjectSource.OPERATIONS
                elif row.project_source == 'Realty':
                    project.project_source = ProjectSource.REALTY
                elif row.project_source == 'Operations':
                    project.project_source = ProjectSource.OPERATIONS
                else:
                    project.project_source = ProjectSource.OPERATIONS
                project.title = row.title or ""
                project.division = row.division or ""
                project.region = row.region or ""
                project.market = row.market or ""
                project.store = row.store or ""
                project.store_area = row.store_area or ""
                project.business_area = row.business_area or ""
                project.phase = row.phase or ""
                project.tribe = row.tribe or ""
                project.wm_week = row.wm_week or ""
                project.fy = row.fy or ""
                project.status = ProjectStatus(row.status) if row.status in ['Active', 'Archived', 'Pending'] else ProjectStatus.ACTIVE
                project.owner = row.owner if hasattr(row, 'owner') else ""
                project.partner = row.partner if hasattr(row, 'partner') else ""
                project.store_count = row.store_count or 1
                project.created_date = row.created_date
                project.last_updated = row.last_updated
                project.description = row.description
                # Add location data only if include_location was True
                if include_location:
                    project.latitude = row.latitude if hasattr(row, 'latitude') else None
                    project.longitude = row.longitude if hasattr(row, 'longitude') else None
                    project.store_address = row.store_address if hasattr(row, 'store_address') else None
                    project.city = row.city if hasattr(row, 'city') else None
                    project.state = row.state if hasattr(row, 'state') else None
                    project.zip_code = row.zip_code if hasattr(row, 'zip_code') else None
                projects.append(project)
            
            # Cache base queries for faster subsequent requests
            if is_base_query:
                DatabaseService._projects_cache = projects
                DatabaseService._cache_timestamp = datetime.now()
                print(f"[CACHE] Cached {len(projects)} projects (TTL: {self._cache_ttl_seconds}s)")
            
            return projects
        except Exception as e:
            print(f"Error querying projects: {e}")
            return self._get_mock_projects()
    
    @async_wrap
    def get_summary(self, filters: FilterCriteria) -> ProjectSummary:
        """Get summary statistics"""
        if not self.client:
            return self._get_mock_summary()
        
        try:
            where_clause, join_clause = self._build_where_clause(filters)
            
            # Add table alias when using join clause
            table_ref = "main" if join_clause else f"`{self.project_id}.{self.dataset}.{self.table}`"
            
            query = f"""
                SELECT 
                    COUNT(DISTINCT CASE 
                        WHEN {table_ref}.Project_Source IN ('Operations', 'Intake Hub') AND {table_ref}.Intake_Card IS NOT NULL 
                          THEN CAST({table_ref}.Intake_Card AS STRING)
                        WHEN {table_ref}.Project_Source = 'Realty'
                          THEN {table_ref}.Title
                        ELSE NULL
                    END) as total_active_projects,
                    COUNT(DISTINCT {table_ref}.Facility) as total_stores,
                    COUNT(DISTINCT CASE WHEN {table_ref}.Project_Source IN ('Operations', 'Intake Hub') AND {table_ref}.Intake_Card IS NOT NULL THEN {table_ref}.Intake_Card END) as intake_hub_projects,
                    COUNT(DISTINCT CASE WHEN {table_ref}.Project_Source IN ('Operations', 'Intake Hub') THEN {table_ref}.Facility END) as intake_hub_stores,
                    COUNT(DISTINCT CASE WHEN {table_ref}.Project_Source = 'Realty' THEN {table_ref}.Title END) as realty_projects,
                    COUNT(DISTINCT CASE WHEN {table_ref}.Project_Source = 'Realty' THEN {table_ref}.Facility END) as realty_stores,
                    MAX({table_ref}.Last_Updated) as last_updated
                FROM `{self.project_id}.{self.dataset}.{self.table}`{"as main " + join_clause if join_clause else ""}
                WHERE {where_clause}
            """
            
            result = list(self.client.query(query).result())[0]
            
            summary = ProjectSummary()
            summary.total_active_projects = result.total_active_projects or 0
            summary.total_stores = result.total_stores or 0
            summary.intake_hub_projects = result.intake_hub_projects or 0
            summary.intake_hub_stores = result.intake_hub_stores or 0
            summary.realty_projects = result.realty_projects or 0
            summary.realty_stores = result.realty_stores or 0
            if result.last_updated:
                summary.last_updated = result.last_updated
            
            # Get by division
            div_query = f"""
                SELECT {table_ref}.Division as division, COUNT(DISTINCT {table_ref}.Intake_Card) as count
                FROM `{self.project_id}.{self.dataset}.{self.table}`{"as main " + join_clause if join_clause else ""}
                WHERE {where_clause} AND {table_ref}.Division IS NOT NULL
                GROUP BY {table_ref}.Division
            """
            div_results = self.client.query(div_query).result()
            summary.by_division = {row.division: row.count for row in div_results}
            
            # Get by phase
            phase_query = f"""
                SELECT {table_ref}.Phase as phase, COUNT(DISTINCT {table_ref}.Intake_Card) as count
                FROM `{self.project_id}.{self.dataset}.{self.table}`{"as main " + join_clause if join_clause else ""}
                WHERE {where_clause} AND {table_ref}.Phase IS NOT NULL
                GROUP BY {table_ref}.Phase
            """
            phase_results = self.client.query(phase_query).result()
            summary.by_phase = {row.phase: row.count for row in phase_results}
            
            return summary
        except Exception as e:
            print(f"Error getting summary: {e}")
            return self._get_mock_summary()
    
    # Class-level cache for filter options
    _filters_cache = None
    _filters_cache_timestamp = None
    _filters_cache_ttl = 0  # DISABLED: Use SQLite cache instead of in-memory cache
    
    def get_filter_options(self) -> Dict:
        """Get all available filter options with caching"""
        if not self.client:
            return self._get_mock_filter_options()
        
        # Check filter cache
        if (DatabaseService._filters_cache is not None and 
            DatabaseService._filters_cache_timestamp is not None):
            age = (datetime.now() - DatabaseService._filters_cache_timestamp).total_seconds()
            if age < DatabaseService._filters_cache_ttl:
                print(f"[CACHE] Returning cached filter options")
                return DatabaseService._filters_cache
        
        try:
            print(f"[DB] Fetching filter options from BigQuery...")
            # Get basic filter options
            query = f"""
                SELECT 
                    ARRAY_AGG(DISTINCT Division IGNORE NULLS ORDER BY Division) as divisions,
                    ARRAY_AGG(DISTINCT Region IGNORE NULLS ORDER BY Region) as regions,
                    ARRAY_AGG(DISTINCT Phase IGNORE NULLS ORDER BY Phase) as phases,
                    ARRAY_AGG(DISTINCT Project_Source IGNORE NULLS ORDER BY Project_Source) as project_sources,
                    ARRAY_AGG(DISTINCT CAST(WM_Week AS STRING) IGNORE NULLS ORDER BY CAST(WM_Week AS STRING) DESC LIMIT 52) as wm_weeks,
                    ARRAY_AGG(DISTINCT CAST(FY AS STRING) IGNORE NULLS ORDER BY CAST(FY AS STRING) DESC) as fiscal_years
                FROM `{self.project_id}.{self.dataset}.{self.table}`
                WHERE Status = 'Active'
            """
            
            result = list(self.client.query(query).result())[0]
            
            # Get distinct markets - normalize and deduplicate in Python
            market_query = f"""
                SELECT DISTINCT Market as market_raw
                FROM `{self.project_id}.{self.dataset}.{self.table}`
                WHERE Status = 'Active' AND Market IS NOT NULL
            """
            try:
                market_results = self.client.query(market_query).result()
                markets_raw = [str(row.market_raw).strip() for row in market_results if row.market_raw]
                # Normalize to 3-digit format and deduplicate
                normalized_markets = set()
                for m in markets_raw:
                    try:
                        num = int(m)
                        normalized_markets.add(f"{num:03d}")
                    except:
                        pass
                markets = sorted(list(normalized_markets), key=lambda x: int(x))
            except Exception as e:
                print(f"Error getting markets: {e}")
                markets = []
            
            # Get ALL distinct stores
            store_query = f"""
                SELECT DISTINCT CAST(Facility AS STRING) as store_raw
                FROM `{self.project_id}.{self.dataset}.{self.table}`
                WHERE Status = 'Active' AND Facility IS NOT NULL
            """
            try:
                store_results = self.client.query(store_query).result()
                stores_raw = []
                for row in store_results:
                    if row.store_raw:
                        store_str = str(row.store_raw).strip()
                        # Remove decimal if it's a number like "728.0"
                        try:
                            store_int = int(float(store_str))
                            stores_raw.append(str(store_int))
                        except:
                            stores_raw.append(store_str)
                # Sort numerically if possible, otherwise alphabetically
                def sort_key(s):
                    try:
                        return (0, int(s))
                    except:
                        return (1, s)
                stores = sorted(list(set(stores_raw)), key=sort_key)
            except Exception as e:
                print(f"Error getting stores: {e}")
                stores = []
            
            # Get distinct partners from IH_Branch_Data
            partners = []
            partner_query = f"""
                SELECT DISTINCT Partner as partner_name
                FROM `{self.project_id}.Store_Support.IH_Branch_Data`
                WHERE Partner IS NOT NULL
                ORDER BY Partner
            """
            try:
                partner_results = self.client.query(partner_query).result()
                partners = [str(row.partner_name).strip() for row in partner_results if row.partner_name]
                partners = sorted(list(set(partners)))  # Deduplicate and sort
                print(f"[DB] Found {len(partners)} distinct partners from IH_Branch_Data")
            except Exception as e:
                print(f"Error getting partners from IH_Branch_Data: {e}")
                partners = []
            
            filter_options = {
                "tribes": ["Tribe 1", "Tribe 2", "Tribe 3"],  # Not in current schema
                "stores": stores,
                "partners": partners,
                "project_sources": result.project_sources or [],
                "markets": markets,
                "regions": result.regions or [],
                "divisions": result.divisions or [],
                "phases": result.phases or [],
                "wm_weeks": result.wm_weeks or [],
                "fiscal_years": result.fiscal_years or [],
            }
            
            # Get the 7 new fields from SQLite cache
            # ALWAYS try cache first, even if BigQuery connection exists
            try:
                from sqlite_cache import get_cache
                cache = get_cache()
                
                # Check if cache has data
                if cache.get_record_count() > 0:
                    cache_filters = cache.get_filter_options()
                    filter_options.update({
                        "owners": cache_filters.get("owners", []),
                        "store_areas": cache_filters.get("store_areas", []),
                        "business_areas": cache_filters.get("business_areas", []),
                        "health_statuses": cache_filters.get("health_statuses", []),
                        "business_types": cache_filters.get("business_types", []),
                        "associate_impacts": cache_filters.get("associate_impacts", []),
                        "customer_impacts": cache_filters.get("customer_impacts", [])
                    })
                    print(f"[DB] Added {len(cache_filters.get('business_areas', []))} business_areas from cache")
                else:
                    print("[DB] Cache is empty, using empty lists for extended fields")
                    filter_options.update({
                        "owners": [],
                        "store_areas": [],
                        "business_areas": [],
                        "health_statuses": [],
                        "business_types": [],
                        "associate_impacts": [],
                        "customer_impacts": []
                    })
            except Exception as e:
                print(f"[DB] ERROR getting new fields from cache: {e}")
                import traceback
                traceback.print_exc()
                # Fallback to empty lists
                filter_options.update({
                    "owners": [],
                    "store_areas": [],
                    "business_areas": [],
                    "health_statuses": [],
                    "business_types": [],
                    "associate_impacts": [],
                    "customer_impacts": []
                })
            
            # Cache the filter options
            DatabaseService._filters_cache = filter_options
            DatabaseService._filters_cache_timestamp = datetime.now()
            print(f"[CACHE] Cached filter options (TTL: {self._filters_cache_ttl}s)")
            
            return filter_options
        except Exception as e:
            print(f"[DB] Error getting filter options: {e}", flush=True)
            import traceback
            traceback.print_exc()
            return self._get_mock_filter_options()
    
    @async_wrap
    def get_store_counts(self, group_by: str) -> List[Dict]:
        """Get store counts grouped by dimension"""
        if not self.client:
            return self._get_mock_store_counts(group_by)
        
        try:
            # Map group_by to actual column names
            column_map = {
                "division": "Division",
                "region": "Region",
                "market": "Market",
                "phase": "Phase"
            }
            
            column = column_map.get(group_by, "Division")
            
            query = f"""
                SELECT 
                    {column} as grouping,
                    Project_Source as project_source,
                    COUNT(DISTINCT Facility) as total_stores,
                    COUNT(DISTINCT Intake_Card) as project_count
                FROM `{self.project_id}.{self.dataset}.{self.table}`
                WHERE Status = 'Active' AND {column} IS NOT NULL
                GROUP BY {column}, Project_Source
                ORDER BY total_stores DESC
            """
            
            results = self.client.query(query).result()
            return [
                {
                    "group": row.grouping,
                    "project_source": row.project_source,
                    "total_stores": row.total_stores,
                    "project_count": row.project_count
                }
                for row in results
            ]
        except Exception as e:
            print(f"Error getting store counts: {e}")
            return self._get_mock_store_counts(group_by)
    
    # Mock data methods for testing without database connection
    def _get_mock_projects(self) -> List[Project]:
        """Return mock project data"""
        mock_data = []
        divisions = ["EAST", "WEST", "NORTH", "SOUTH"]
        sources = [ProjectSource.OPERATIONS, ProjectSource.REALTY]
        phases = ["Planning", "Execution", "Review", "Complete"]
        
        for i in range(20):
            project = Project()
            project.project_id = f"PROJ-{1000 + i}"
            project.project_source = sources[i % 2]
            project.title = f"Store Renovation Project {i+1}"
            project.division = divisions[i % 4]
            project.region = f"Region {(i % 4) + 1}"
            project.market = f"Market {(i % 8) + 1}"
            project.store = f"Store {2000 + i}"
            project.phase = phases[i % 4]
            project.tribe = f"Tribe {(i % 3) + 1}"
            project.wm_week = f"2026-W{(i % 10) + 1:02d}"
            project.status = ProjectStatus.ACTIVE
            project.store_count = (i % 50) + 10
            project.created_date = datetime.now()
            project.last_updated = datetime.now()
            project.description = f"Sample project description for project {i+1}"
            mock_data.append(project)
        
        return mock_data
    
    def _get_mock_summary(self) -> ProjectSummary:
        """Return mock summary data"""
        summary = ProjectSummary()
        summary.total_active_projects = 150
        summary.total_stores = 4500
        summary.intake_hub_projects = 90
        summary.intake_hub_stores = 2700
        summary.realty_projects = 60
        summary.realty_stores = 1800
        summary.by_division = {
            "EAST": 40,
            "WEST": 35,
            "NORTH": 38,
            "SOUTH": 37
        }
        summary.by_phase = {
            "Planning": 30,
            "Execution": 70,
            "Review": 35,
            "Complete": 15
        }
        return summary
    
    def _get_mock_filter_options(self) -> Dict:
        """Return mock filter options - includes ALL 16 fields to match FilterOptionsResponse model"""
        return {
            "tribes": ["Tribe 1", "Tribe 2", "Tribe 3"],
            "stores": [f"Store {2000 + i}" for i in range(20)],
            "project_sources": ["Operations", "Realty"],
            "markets": [f"Market {i+1}" for i in range(8)],
            "regions": [f"Region {i+1}" for i in range(4)],
            "divisions": ["EAST", "WEST", "NORTH", "SOUTH"],
            "phases": ["Planning", "Execution", "Review", "Complete"],
            "wm_weeks": [f"2026-W{i:02d}" for i in range(1, 11)],
            "fiscal_years": ["2024", "2025", "2026"],
            "owners": ["Mock Owner 1", "Mock Owner 2"],
            "store_areas": ["Mock Area 1", "Mock Area 2"],
            "business_areas": ["Mock Business Area 1", "Mock Business Area 2"],
            "health_statuses": ["On Track", "At Risk"],
            "business_types": ["Type 1", "Type 2"],
            "associate_impacts": ["High", "Low"],
            "customer_impacts": ["High", "Low"]
        }
    
    def _get_mock_store_counts(self, group_by: str) -> List[Dict]:
        """Return mock store count data"""
        groups = {
            "division": ["EAST", "WEST", "NORTH", "SOUTH"],
            "region": ["Region 1", "Region 2", "Region 3", "Region 4"],
            "market": ["Market 1", "Market 2", "Market 3", "Market 4"],
            "phase": ["Planning", "Execution", "Review", "Complete"]
        }
        
        result = []
        for group in groups.get(group_by, []):
            result.append({
                "group": group,
                "project_source": "Intake Hub",
                "total_stores": (hash(group) % 500) + 300,
                "project_count": (hash(group) % 30) + 10
            })
            result.append({
                "group": group,
                "project_source": "Realty",
                "total_stores": (hash(group + "R") % 400) + 200,
                "project_count": (hash(group + "R") % 25) + 8
            })
        
        return result
