# Quick Start - Local Hosting

Get your project running locally in 5 minutes.

---

## Step 1: Choose Your Method

**Do users access your project via web browser?**
- **YES** → Go to [Continuous Server Setup](#continuous-server-setup)
- **NO** (emails, reports, scheduled tasks) → Go to [Scheduled Automation Setup](#scheduled-automation-setup)

---

## Scheduled Automation Setup

For projects that run on a schedule and produce outputs (emails, files, etc.)

### Minimum Files Needed

```
your-project/
├── main_script.py          # Your automation code
├── setup_task.bat          # Creates scheduled task
└── requirements.txt        # Python packages
```

### Quick Setup

1. **Create your script** (`main_script.py`)
   ```python
   import logging
   from datetime import datetime
   
   logging.basicConfig(level=logging.INFO)
   
   def main():
       logging.info(f"Running at {datetime.now()}")
       # Your automation logic here
       logging.info("Complete!")
   
   if __name__ == "__main__":
       main()
   ```

2. **Create setup script** (`setup_task.bat`)
   ```batch
   @echo off
   schtasks /Create /TN "MyTask" /TR "cmd /c cd /d %CD% && python main_script.py" /SC HOURLY /ST 06:00 /F
   echo Task created!
   pause
   ```

3. **Run setup** (as Admin)
   ```cmd
   setup_task.bat
   ```

4. **Verify** - Open Task Scheduler, find "MyTask", right-click → Run

**📁 Full Template:** [Scheduled Automation System/README.md](./Scheduled%20Automation%20System/README.md)

---

## Continuous Server Setup

For dashboards and APIs that need to be always available.

### Minimum Files Needed

```
your-project/
├── backend/
│   ├── main.py             # FastAPI/Flask server
│   └── start_backend.bat   # Server startup
├── frontend/
│   └── index.html          # Web interface
└── create_startup_shortcut.ps1  # Auto-start
```

### Quick Setup

1. **Create your server** (`backend/main.py`)
   ```python
   from fastapi import FastAPI
   import uvicorn
   
   app = FastAPI()
   
   @app.get("/")
   async def root():
       return {"message": "Hello World"}
   
   if __name__ == "__main__":
       uvicorn.run(app, host="0.0.0.0", port=8001)
   ```

2. **Create start script** (`backend/start_backend.bat`)
   ```batch
   @echo off
   cd /d "%~dp0"
   python main.py
   ```

3. **Test manually**
   ```cmd
   cd backend
   python main.py
   ```
   Open: http://localhost:8001

4. **Set up auto-start** (no admin needed)
   ```powershell
   # create_startup_shortcut.ps1
   $WshShell = New-Object -ComObject WScript.Shell
   $Shortcut = $WshShell.CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\MyServer.lnk")
   $Shortcut.TargetPath = "$PSScriptRoot\backend\start_backend.bat"
   $Shortcut.Save()
   Write-Host "Done! Server will start on login."
   ```

**📁 Full Template:** [Continous Running Server/README.md](./Continous%20Running%20Server%20-%20HTTP%20Port/README.md)

---

## Common Tasks

### Install Python Dependencies
```cmd
pip install fastapi uvicorn requests pandas
```

### Check if Port is Available
```cmd
netstat -ano | findstr :8001
```

### Find Your IP Address (for sharing)
```cmd
ipconfig
```
Look for "IPv4 Address" under your active adapter.

### Allow Port Through Firewall
```cmd
netsh advfirewall firewall add rule name="My Server" dir=in action=allow protocol=TCP localport=8001
```

---

## Checklist

### Scheduled Automation
- [ ] Script runs successfully manually
- [ ] Task created in Task Scheduler
- [ ] Logs are being written
- [ ] Output is delivered (email/file)

### Continuous Server
- [ ] Server starts and listens on port
- [ ] http://localhost:PORT works
- [ ] Auto-start configured
- [ ] Team can access via IP/VPN

---

## Need More Help?

- **Detailed Decision Guide:** [DECISION_GUIDE.md](./DECISION_GUIDE.md)
- **Scheduled Automation Template:** [Scheduled Automation System/](./Scheduled%20Automation%20System/)
- **Continuous Server Template:** [Continous Running Server/](./Continous%20Running%20Server%20-%20HTTP%20Port/)
