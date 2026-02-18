#!/usr/bin/env python3
"""
Dashboard using only built-in Python libraries
No external dependencies required - works with standard Python installation.

Usage:
    python dashboard_builtin.py
    Then visit: http://localhost:5000
"""

import http.server
import socketserver
import json
from pathlib import Path
import sys
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from email_history_logger import EmailHistoryLogger


PORT = 5000
logger = EmailHistoryLogger()


class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler for dashboard"""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)
        
        # API endpoints
        if path == '/api/metrics/total':
            self.send_json_response(self.get_total_metrics())
        elif path == '/api/metrics/by-role':
            self.send_json_response(self.get_changes_by_role())
        elif path == '/api/metrics/by-dc':
            self.send_json_response(self.get_changes_by_dc())
        elif path == '/api/metrics/daily-trend':
            days = int(query_params.get('days', [30])[0])
            self.send_json_response(self.get_daily_trend(days))
        elif path == '/api/health':
            self.send_json_response({'status': 'ok'})
        elif path == '/' or path == '/dashboard' or path == '/index.html':
            self.send_html_response(self.get_dashboard_html())
        else:
            self.send_error(404, 'Not Found')
    
    def send_json_response(self, data):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def send_html_response(self, html):
        """Send HTML response"""
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def log_message(self, format, *args):
        """Override to add timestamps"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {format % args}")
    
    def get_total_metrics(self):
        """Get total metrics"""
        total_changes = logger.get_total_changes_detected(days=30)
        total_emails = logger.get_total_emails_sent(days=30)
        dc_data = logger.get_changes_by_dc(days=30)
        unique_dcs = len(dc_data)
        
        return {
            'total_changes': total_changes,
            'total_emails': total_emails,
            'unique_dcs': unique_dcs,
            'last_updated': datetime.now().isoformat()
        }
    
    def get_changes_by_role(self):
        """Get changes by role type"""
        roles = logger.get_changes_by_role_type(days=30)
        
        return {
            'labels': list(roles.keys()),
            'data': list(roles.values())
        }
    
    def get_changes_by_dc(self):
        """Get changes by DC territory"""
        dc_data = logger.get_changes_by_dc(days=30)
        
        data = []
        for record in sorted(dc_data, key=lambda x: x.get('total_changes', 0), reverse=True):
            data.append({
                'dc': f"DC {record.get('dc_number', 'N/A')}",
                'changes': record.get('total_changes', 0),
                'emails': record.get('email_count', 0),
                'type': record.get('dc_type', 'Unknown')
            })
        
        return {'dcs': data}
    
    def get_daily_trend(self, days=30):
        """Get daily trend data"""
        daily = logger.get_daily_trend(days)
        
        labels = []
        data = []
        
        for record in daily:
            date_str = record['date']
            changes = record['total_changes']
            labels.append(date_str[-5:])  # MM-DD format
            data.append(changes)
        
        return {
            'labels': labels,
            'data': data
        }
    
    def get_dashboard_html(self):
        """Return dashboard HTML"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DC Manager Changes Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #f5f5f5 0%, #e9e9e9 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        header {
            background: linear-gradient(135deg, #008a00 0%, #0071ce 100%);
            color: white;
            padding: 30px 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        header h1 {
            font-size: 28px;
            margin-bottom: 5px;
        }
        
        header p {
            font-size: 14px;
            opacity: 0.9;
        }
        
        .time-filter {
            margin: 20px 0;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .time-filter button {
            padding: 8px 16px;
            border: 2px solid #ddd;
            background: white;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s;
        }
        
        .time-filter button.active {
            background: #008a00;
            color: white;
            border-color: #008a00;
        }
        
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .kpi-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-left: 5px solid #008a00;
        }
        
        .kpi-card i {
            color: #008a00;
            font-size: 24px;
            margin-bottom: 10px;
        }
        
        .kpi-label {
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 5px;
        }
        
        .kpi-value {
            font-size: 32px;
            font-weight: bold;
            color: #333;
        }
        
        .chart-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .chart-container {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .chart-title {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 15px;
            color: #333;
        }
        
        .full-width {
            grid-column: 1 / -1;
        }
        
        .table-container {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            overflow-x: auto;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
        }
        
        th {
            background: #f5f5f5;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: #333;
            border-bottom: 2px solid #ddd;
        }
        
        td {
            padding: 12px;
            border-bottom: 1px solid #eee;
        }
        
        tr:hover {
            background: #f9f9f9;
        }
        
        .dc-badge {
            display: inline-block;
            background: #008a00;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
        }
        
        .type-ambient {
            background: #4CAF50;
            padding: 4px 8px;
            border-radius: 4px;
            color: white;
            font-size: 11px;
        }
        
        .type-perishable {
            background: #2196F3;
            padding: 4px 8px;
            border-radius: 4px;
            color: white;
            font-size: 11px;
        }
        
        .refresh-indicator {
            text-align: center;
            color: #999;
            font-size: 12px;
            margin-top: 20px;
        }
        
        @media (max-width: 768px) {
            .chart-grid {
                grid-template-columns: 1fr;
            }
            
            .kpi-grid {
                grid-template-columns: 1fr;
            }
            
            header h1 {
                font-size: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1><i class="fas fa-chart-bar"></i> DC Manager Changes Dashboard</h1>
            <p>Real-time tracking of manager changes across distribution centers</p>
        </header>
        
        <div class="time-filter">
            <button class="active" onclick="changePeriod(30)">Last 30 Days</button>
            <button onclick="changePeriod(60)">Last 60 Days</button>
            <button onclick="changePeriod(90)">Last 90 Days</button>
        </div>
        
        <div class="kpi-grid">
            <div class="kpi-card">
                <i class="fas fa-exchange"></i>
                <div class="kpi-label">Total Changes Detected</div>
                <div class="kpi-value" id="total-changes">-</div>
            </div>
            <div class="kpi-card">
                <i class="fas fa-envelope"></i>
                <div class="kpi-label">Emails Sent</div>
                <div class="kpi-value" id="total-emails">-</div>
            </div>
            <div class="kpi-card">
                <i class="fas fa-warehouse"></i>
                <div class="kpi-label">Distribution Centers</div>
                <div class="kpi-value" id="unique-dcs">-</div>
            </div>
        </div>
        
        <div class="chart-grid">
            <div class="chart-container">
                <div class="chart-title"><i class="fas fa-pie-chart"></i> Changes by Role Type</div>
                <canvas id="roleChart"></canvas>
            </div>
            <div class="chart-container">
                <div class="chart-title"><i class="fas fa-bar-chart"></i> Changes by DC Territory</div>
                <canvas id="dcChart"></canvas>
            </div>
        </div>
        
        <div class="chart-grid">
            <div class="chart-container full-width">
                <div class="chart-title"><i class="fas fa-line-chart"></i> Daily Trend</div>
                <canvas id="trendChart"></canvas>
            </div>
        </div>
        
        <div class="table-container">
            <div class="chart-title"><i class="fas fa-table"></i> DC Territory Summary</div>
            <table>
                <thead>
                    <tr>
                        <th>DC Territory</th>
                        <th>Type</th>
                        <th>Total Changes</th>
                        <th>Emails Sent</th>
                    </tr>
                </thead>
                <tbody id="dc-table">
                    <tr>
                        <td colspan="4" style="text-align: center; color: #999;">Loading...</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <div class="refresh-indicator">
            Dashboard auto-refreshes every 5 minutes | Last updated: <span id="updated">-</span>
        </div>
    </div>
    
    <script>
        let currentPeriod = 30;
        let roleChart = null;
        let dcChart = null;
        let trendChart = null;
        
        function changePeriod(days) {
            currentPeriod = days;
            document.querySelectorAll('.time-filter button').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            refreshData();
        }
        
        async function fetchData(endpoint) {
            try {
                let url = endpoint;
                if (endpoint.includes('trend')) {
                    url += '?days=' + currentPeriod;
                }
                const response = await fetch(url);
                if (!response.ok) throw new Error('Network response was not ok');
                return await response.json();
            } catch (error) {
                console.error('Error fetching data:', error);
                return null;
            }
        }
        
        async function refreshData() {
            // Fetch all data
            const total = await fetchData('/api/metrics/total');
            const roleData = await fetchData('/api/metrics/by-role');
            const dcData = await fetchData('/api/metrics/by-dc');
            const trend = await fetchData('/api/metrics/daily-trend');
            
            // Update KPI cards
            if (total) {
                document.getElementById('total-changes').textContent = total.total_changes.toLocaleString();
                document.getElementById('total-emails').textContent = total.total_emails.toLocaleString();
                document.getElementById('unique-dcs').textContent = total.unique_dcs.toLocaleString();
                document.getElementById('updated').textContent = new Date(total.last_updated).toLocaleTimeString();
            }
            
            // Update charts
            if (roleData) updateRoleChart(roleData);
            if (dcData) updateDCChart(dcData);
            if (trend) updateTrendChart(trend);
            if (dcData) updateDCTable(dcData);
        }
        
        function updateRoleChart(data) {
            const ctx = document.getElementById('roleChart').getContext('2d');
            if (roleChart) roleChart.destroy();
            
            roleChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.data,
                        backgroundColor: ['#008a00', '#0071ce', '#FFC107'],
                        borderColor: '#fff',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        }
        
        function updateDCChart(data) {
            const ctx = document.getElementById('dcChart').getContext('2d');
            if (dcChart) dcChart.destroy();
            
            const dcs = data.dcs.slice(0, 10);
            dcChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: dcs.map(d => d.dc),
                    datasets: [{
                        label: 'Changes',
                        data: dcs.map(d => d.changes),
                        backgroundColor: '#008a00',
                        borderColor: '#006a00',
                        borderWidth: 1
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        x: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
        
        function updateTrendChart(data) {
            const ctx = document.getElementById('trendChart').getContext('2d');
            if (trendChart) trendChart.destroy();
            
            trendChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Daily Changes',
                        data: data.data,
                        borderColor: '#008a00',
                        backgroundColor: 'rgba(0, 138, 0, 0.1)',
                        borderWidth: 2,
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: true
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
        
        function updateDCTable(data) {
            const tbody = document.getElementById('dc-table');
            tbody.innerHTML = data.dcs.map(dc => `
                <tr>
                    <td><span class="dc-badge">${dc.dc}</span></td>
                    <td><span class="type-${dc.type.toLowerCase()}">${dc.type}</span></td>
                    <td>${dc.changes.toLocaleString()}</td>
                    <td>${dc.emails.toLocaleString()}</td>
                </tr>
            `).join('');
        }
        
        // Initial load and auto-refresh
        refreshData();
        setInterval(refreshData, 5 * 60 * 1000); // Refresh every 5 minutes
    </script>
</body>
</html>"""


def main():
    """Start the dashboard server"""
    Handler = DashboardHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("\n" + "="*70)
        print("🚀 DASHBOARD STARTED")
        print("="*70)
        print(f"\n📊 Open your browser: http://localhost:{PORT}")
        print(f"\n✓ Dashboard API running")
        print(f"✓ Test data loaded and ready")
        print(f"✓ Charts and metrics available")
        print("\nPress Ctrl+C to stop\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n" + "="*70)
            print("Dashboard stopped")
            print("="*70 + "\n")


if __name__ == "__main__":
    main()
