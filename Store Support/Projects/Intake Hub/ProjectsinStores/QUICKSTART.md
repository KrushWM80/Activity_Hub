# ⚡ 30-Second Quickstart

## Already have Python 3.10+? Let's go!

```powershell
# 1. Install (5 seconds)
cd "c:\Users\krush\Documents\VSCode\Intake Hub\ProjectsinStores\backend"
pip install fastapi uvicorn google-cloud-bigquery

# 2. Authenticate (10 seconds)
gcloud auth application-default login

# 3. Start (5 seconds)
cd ..
.\START_DASHBOARD.bat

# 4. Browser opens automatically to:
# http://localhost:8001/           (Main Dashboard)
# http://localhost:8001/admin.html (Admin Panel)
```

## 🎉 Done!

You now have:
- ✅ **196 active projects** from BigQuery
- ✅ **4,576 stores** with hierarchical navigation  
- ✅ **Sparky AI** for intelligent project search
- ✅ **Live filtering** and CSV export
- ✅ **Admin Panel** for fix management

## Available URLs

| URL | Purpose |
|-----|-------------|
| http://localhost:8001/ | Main Dashboard (Dev) |
| http://127.0.0.1:8001/ | Main Dashboard (Production/Live) |
| http://localhost:8001/admin.html | Admin Panel |
| http://localhost:8001/reports.html | Email Reports |
| http://localhost:8001/docs | API Documentation |

## ✨ That's It!

Your dashboard is now running with:
- ✅ Interactive filters
- ✅ Real-time charts
- ✅ AI assistant (with OpenAI key)
- ✅ Project table
- ✅ Summary statistics

## 🎯 Test the API

Run the test script to verify everything works:
```powershell
cd backend
python test_api.py
```

## 📖 Need More Help?

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions, troubleshooting, and Code Puppy Pages integration.

## 🔑 Configuration Details

### Database (Optional)
Add to `.env`:
```
GCP_PROJECT_ID=wmt-assetprotection-prod
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
```

### AI Assistant (Optional)
Add to `.env`:
```
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4
```

**Note:** Without these, the dashboard uses mock data and still works perfectly for testing and demos!
