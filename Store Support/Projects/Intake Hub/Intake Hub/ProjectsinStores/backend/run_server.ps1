$env:ENVIRONMENT="prod"
cd "c:\Users\krush\Documents\VSCode\Intake Hub\ProjectsinStores\backend"
python -m uvicorn main:app --host 0.0.0.0 --port 8001
