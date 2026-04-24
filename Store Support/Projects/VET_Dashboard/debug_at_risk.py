"""Debug: verify at-risk items in phase tables"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from send_vet_report_final import _fetch_from_bigquery_direct, _build_stats

data = _fetch_from_bigquery_direct()
stats = _build_stats(data)
print("Total rows:", len(data))
print("Unique projects:", stats["total_projects"])
print("On Track:", stats["on_track"], "At Risk:", stats["at_risk"], "Off Track:", stats["off_track"])

at_risk = [p for p in data if "At Risk" in str(p.get("Health Status", ""))]
print("At Risk rows:", len(at_risk))

seen = set()
for p in at_risk:
    key = p.get("Project ID", p.get("Initiative - Project Title", ""))
    if key not in seen:
        seen.add(key)
        title = p.get("Initiative - Project Title", "")
        phase = p.get("Phase", "")
        fp = p.get("Facility Phase", "")
        sd = p.get("Start Date", "")
        print(f"  [{phase}] {title}  FacPhase={fp}  StartDate={sd}")
print("Unique at-risk projects:", len(seen))

phases = {}
for p in data:
    ph = p.get("Phase", "")
    phases[ph] = phases.get(ph, 0) + 1
print("Rows by Phase:", phases)
