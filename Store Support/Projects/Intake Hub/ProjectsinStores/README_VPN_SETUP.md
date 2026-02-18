# VPN Server Setup Instructions

## 🚀 Quick Start

### 1. Start the Backend Server

**Option A: Using PowerShell Script (Recommended)**
```powershell
cd "backend"
.\start_server.ps1
```

**Option B: Manual Start**
```powershell
cd "backend"
python main.py
```

The server will start on **port 8001** and be accessible to anyone on the VPN.

### 2. Get Your VPN IP Address

The startup script will display your IP addresses. Look for your VPN IP (usually something like `10.x.x.x` or `192.168.x.x`).

Example output:
```
📡 Network Information:
   Your IP Address(es):
   - 10.123.45.67  ← Your VPN IP
   - 192.168.1.100 ← Your local network IP
```

### 3. Configure the HTML File

Open `code_puppy_standalone.html` and update line ~776:

**Before:**
```javascript
const VPN_SERVER_URL = 'http://YOUR_VPN_IP:8001';  // ⬅️ REPLACE WITH YOUR VPN IP/HOSTNAME
```

**After:**
```javascript
const VPN_SERVER_URL = 'http://10.123.45.67:8001';  // ⬅️ Your actual VPN IP
```

### 4. Share Access with Team

Send your team:
1. **Your VPN IP address** (e.g., `10.123.45.67`)
2. **The updated `code_puppy_standalone.html` file**

Team members can:
- Open the HTML file directly in their browser (no server needed on their end)
- Access it via network share or email
- The HTML will automatically connect to your backend server

---

## 🔒 Security & Authentication

### BigQuery Authentication

The server needs Google Cloud credentials to access BigQuery. Choose one option:

**Option 1: Use Default Credentials (Recommended)**
```powershell
gcloud auth application-default login
```

**Option 2: Use Service Account**
1. Download service account JSON from Google Cloud Console
2. Set environment variable:
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\service-account-key.json"
```

### Firewall Configuration

Ensure port 8001 is allowed in Windows Firewall:

```powershell
# Add firewall rule (run as Administrator)
New-NetFirewallRule -DisplayName "FastAPI Backend" -Direction Inbound -LocalPort 8001 -Protocol TCP -Action Allow
```

---

## 📊 Usage Scenarios

### Scenario 1: Always-On Server
**Use Case:** Team needs 24/7 access to dashboard

**Setup:**
1. Run server on a dedicated VM or always-on machine
2. Configure server to start on boot:
   - Create scheduled task in Windows Task Scheduler
   - Set trigger: "At system startup"
   - Action: Start `start_server.ps1`

### Scenario 2: On-Demand Server
**Use Case:** Start server only when needed

**Setup:**
1. Start server manually: `.\start_server.ps1`
2. Share your current VPN IP with team
3. Stop server when done (Ctrl+C)

### Scenario 3: Development Server
**Use Case:** Testing changes locally

**Setup:**
1. Keep HTML file pointing to `localhost:8001`
2. No VPN access needed
3. Test changes before sharing with team

---

## 🛠️ Troubleshooting

### Server Won't Start

**Check Python packages:**
```powershell
pip install fastapi uvicorn google-cloud-bigquery python-dotenv openai
```

**Check port availability:**
```powershell
netstat -ano | findstr :8001
```

### Can't Connect from VPN

**Verify firewall:**
```powershell
Test-NetConnection -ComputerName YOUR_VPN_IP -Port 8001
```

**Check server is bound to 0.0.0.0:**
Look for this in `main.py`:
```python
uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
```

### BigQuery Connection Failed

**Authenticate:**
```powershell
gcloud auth application-default login
```

**Verify project ID:**
```powershell
gcloud config get-value project
```

---

## 📝 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GCP_PROJECT_ID` | `wmt-assetprotection-prod` | Google Cloud Project ID |
| `BIGQUERY_DATASET` | `Store_Support_Dev` | BigQuery dataset name |
| `BIGQUERY_TABLE` | `IH_Intake_Data` | BigQuery table name |
| `GOOGLE_APPLICATION_CREDENTIALS` | (optional) | Path to service account JSON |

---

## 🔄 Updating the Server

1. Stop the server (Ctrl+C)
2. Pull latest changes from Git
3. Restart the server (`.\start_server.ps1`)

Team members with the HTML file will automatically use the new backend without any changes.

---

## 📈 Monitoring

**View server logs:**
The console shows real-time requests:
```
INFO:     127.0.0.1:12345 - "GET /api/projects HTTP/1.1" 200 OK
INFO:     127.0.0.1:12346 - "POST /api/ai/query HTTP/1.1" 200 OK
```

**Check server health:**
Visit in browser: `http://YOUR_VPN_IP:8001/api/health`

---

## 💡 Tips

1. **Static IP:** Use a machine with a static VPN IP for consistency
2. **DNS Hostname:** If your machine has a VPN hostname (e.g., `myserver.walmart.net`), use that instead of IP
3. **Multiple Users:** The server can handle multiple concurrent users
4. **Auto-Reload:** The server automatically reloads when you edit backend code
5. **Logs:** Keep the PowerShell window open to monitor API calls

---

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review server logs in the PowerShell window
3. Verify VPN connectivity: `ping YOUR_VPN_IP`
4. Test locally first: `http://localhost:8001`
