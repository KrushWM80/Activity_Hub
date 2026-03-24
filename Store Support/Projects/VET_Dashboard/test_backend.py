"""
Minimal test backend to verify Flask is working
"""
from flask import Flask, jsonify
import logging

app = Flask(__name__, static_folder=".", static_url_path='')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    return "V.E.T. Dashboard Test - Backend Running!"

@app.route('/api/test')
def test():
    return jsonify({'status': 'ok', 'message': 'Backend is working'})

if __name__ == '__main__':
    port = 5001
    logger.info(f"Starting test backend on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
