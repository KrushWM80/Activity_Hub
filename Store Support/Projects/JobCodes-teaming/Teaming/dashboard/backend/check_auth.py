#!/usr/bin/env python3
"""Check what users and sessions exist"""

import json
import os

data_dir = 'data'

# Load users file
users_file = os.path.join(data_dir, 'users.json')
print("=" * 60)
print("USERS")
print("=" * 60)
if os.path.exists(users_file):
    with open(users_file) as f:
        users = json.load(f)
    print(f"Found {len(users)} users:")
    for username, user in users.items():
        print(f"  {username}:")
        print(f"    - role: {user.get('role')}")
        print(f"    - approved: {user.get('approved')}")
        print(f"    - name: {user.get('name')}")
else:
    print("Users file not found")

# Load sessions file
sessions_file = os.path.join(data_dir, 'sessions.json')
print("\n" + "=" * 60)
print("SESSIONS")
print("=" * 60)
if os.path.exists(sessions_file):
    with open(sessions_file) as f:
        sessions = json.load(f)
    print(f"Found {len(sessions)} sessions:")
    for idx, (sid, sess) in enumerate(list(sessions.items())[:3]):
        print(f"  {sid[:16]}...:")
        print(f"    - username: {sess.get('username')}")
        print(f"    - created: {sess.get('created')}")
else:
    print("Sessions file not found or empty")
