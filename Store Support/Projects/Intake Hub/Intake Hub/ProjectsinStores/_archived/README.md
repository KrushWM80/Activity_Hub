# Archived Files

This folder contains previous versions and experiments that have been replaced by the current solution.

## code_puppy/

**Status:** Archived (Not Currently Used)

The Code Puppy branded dashboard version. This was an experiment with Walmart branding and a different UI approach.

### Why It's Archived

- Replaced by the original `simple.html` dashboard which better matches the user's original design
- The hierarchical Division → Region → Market → Store navigation in `simple.html` is more intuitive
- `simple.html` has cleaner filtering and better performance

### If You Need to Go Back

1. The file is preserved at `_archived/code_puppy/code_puppy_standalone.html`
2. Update `backend/main.py` line 87 to serve this version:
   ```python
   html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "_archived", "code_puppy", "code_puppy_standalone.html")
   ```
3. Restart the backend server

### Current Active Dashboard

The active dashboard is now:
- **File:** `frontend/simple.html`
- **Features:** Hierarchical filtering, Sparky AI, multi-select filters
- **Served by:** Backend at http://10.97.105.88:8001
