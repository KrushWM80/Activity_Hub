#!/usr/bin/env python3
"""
Database helpers for Activity Hub hierarchy lookups
Query director/sr_director/vp information from AH_Hierarchy table
"""

from google.cloud import bigquery
import logging

logger = logging.getLogger(__name__)

client = bigquery.Client(project='wmt-assetprotection-prod')

BQ_PROJECT = 'wmt-assetprotection-prod'
BQ_DATASET = 'Store_Support_Dev'


def get_hierarchy_for_person(person_name: str) -> dict:
    """
    Get hierarchy information for a person
    Returns dict with director, sr_director, vp fields
    """
    if not person_name or person_name.strip() == '':
        return {'director': None, 'sr_director': None, 'vp': None}
    
    query = f"""
    SELECT person_name, director, sr_director, vp
    FROM `{BQ_PROJECT}.{BQ_DATASET}.AH_Hierarchy`
    WHERE LOWER(TRIM(person_name)) = LOWER(TRIM(@person_name))
    LIMIT 1
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("person_name", "STRING", person_name)
        ]
    )
    
    try:
        results = list(client.query(query, job_config=job_config).result())
        if results:
            row = results[0]
            return {
                'person_name': row.person_name,
                'director': row.director,
                'sr_director': row.sr_director,
                'vp': row.vp,
                'source': 'hierarchy'
            }
        return {'director': None, 'sr_director': None, 'vp': None, 'source': None}
    except Exception as e:
        logger.error(f"Error getting hierarchy for {person_name}: {e}")
        return {'director': None, 'sr_director': None, 'vp': None}


def get_director_projects(director_name: str, include_not_updated: bool = False) -> list:
    """
    Get projects where someone is the director
    Returns list of projects from AH_Projects table
    """
    if not director_name or director_name.strip() == '':
        return []
    
    # Build status filter
    status_filter = ""
    if not include_not_updated:
        status_filter = "AND ap.status != 'Not Updated'"
    
    query = f"""
    SELECT 
        ap.project_id,
        ap.title,
        ap.owner,
        ap.health,
        ap.status,
        ap.business_organization,
        ap.director_id,
        ap.sr_director_id,
        ap.project_update_date,
        ap.project_source
    FROM `{BQ_PROJECT}.{BQ_DATASET}.AH_Projects` ap
    WHERE (ap.director_id = @director_name OR ap.sr_director_id = @director_name)
      {status_filter}
    ORDER BY ap.project_update_date DESC
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("director_name", "STRING", director_name)
        ]
    )
    
    try:
        results = list(client.query(query, job_config=job_config).result())
        return [dict(row) for row in results]
    except Exception as e:
        logger.error(f"Error getting director projects for {director_name}: {e}")
        return []


def get_director_projects_by_name(director_name: str, include_not_updated: bool = False) -> list:
    """
    Get projects where someone is director by matching AH_Hierarchy
    This is a name-based lookup vs ID-based lookup
    Returns list of projects
    """
    if not director_name or director_name.strip() == '':
        return []
    
    # First get all people this person is the director for
    status_filter = ""
    if not include_not_updated:
        status_filter = "AND ap.status != 'Not Updated'"
    
    query = f"""
    SELECT DISTINCT
        ap.project_id,
        ap.title,
        ap.owner,
        ap.health,
        ap.status,
        ap.business_organization,
        ap.director_id,
        ap.sr_director_id,
        ap.project_update_date,
        ap.project_source
    FROM `{BQ_PROJECT}.{BQ_DATASET}.AH_Projects` ap
    INNER JOIN `{BQ_PROJECT}.{BQ_DATASET}.AH_Hierarchy` h
        ON (ap.owner = h.person_name OR ap.director_id = h.person_name)
        AND (h.director = @director_name OR h.sr_director = @director_name)
    WHERE True
      {status_filter}
    
    UNION DISTINCT
    
    -- Also get projects directly assigned to this person
    SELECT DISTINCT
        ap.project_id,
        ap.title,
        ap.owner,
        ap.health,
        ap.status,
        ap.business_organization,
        ap.director_id,
        ap.sr_director_id,
        ap.project_update_date,
        ap.project_source
    FROM `{BQ_PROJECT}.{BQ_DATASET}.AH_Projects` ap
    WHERE (LOWER(TRIM(ap.director_id)) = LOWER(TRIM(@director_name))
        OR LOWER(TRIM(ap.sr_director_id)) = LOWER(TRIM(@director_name)))
      {status_filter}
    
    ORDER BY project_update_date DESC
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("director_name", "STRING", director_name)
        ]
    )
    
    try:
        results = list(client.query(query, job_config=job_config).result())
        return [dict(row) for row in results]
    except Exception as e:
        logger.error(f"Error getting director projects by name for {director_name}: {e}")
        return []


def get_all_unique_people() -> list:
    """Get list of all unique people from hierarchy for dropdown selectors"""
    query = f"""
    SELECT DISTINCT person_name
    FROM `{BQ_PROJECT}.{BQ_DATASET}.AH_Hierarchy`
    WHERE person_name IS NOT NULL AND person_name != 'Unknown' AND TRIM(person_name) != ''
    ORDER BY person_name ASC
    """
    
    try:
        results = list(client.query(query).result())
        return [row.person_name for row in results]
    except Exception as e:
        logger.error(f"Error getting all unique people: {e}")
        return []
