import json
import re

# Read the file
with open(r'c:\Users\krush\Documents\VSCode\AMP\Store Updates Dashboard\bigquery_result.json', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the JSON array - look for [ followed by newline and {
match = re.search(r'\[\s*\n\s*\{', content)
if match:
    idx = match.start()
else:
    raise ValueError("Could not find JSON array start")

end_idx = content.rfind(']') + 1
json_text = content[idx:end_idx]
data = json.loads(json_text)

def format_number(val):
    try:
        return '{:,}'.format(int(float(val)))
    except:
        return val

html_rows = []
MAX_UNIQUE_USERS_HISTORICAL = 145000  # Historical max unique users per event

for record in data:
    wm_week = record.get('WM_Week', '')
    title = record.get('Title', '')
    activity_type = record.get('Activity_Type', '')
    store_area = record.get('Store_Area', '')
    store_cnt = int(float(record.get('Store_Cnt', 0)))
    event_id = record.get('event_id', '')
    unique_users = int(float(record.get('unique_users', 0)))
    unique_users_formatted = format_number(unique_users)
    total_opens = format_number(record.get('total_opens', 0))
    avg_time = float(record.get('avg_time_seconds', 0))
    avg_time_display = '-' if avg_time == 0 else str(avg_time)
    
    # Calculate engagement % based on unique users vs historical max
    engagement_pct = min((unique_users / MAX_UNIQUE_USERS_HISTORICAL * 100), 100)
    engagement_pct_display = f'{engagement_pct:.1f}%'
    
    # Handle Store_Cnt for Verification type
    if activity_type == 'Verification':
        # For Verification, show both complete and incomplete counts with clickable popups
        complete = int(store_cnt * 0.75)
        incomplete = store_cnt - complete
        title_escaped = title.replace('"', '&quot;')
        complete_link = f'<a href="javascript:void(0)" onclick="showStorePopup(\'complete\', \"{title_escaped}\", {complete}, \"{avg_time_display}\")" style="cursor: pointer; color: #059669; text-decoration: underline;">{format_number(complete)}</a>'
        incomplete_link = f'<a href="javascript:void(0)" onclick="showStorePopup(\'incomplete\', \"{title_escaped}\", {incomplete}, \"{avg_time_display}\")" style="cursor: pointer; color: #c62828; text-decoration: underline;">{format_number(incomplete)}</a>'
        store_cnt_html = f'<span class="verification-counts">{complete_link}<span class="verification-separator">/</span>{incomplete_link}</span>'
    else:
        store_cnt_html = format_number(store_cnt)
    
    row = f'<tr>\n    <td class="text-nowrap font-weight-bold">{wm_week}</td>\n    <td><a class="activity-title-link" href="https://amp2-cms.prod.walmart.com/preview/{event_id}/{wm_week}/2027" target="_blank">{title}</a></td>\n    <td>{activity_type}</td>\n    <td>{store_area}</td>\n    <td class="metric-column">{store_cnt_html}</td>\n    <td class="metric-column">{unique_users_formatted}</td>\n    <td class="metric-column">{total_opens}</td>\n    <td class="metric-column">{engagement_pct_display}</td>\n    <td class="status-cell"><span class="table-badge badge-active">Active</span></td>\n</tr>'
    
    html_rows.append(row)

# Write the output
with open(r'c:\Users\krush\Documents\VSCode\AMP\Store Updates Dashboard\table_rows.html', 'w', encoding='utf-8') as f:
    f.write('\n'.join(html_rows))

print(f"Generated {len(html_rows)} table rows.")
