"""Launcher for VET Dashboard backend - sets env vars and runs Flask with stdout logging."""
import os
import sys
import io

# Force UTF-8 output to prevent cp1252 encoding crashes with special characters
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Set credentials before any Google imports - use existing env var if set, otherwise use known path
_creds = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '')
if not _creds or not os.path.exists(_creds):
    _creds = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = _creds
os.environ['GOOGLE_CLOUD_PROJECT'] = 'wmt-assetprotection-prod'

# Now import and run backend
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend import app

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
