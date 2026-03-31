from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = FastAPI(title="Digital Egg Hunt API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
DATA_FILE = Path(__file__).parent.parent / "data" / "egg_hunt_data.json"
CUTOFF_TIME = datetime(2026, 4, 3, 9, 30, 0, tzinfo=timezone.utc)  # 9:30 AM EDT
TOTAL_EGGS = 50

# Pydantic models
class ScanRequest(BaseModel):
    user_name: str
    egg_id: str

class RegisterRequest(BaseModel):
    first_name: str
    last_name: str

class UserData(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    eggs_found: list
    registration_time: str
    last_scan_time: str

# Initialize data file if it doesn't exist
def initialize_data():
    if not DATA_FILE.exists():
        data = {
            "users": {},
            "winner": None,
            "winner_announcement_time": None,
            "game_status": "active",
            "email_recipients": ["kendall.rush@walmart.com"]
        }
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)

# Load data
def load_data():
    initialize_data()
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Save data
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Generate unique user ID
def generate_user_id(first_name, last_name):
    return f"{first_name.lower()}_{last_name.lower()}_{int(datetime.now().timestamp())}"

# Check if game cutoff has been reached
def is_cutoff_reached():
    return datetime.now(timezone.utc) >= CUTOFF_TIME

# Detect winner
def detect_winner(data):
    if data.get("winner"):
        return None  # Winner already declared
    
    for user_id, user in data["users"].items():
        if len(user["eggs_found"]) == TOTAL_EGGS:
            return user_id
    
    return None

# Send email to configured recipients
def send_winner_email(winner_name, recipients=None):
    """Send winner notification to configured recipients (default: Kendall only)"""
    try:
        # Using Office 365 SMTP
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()
        
        # Note: You'll need to set environment variables for credentials
        sender_email = os.getenv('SENDER_EMAIL', 'activity_team@walmart.com')
        sender_password = os.getenv('SENDER_PASSWORD')
        
        # Use provided recipients or default
        if recipients is None:
            recipients = ["kendall.rush@walmart.com"]
        
        if not sender_password:
            print(f"Warning: SENDER_PASSWORD not set. Would send to {', '.join(recipients)}")
            return True
        
        server.login(sender_email, sender_password)
        
        subject = f"🥚 Digital Egg Hunt Winner - {winner_name}! 🥚"
        body = f"""
Congratulations!

{winner_name} has won the Digital Egg Hunt by finding all 50 eggs!

Please come by the Activity Team to collect your prize!

---
Digital Egg Hunt System
"""
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server.send_message(msg)
        server.quit()
        print(f"Email sent to {', '.join(recipients)} about {winner_name}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# API Endpoints

@app.post("/register")
def register_user(request: RegisterRequest):
    """Register a new participantUser"""
    data = load_data()
    
    if is_cutoff_reached():
        raise HTTPException(status_code=400, detail="Game has ended")
    
    user_id = generate_user_id(request.first_name, request.last_name)
    
    # Check if user already registered
    for existing_id, user in data["users"].items():
        if (user["first_name"].lower() == request.first_name.lower() and 
            user["last_name"].lower() == request.last_name.lower()):
            return {
                "user_id": existing_id,
                "message": "User already registered",
                "status": "existing"
            }
    
    now = datetime.now(timezone.utc).isoformat()
    data["users"][user_id] = {
        "first_name": request.first_name,
        "last_name": request.last_name,
        "eggs_found": [],
        "registration_time": now,
        "last_scan_time": now
    }
    
    save_data(data)
    
    return {
        "user_id": user_id,
        "message": "User registered successfully",
        "status": "new"
    }

@app.post("/scan")
def scan_egg(request: ScanRequest):
    """Record an egg scan"""
    data = load_data()
    
    if is_cutoff_reached() and not data.get("winner"):
        # Determine winner at cutoff
        determine_final_winner(data)
        save_data(data)
        raise HTTPException(status_code=400, detail="Game has ended - winner determined")
    
    if data.get("winner"):
        raise HTTPException(status_code=400, detail="Game has ended - winner already declared")
    
    # Find user by name (case-insensitive)
    user_id = None
    for uid, user in data["users"].items():
        if (user["first_name"].lower() == request.user_name.split()[0].lower() and
            len(request.user_name.split()) > 1 and
            user["last_name"].lower() == request.user_name.split()[1].lower()):
            user_id = uid
            break
    
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Validate egg ID
    if not request.egg_id.upper().startswith(('EGG-', 'T')):
        raise HTTPException(status_code=400, detail="Invalid egg ID format")
    
    egg_id_upper = request.egg_id.upper()
    
    # Check if already found
    if egg_id_upper in data["users"][user_id]["eggs_found"]:
        return {
            "status": "already_found",
            "egg_id": egg_id_upper,
            "eggs_count": len(data["users"][user_id]["eggs_found"])
        }
    
    # Add egg to found list
    data["users"][user_id]["eggs_found"].append(egg_id_upper)
    data["users"][user_id]["last_scan_time"] = datetime.now(timezone.utc).isoformat()
    
    eggs_found = len(data["users"][user_id]["eggs_found"])
    response = {
        "status": "success",
        "egg_id": egg_id_upper,
        "eggs_count": eggs_found,
        "eggs_remaining": TOTAL_EGGS - eggs_found
    }
    
    # Check for winner
    if eggs_found == TOTAL_EGGS:
        winner_id = user_id
        data["winner"] = {
            "user_id": winner_id,
            "first_name": data["users"][winner_id]["first_name"],
            "last_name": data["users"][winner_id]["last_name"],
            "eggs_found": TOTAL_EGGS,
            "win_time": datetime.now(timezone.utc).isoformat()
        }
        data["winner_announcement_time"] = datetime.now(timezone.utc).isoformat()
        
        # Send email to configured recipients
        winner_name = f"{data['winner']['first_name']} {data['winner']['last_name']}"
        recipients = data.get("email_recipients", ["kendall.rush@walmart.com"])
        send_winner_email(winner_name, recipients)
        
        response["winner"] = True
        response["message"] = f"Congratulations! {winner_name} won the Digital Egg Hunt!"
    
    save_data(data)
    return response

@app.get("/leaderboard")
def get_leaderboard():
    """Get current leaderboard"""
    data = load_data()
    
    # Sort users by eggs found (descending), then by registration time
    sorted_users = sorted(
        data["users"].items(),
        key=lambda x: (-len(x[1]["eggs_found"]), x[1]["registration_time"])
    )
    
    leaderboard = []
    for rank, (user_id, user) in enumerate(sorted_users, 1):
        leaderboard.append({
            "rank": rank,
            "name": f"{user['first_name']} {user['last_name']}",
            "eggs_found": len(user["eggs_found"]),
            "eggs_remaining": TOTAL_EGGS - len(user["eggs_found"]),
            "registration_time": user["registration_time"],
            "last_scan_time": user["last_scan_time"]
        })
    
    return {
        "leaderboard": leaderboard,
        "total_participants": len(data["users"]),
        "total_eggs": TOTAL_EGGS,
        "winner": data.get("winner"),
        "cutoff_time": CUTOFF_TIME.isoformat(),
        "game_status": data["game_status"]
    }

@app.get("/status")
def get_game_status():
    """Get game status and countdown"""
    data = load_data()
    now = datetime.now(timezone.utc)
    
    time_remaining = CUTOFF_TIME - now
    time_remaining_seconds = int(time_remaining.total_seconds())
    
    return {
        "game_status": data["game_status"],
        "cutoff_time": CUTOFF_TIME.isoformat(),
        "current_time": now.isoformat(),
        "time_remaining_seconds": time_remaining_seconds,
        "cutoff_reached": is_cutoff_reached(),
        "winner": data.get("winner"),
        "total_participants": len(data["users"]),
        "total_eggs": TOTAL_EGGS
    }

@app.post("/reset-data")
def reset_data(admin_key: str = None):
    """Reset all game data (admin only)"""
    # Simple admin protection - use environment variable
    expected_key = os.getenv('ADMIN_KEY', 'admin123')
    
    if admin_key != expected_key:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    data = {
        "users": {},
        "winner": None,
        "winner_announcement_time": None,
        "game_status": "active",
        "email_recipients": ["kendall.rush@walmart.com"]
    }
    save_data(data)
    
    return {"message": "Data reset successfully"}

def determine_final_winner(data):
    """Determine winner at cutoff time based on egg count"""
    if data.get("winner"):
        return
    
    if not data["users"]:
        return
    
    # Find user with most eggs
    max_eggs = 0
    winner_id = None
    
    for user_id, user in data["users"].items():
        if len(user["eggs_found"]) > max_eggs:
            max_eggs = len(user["eggs_found"])
            winner_id = user_id
    
    if winner_id:
        user = data["users"][winner_id]
        data["winner"] = {
            "user_id": winner_id,
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "eggs_found": len(user["eggs_found"]),
            "win_time": datetime.now(timezone.utc).isoformat()
        }
        data["winner_announcement_time"] = datetime.now(timezone.utc).isoformat()
        
        winner_name = f"{user['first_name']} {user['last_name']}"
        recipients = data.get("email_recipients", ["kendall.rush@walmart.com"])
        send_winner_email(winner_name, recipients)

@app.get("/email-recipients")
def get_email_recipients():
    """Get current email recipients for winner notification"""
    data = load_data()
    return {
        "recipients": data.get("email_recipients", ["kendall.rush@walmart.com"]),
        "message": "These people will be notified when a winner is found"
    }

class EmailRecipientsRequest(BaseModel):
    recipients: list[str]

@app.post("/email-recipients")
def set_email_recipients(request: EmailRecipientsRequest, admin_key: str = None):
    """Update email recipients (admin only)"""
    expected_key = os.getenv('ADMIN_KEY', 'admin123')
    
    if admin_key != expected_key:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    data = load_data()
    data["email_recipients"] = request.recipients
    save_data(data)
    
    return {
        "message": "Email recipients updated",
        "recipients": request.recipients
    }

@app.get("/")
def root():
    return {
        "name": "Digital Egg Hunt API",
        "version": "1.0",
        "endpoints": {
            "register": "/register (POST) - Register a participant",
            "scan": "/scan (POST) - Scan an egg",
            "leaderboard": "/leaderboard (GET) - Get live leaderboard",
            "status": "/status (GET) - Get game status and countdown",
            "email_recipients": "/email-recipients (GET) - View recipients",
            "set_recipients": "/email-recipients (POST) - Update recipients (admin)",
            "reset": "/reset-data (POST) - Reset all data (admin only)"
        }
    }

if __name__ == "__main__":
    import uvicorn
    initialize_data()
    uvicorn.run(app, host="0.0.0.0", port=8003)
