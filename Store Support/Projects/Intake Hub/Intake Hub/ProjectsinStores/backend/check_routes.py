import sys
sys.path.insert(0, '.')

import main

print("Registered filter endpoints:")
for route in main.app.routes:
    if 'filter' in route.path.lower():
        print(f"  Path: {route.path}")
        print(f"  Methods: {route.methods if hasattr(route, 'methods') else 'N/A'}")
        print()
