#!/usr/bin/env python3
"""
TDA Insights Dashboard Backend - Pure Socket Version
Uses only Python standard library, minimal dependencies
"""

import socket
import json
import threading
import time
from pathlib import Path

PORT = 5000
SCRIPT_DIR = Path(__file__).parent

# Sample data (replace with BigQuery data if available)
SAMPLE_DATA = [
    {
        "Initiative - Project Title": "Sidekick Enhancement",
        "Health Status": "On Track",
        "Phase": "Test",
        "# of Stores": 120,
        "Intake & Testing": "System testing in progress. All core features validated. Ready for POC expansion.",
        "Dallas POC": "John Smith - Store #4521, TX",
        "Deployment": "Scheduled for 3/15/2026. Training materials prepared. Rollout plan finalized."
    },
    {
        "Initiative - Project Title": "GMD Optimization",
        "Health Status": "At Risk",
        "Phase": "POC/POT",
        "# of Stores": 95,
        "Intake & Testing": "POC execution with pilot stores. Initial results show 15% efficiency gains.",
        "Dallas POC": "Jane Doe - Store #2847, TX",
        "Deployment": "Delayed. Addressing performance issues discovered in POC phase. New target: 4/1/2026"
    },
    {
        "Initiative - Project Title": "DSD Redesign",
        "Health Status": "On Track",
        "Phase": "Roll/Deploy",
        "# of Stores": 250,
        "Intake & Testing": "All validation complete. Rollout in waves starting Week 3.",
        "Dallas POC": "Bob Wilson - Store #1234, TX",
        "Deployment": "Live in 250 stores as of 2/28/2026. Phase 2 rollout beginning next week."
    },
    {
        "Initiative - Project Title": "Fresh Department Update",
        "Health Status": "Off Track",
        "Phase": "Pending",
        "# of Stores": 180,
        "Intake & Testing": "Initial requirements gathering delayed. No testing scheduled yet.",
        "Dallas POC": "Alice Johnson - Pending Assignment",
        "Deployment": "Blocked. Awaiting stakeholder sign-off on requirements."
    },
    {
        "Initiative - Project Title": "Inventory System Migration",
        "Health Status": "On Track",
        "Phase": "Mkt Scale",
        "# of Stores": 15,
        "Intake & Testing": "Market testing complete. System scaling for regional rollout.",
        "Dallas POC": "Tom Brown - Store #5678, TX",
        "Deployment": "Regional deployment Q2 2026. Infrastructure scaled for 500+ stores."
    },
]

def filter_data(phase=None, health_status=None):
    """Filter sample data by phase and health status"""
    data = SAMPLE_DATA
    if phase and phase != "All":
        data = [r for r in data if r.get("Phase") == phase]
    if health_status and health_status != "All":
        data = [r for r in data if r.get("Health Status") == health_status]
    return data

def handle_request(client_socket, addr):
    """Handle a single HTTP request"""
    try:
        # Receive request
        request_data = client_socket.recv(4096).decode('utf-8', errors='ignore')
        request_lines = request_data.split('\r\n')
        request_line = request_lines[0] if request_lines else ""
        
        # Parse request
        parts = request_line.split()
        if len(parts) < 2:
            return
        
        method = parts[0]
        path = parts[1].split('?')[0]  # Remove query string
        
        print(f"[{time.strftime('%H:%M:%S')}] {method} {path}")
        
        # Handle routes
        if path == '/api/health':
            response_json = json.dumps({
                'status': 'healthy',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'server': 'TDA Insights Lightweight'
            })
            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(response_json)}\r\nConnection: close\r\n\r\n{response_json}"
            client_socket.sendall(response.encode())
        
        elif path == '/api/data':
            data = filter_data()
            response_json = json.dumps({
                'success': True,
                'count': len(data),
                'data': data
            })
            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(response_json)}\r\nConnection: close\r\n\r\n{response_json}"
            client_socket.sendall(response.encode())
        
        elif path == '/api/phases':
            # Return phases in proper order
            phases = ['Pending', 'POC/POT', 'Test', 'Mkt Scale', 'Roll/Deploy']
            response_json = json.dumps({
                'success': True,
                'phases': phases
            })
            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(response_json)}\r\nConnection: close\r\n\r\n{response_json}"
            client_socket.sendall(response.encode())
        
        elif path == '/api/health-statuses':
            statuses = sorted(set(r.get("Health Status", "Unknown") for r in SAMPLE_DATA))
            response_json = json.dumps({
                'success': True,
                'health_statuses': statuses
            })
            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(response_json)}\r\nConnection: close\r\n\r\n{response_json}"
            client_socket.sendall(response.encode())
        
        elif path == '/api/summary':
            data = filter_data()
            summary = {
                'total_projects': len(data),
                'total_stores': sum(int(r.get('# of Stores', 0) or 0) for r in data),
                'by_health_status': {},
                'by_phase': {}
            }
            for r in data:
                status = r.get('Health Status', 'Unknown')
                summary['by_health_status'][status] = summary['by_health_status'].get(status, 0) + 1
                phase = r.get('Phase', 'Unknown')
                summary['by_phase'][phase] = summary['by_phase'].get(phase, 0) + 1
            
            response_json = json.dumps({'success': True, 'summary': summary})
            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(response_json)}\r\nConnection: close\r\n\r\n{response_json}"
            client_socket.sendall(response.encode())
        
        elif path == '/dashboard.html' or path == '/':
            html_file = SCRIPT_DIR / 'dashboard.html'
            if html_file.exists():
                try:
                    with open(html_file, 'r', encoding='utf-8') as f:
                        html = f.read()
                    html_bytes = html.encode('utf-8')
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(html_bytes)}\r\nConnection: close\r\n\r\n"
                    client_socket.sendall(response.encode('utf-8'))
                    client_socket.sendall(html_bytes)
                except Exception as e:
                    print(f"[ERROR] Failed to serve HTML: {e}")
                    error_response = f"HTTP/1.1 500 Server Error\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nFailed to load dashboard"
                    client_socket.sendall(error_response.encode())
            else:
                error = "Dashboard not found"
                response = f"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\n{error}"
                client_socket.sendall(response.encode())
        
        elif path == '/api/ppt/generate':
            # Simple PPT generation stub (no external dependencies)
            response_json = json.dumps({
                'success': True,
                'file_name': f'TDA_Report_{int(time.time())}.pptx',
                'message': 'PPT generation requires python-pptx. Install with: pip install python-pptx'
            })
            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(response_json)}\r\nConnection: close\r\n\r\n{response_json}"
            client_socket.sendall(response.encode())
        
        elif path == '/favicon.ico':
            response = "HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n"
            client_socket.sendall(response.encode())
        
        else:
            response_json = json.dumps({'error': 'Endpoint not found'})
            response = f"HTTP/1.1 404 Not Found\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(response_json)}\r\nConnection: close\r\n\r\n{response_json}"
            client_socket.sendall(response.encode())
    
    except Exception as e:
        print(f"[ERROR] Error handling request: {e}")
        try:
            error_response = "HTTP/1.1 500 Server Error\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nServer Error"
            client_socket.sendall(error_response.encode())
        except:
            pass
    
    finally:
        try:
            client_socket.close()
        except:
            pass

def start_server():
    """Start the HTTP server"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind(('127.0.0.1', PORT))
        server_socket.listen(5)
        
        print("\n" + "="*60)
        print("[OK] TDA Insights Dashboard - Lightweight Backend")
        print("="*60)
        print(f"[OK] Server listening on http://127.0.0.1:{PORT}")
        print(f"[OK] Dashboard: http://localhost:{PORT}/dashboard.html")
        print(f"[OK] API: http://localhost:{PORT}/api/data")
        print("="*60)
        print("Press Ctrl+C to stop\n")
        
        while True:
            try:
                client_socket, addr = server_socket.accept()
                thread = threading.Thread(target=handle_request, args=(client_socket, addr), daemon=True)
                thread.start()
            except KeyboardInterrupt:
                print("\n\nShutdown requested...")
                break
            except Exception as e:
                print(f"Error accepting connection: {e}")
    
    except OSError as e:
        print(f"[ERROR] Cannot bind to port {PORT}")
        print(f"  {e}")
        return False
    
    finally:
        server_socket.close()
        print("[OK] Server shut down\n")
    
    return True

if __name__ == '__main__':
    try:
        start_server()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
