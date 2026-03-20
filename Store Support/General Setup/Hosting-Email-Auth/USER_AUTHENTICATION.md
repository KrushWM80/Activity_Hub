# User Authentication & Login Implementation

## Overview

The Job Code Teaming Dashboard implements a simple but effective authentication system using JSON file storage and session management. This guide covers the key patterns and code.

---

## 🔐 Authentication Model

### Components

1. **User Account Storage** (`data/users.json`)
   ```json
   {
       "admin": {
           "password": "hashed_password_or_plain",
           "role": "admin",
           "email": "admin@example.com"
       },
       "user1": {
           "password": "user_password",
           "role": "user",
           "email": "user1@example.com"
       }
   }
   ```

2. **Session Storage** (`data/sessions.json`)
   ```json
   {
       "session_token_123": {
           "username": "admin",
           "role": "admin",
           "login_time": "2025-01-21T10:30:00Z",
           "expires": "2025-01-21T18:30:00Z"
       }
   }
   ```

3. **Role-Based Access Control (RBAC)**
   - **Admin**: Full access (approve users, approve requests, export data)
   - **User**: Limited access (view data, submit requests)

---

## 🛠️ Implementation Pattern

### 1. Login Endpoint

```python
@app.post("/api/login")
async def login(credentials: dict):
    username = credentials.get("username")
    password = credentials.get("password")
    
    # Load users from JSON
    users = load_json("data/users.json")
    
    # Check if user exists and password matches
    if username in users and users[username]["password"] == password:
        # Generate session token
        session_token = generate_token()
        
        # Store session
        session = {
            "username": username,
            "role": users[username]["role"],
            "login_time": datetime.now().isoformat(),
            "expires": (datetime.now() + timedelta(hours=8)).isoformat()
        }
        save_session(session_token, session)
        
        return {"success": True, "token": session_token, "role": session["role"]}
    
    return {"success": False, "error": "Invalid credentials"}
```

### 2. Session Validation Middleware

```python
def verify_session(token: str):
    """Check if session token is valid and not expired"""
    sessions = load_json("data/sessions.json")
    
    if token not in sessions:
        return None
    
    session = sessions[token]
    
    # Check expiration
    expires = datetime.fromisoformat(session["expires"])
    if datetime.now() > expires:
        del sessions[token]
        save_json("data/sessions.json", sessions)
        return None
    
    return session

def require_auth(func):
    """Decorator to require valid session"""
    async def wrapper(request: Request, *args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        session = verify_session(token)
        
        if not session:
            return {"error": "Unauthorized"}, 401
        
        return await func(session, *args, **kwargs)
    return wrapper
```

### 3. Role-Based Access Control

```python
def require_role(*allowed_roles):
    """Decorator to require specific role"""
    def decorator(func):
        async def wrapper(session: dict, *args, **kwargs):
            if session["role"] not in allowed_roles:
                return {"error": "Forbidden"}, 403
            return await func(session, *args, **kwargs)
        return wrapper
    return decorator

# Usage examples
@app.post("/api/approve-request")
@require_auth
@require_role("admin")
async def approve_request(session: dict, request_id: str):
    # Only admins can approve requests
    pass

@app.get("/api/my-requests")
@require_auth
@require_role("user", "admin")
async def get_my_requests(session: dict):
    # Both users and admins can view requests
    pass
```

---

## 🌐 Frontend Login Implementation

### HTML Login Form

```html
<!DOCTYPE html>
<html>
<head>
    <title>Job Code Dashboard - Login</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
        }
        
        .login-box {
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            width: 300px;
        }
        
        .login-box h1 {
            text-align: center;
            color: #333;
            margin-top: 0;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 5px;
            color: #555;
            font-weight: bold;
        }
        
        .form-group input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
            font-size: 14px;
        }
        
        .form-group input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 5px rgba(102, 126, 234, 0.3);
        }
        
        .login-btn {
            width: 100%;
            padding: 10px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 20px;
        }
        
        .login-btn:hover {
            background: #5568d3;
        }
        
        .error-message {
            color: #e74c3c;
            font-size: 14px;
            margin-top: 10px;
            display: none;
        }
        
        .info-message {
            background: #ecf0f1;
            padding: 10px;
            border-radius: 4px;
            font-size: 12px;
            color: #555;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="login-box">
        <h1>🔐 Login</h1>
        <div class="info-message">
            Demo: username: <strong>admin</strong> | password: <strong>admin123</strong>
        </div>
        
        <form id="loginForm">
            <div class="form-group">
                <label for="username">Username:</label>
                <input 
                    type="text" 
                    id="username" 
                    name="username" 
                    required 
                    autofocus
                    autocomplete="username"
                >
            </div>
            
            <div class="form-group">
                <label for="password">Password:</label>
                <input 
                    type="password" 
                    id="password" 
                    name="password" 
                    required
                    autocomplete="current-password"
                >
            </div>
            
            <button type="submit" class="login-btn">Login</button>
        </form>
        
        <div class="error-message" id="errorMessage"></div>
    </div>

    <script>
        document.getElementById("loginForm").addEventListener("submit", async (e) => {
            e.preventDefault();
            
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;
            const errorDiv = document.getElementById("errorMessage");
            
            try {
                const response = await fetch("/api/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ username, password })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Store token in localStorage
                    localStorage.setItem("sessionToken", data.token);
                    localStorage.setItem("userRole", data.role);
                    
                    // Redirect to dashboard
                    window.location.href = "/dashboard.html";
                } else {
                    errorDiv.textContent = "Invalid username or password";
                    errorDiv.style.display = "block";
                }
            } catch (error) {
                errorDiv.textContent = "Login failed: " + error.message;
                errorDiv.style.display = "block";
            }
        });
    </script>
</body>
</html>
```

### JavaScript Session Management

```javascript
// Get token from localStorage
function getSessionToken() {
    return localStorage.getItem("sessionToken");
}

// Get user role
function getUserRole() {
    return localStorage.getItem("userRole");
}

// Make authenticated API call
async function apiCall(endpoint, method = "GET", body = null) {
    const token = getSessionToken();
    
    if (!token) {
        // Redirect to login
        window.location.href = "/login.html";
        return null;
    }
    
    const options = {
        method,
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        }
    };
    
    if (body) {
        options.body = JSON.stringify(body);
    }
    
    try {
        const response = await fetch(endpoint, options);
        
        if (response.status === 401) {
            // Token expired or invalid
            localStorage.removeItem("sessionToken");
            localStorage.removeItem("userRole");
            window.location.href = "/login.html";
            return null;
        }
        
        return await response.json();
    } catch (error) {
        console.error("API call failed:", error);
        return null;
    }
}

// Check role before showing elements
function showIfRole(elementId, ...allowedRoles) {
    const userRole = getUserRole();
    const element = document.getElementById(elementId);
    
    if (element) {
        element.style.display = allowedRoles.includes(userRole) ? "block" : "none";
    }
}

// Logout
function logout() {
    localStorage.removeItem("sessionToken");
    localStorage.removeItem("userRole");
    window.location.href = "/login.html";
}
```

---

## 🔑 Best Practices

### Security Considerations

1. **Password Storage**
   - ⚠️ Current implementation stores plain text - not production safe
   - ✅ Use `bcrypt` or `argon2` for real applications
   - Implementation:
     ```python
     from passlib.context import CryptContext
     pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
     
     # Hash password on registration
     hashed = pwd_context.hash(password)
     
     # Verify password on login
     if pwd_context.verify(password, hashed):
         # Login successful
     ```

2. **Session Tokens**
   - Use `secrets.token_urlsafe()` for secure random tokens
   - Set reasonable expiration times (4-8 hours typical)
   - Implement session refresh mechanism

3. **HTTPS in Production**
   - Always use HTTPS for login forms (prevents man-in-the-middle attacks)
   - HTTP OK for local/VPN-only access

4. **Rate Limiting**
   - Prevent brute force attacks
   - Limit login attempts per IP

---

## 📝 Key Learnings

✅ **JSON-based storage** works great for small team projects  
✅ **Simple decorators** make role-based access control easy  
✅ **localStorage** is convenient for frontend token storage (use httpOnly for production)  
✅ **Session expiration** prevents hijacked sessions from being used indefinitely  
✅ **Multiple user roles** enable flexible permission systems  

---

## 🎓 Related Files

- Source: `C:\Users\krush\Documents\VSCode\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend\main.py`
- Frontend: `JobCodeTeamingDashboard.html`
- See also: [WORKFLOW_PATTERNS.md](./WORKFLOW_PATTERNS.md) - Multi-step approval workflows
