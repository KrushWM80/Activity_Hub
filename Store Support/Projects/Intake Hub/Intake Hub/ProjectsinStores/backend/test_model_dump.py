import sys
sys.path.insert(0, '/c/Users/krush/Documents/VSCode/Intake Hub/ProjectsinStores/backend')

from main import FilterOptionsResponse
from sqlite_cache import get_cache

cache = get_cache()
filters = cache.get_filter_options()

# Create response object exactly like the endpoint does
response_obj = FilterOptionsResponse(
    tribes=[],
    stores=filters.get('stores', []),
    project_sources=filters.get('project_sources', []),
    markets=filters.get('markets', []),
    regions=filters.get('regions', []),
    divisions=filters.get('divisions', []),
    phases=filters.get('phases', []),
    wm_weeks=filters.get('wm_weeks', []),
    fiscal_years=filters.get('fiscal_years', []),
    owners=filters.get('owners', []),
    store_areas=filters.get('store_areas', []),
    business_areas=filters.get('business_areas', []),
    health_statuses=filters.get('health_statuses', []),
    business_types=filters.get('business_types', []),
    associate_impacts=filters.get('associate_impacts', []),
    customer_impacts=filters.get('customer_impacts', [])
)

print(f"Model dump fields: {list(response_obj.model_dump().keys())}")
print(f"Model dump json: {len(response_obj.model_dump_json())} bytes")
print(f"First 300 chars: {response_obj.model_dump_json()[:300]}")
