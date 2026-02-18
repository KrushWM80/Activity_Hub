# Store Location Data Integration

## Current Status
The dashboard currently uses store data from `IH_Intake_Data` table, which may not include latitude/longitude coordinates.

## Store Location Reference
Full store location data with coordinates is available in:
- **Table**: `wmt-assetprotection-prod.Store_Support_Dev.Store_Cur_Data`
- **Contains**: Latitude, Longitude, Store Address, City, State, Zip

## Implementation Plan

### Backend Changes Needed

1. **Update database.py** to join with Store_Cur_Data:
```python
query = f"""
    SELECT 
        CAST(ih.Intake_Card AS STRING) as project_id,
        ih.Project_Source as project_source,
        ih.Title as title,
        ih.Division as division,
        ih.Region as region,
        ih.Market as market,
        CAST(ih.Facility AS STRING) as store,
        ih.Store_Area as store_area,
        ih.Business_Area as business_area,
        ih.Phase as phase,
        '' as tribe,
        CAST(ih.WM_Week AS STRING) as wm_week,
        ih.Status as status,
        1 as store_count,
        ih.CREATED_TS as created_date,
        ih.Last_Updated as last_updated,
        ih.OVERVIEW as description,
        sc.latitude,
        sc.longitude,
        sc.store_address,
        sc.city,
        sc.state,
        sc.zip_code
    FROM `{self.project_id}.{self.dataset}.{self.table}` ih
    LEFT JOIN `{self.project_id}.{self.dataset}.Store_Cur_Data` sc
        ON CAST(ih.Facility AS STRING) = CAST(sc.store_number AS STRING)
    WHERE {where_clause}
    ORDER BY ih.Last_Updated DESC
    LIMIT 1000
"""
```

2. **Update models.py** to include location fields:
```python
class Project(BaseModel):
    # ... existing fields ...
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    store_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
```

### Frontend Changes Needed

Once backend provides lat/long data, add:

1. **Heat Map Component** using MapLibre GL:
```javascript
function createHeatMap(projects) {
    const map = new maplibregl.Map({
        container: 'map',
        style: 'https://demotiles.maplibre.org/style.json',
        center: [-95.7129, 37.0902], // Center of US
        zoom: 4
    });
    
    projects.forEach(p => {
        if (p.latitude && p.longitude) {
            new maplibregl.Marker()
                .setLngLat([p.longitude, p.latitude])
                .setPopup(new maplibregl.Popup().setHTML(
                    `<h3>${p.title}</h3>
                     <p>Store: ${p.store}</p>
                     <p>Division: ${p.division}</p>`
                ))
                .addTo(map);
        }
    });
}
```

2. **Add Heat Map Container** in HTML:
```html
<div class="map-container" style="height: 500px; margin-bottom: 20px;">
    <h2>🗺️ Store Heat Map</h2>
    <div id="map" style="height: 450px; border-radius: 8px;"></div>
</div>
```

## Next Steps

1. Verify Store_Cur_Data table schema:
   ```sql
   SELECT * FROM `wmt-assetprotection-prod.Store_Support_Dev.Store_Cur_Data` LIMIT 1
   ```

2. Confirm the join key (store number field name in both tables)

3. Update backend query with LEFT JOIN

4. Test with sample data

5. Add heat map visualization to frontend

## Benefits

- Visual representation of project distribution
- Geographic filtering capabilities
- Store clustering analysis
- Regional impact visualization
- Better insights for stakeholders
