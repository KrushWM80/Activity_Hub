"""Debug: check what keys the direct BQ query returns"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from send_vet_report_final import _fetch_from_bigquery_direct

data = _fetch_from_bigquery_direct()
if data:
    print(f"Total rows: {len(data)}")
    print(f"Keys: {list(data[0].keys())}")
    for row in data[:5]:
        title = str(row.get('Initiative - Project Title', '?'))[:40]
        phase = str(row.get('Phase', ''))
        fac = str(row.get('Facility Phase', 'MISSING'))
        sd = str(row.get('Start Date', ''))
        print(f"  {title:40s}  Phase={phase:15s}  FacPhase={fac:15s}  SD={sd}")
else:
    print("No data returned")
