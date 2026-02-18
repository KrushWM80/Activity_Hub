# GitHub Pages - Templates & Examples

## Template 1: Simple Landing Page

### Files
```
index.html
css/style.css
js/script.js
```

### index.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Project</title>
    <meta name="description" content="Description of my project">
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <nav>
            <h1>My Project</h1>
            <ul>
                <li><a href="#about">About</a></li>
                <li><a href="#features">Features</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>
    
    <section id="hero">
        <h2>Welcome to My Project</h2>
        <p>A brief description of what this project does.</p>
        <a href="#features" class="btn">Learn More</a>
    </section>
    
    <section id="features">
        <h2>Features</h2>
        <div class="feature-grid">
            <div class="feature">
                <h3>Feature 1</h3>
                <p>Description of feature 1</p>
            </div>
            <div class="feature">
                <h3>Feature 2</h3>
                <p>Description of feature 2</p>
            </div>
            <div class="feature">
                <h3>Feature 3</h3>
                <p>Description of feature 3</p>
            </div>
        </div>
    </section>
    
    <footer>
        <p>&copy; 2025 My Project. All rights reserved.</p>
    </footer>
    
    <script src="js/script.js"></script>
</body>
</html>
```

### css/style.css
```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
}

header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem 2rem;
}

nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

nav ul {
    list-style: none;
    display: flex;
    gap: 2rem;
}

nav a {
    color: white;
    text-decoration: none;
    transition: opacity 0.3s;
}

nav a:hover {
    opacity: 0.8;
}

#hero {
    text-align: center;
    padding: 4rem 2rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

#hero h2 {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.btn {
    display: inline-block;
    padding: 1rem 2rem;
    background: white;
    color: #667eea;
    text-decoration: none;
    border-radius: 5px;
    font-weight: bold;
    margin-top: 1rem;
    transition: transform 0.3s;
}

.btn:hover {
    transform: translateY(-2px);
}

#features {
    padding: 4rem 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

#features h2 {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 3rem;
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
}

.feature {
    padding: 2rem;
    background: #f4f4f4;
    border-radius: 10px;
    text-align: center;
}

.feature h3 {
    margin-bottom: 1rem;
    color: #667eea;
}

footer {
    background: #333;
    color: white;
    text-align: center;
    padding: 2rem;
    margin-top: 4rem;
}

@media (max-width: 768px) {
    nav {
        flex-direction: column;
        gap: 1rem;
    }
    
    #hero h2 {
        font-size: 2rem;
    }
}
```

---

## Template 2: Documentation Site

### Files
```
docs/
├── index.html
├── getting-started.html
├── api.html
├── css/
│   └── docs.css
└── js/
    └── docs.js
```

### docs/index.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documentation - My Project</title>
    <link rel="stylesheet" href="css/docs.css">
</head>
<body>
    <nav class="sidebar">
        <h2>Documentation</h2>
        <ul>
            <li><a href="index.html" class="active">Home</a></li>
            <li><a href="getting-started.html">Getting Started</a></li>
            <li><a href="api.html">API Reference</a></li>
            <li><a href="examples.html">Examples</a></li>
        </ul>
    </nav>
    
    <main class="content">
        <h1>Welcome to the Documentation</h1>
        
        <section id="intro">
            <h2>Introduction</h2>
            <p>This is the documentation for My Project.</p>
        </section>
        
        <section id="quick-start">
            <h2>Quick Start</h2>
            <pre><code>npm install my-project
npm start</code></pre>
        </section>
        
        <section id="features">
            <h2>Key Features</h2>
            <ul>
                <li>Feature 1</li>
                <li>Feature 2</li>
                <li>Feature 3</li>
            </ul>
        </section>
    </main>
    
    <script src="js/docs.js"></script>
</body>
</html>
```

### docs/css/docs.css
```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    display: grid;
    grid-template-columns: 250px 1fr;
    min-height: 100vh;
}

.sidebar {
    background: #2c3e50;
    color: white;
    padding: 2rem;
    position: fixed;
    width: 250px;
    height: 100vh;
    overflow-y: auto;
}

.sidebar h2 {
    margin-bottom: 2rem;
    border-bottom: 2px solid #3498db;
    padding-bottom: 0.5rem;
}

.sidebar ul {
    list-style: none;
}

.sidebar li {
    margin-bottom: 0.5rem;
}

.sidebar a {
    color: #ecf0f1;
    text-decoration: none;
    display: block;
    padding: 0.5rem;
    border-radius: 5px;
    transition: background 0.3s;
}

.sidebar a:hover,
.sidebar a.active {
    background: #34495e;
}

.content {
    margin-left: 250px;
    padding: 3rem;
    max-width: 900px;
}

.content h1 {
    font-size: 2.5rem;
    margin-bottom: 2rem;
    color: #2c3e50;
}

.content h2 {
    font-size: 2rem;
    margin-top: 3rem;
    margin-bottom: 1rem;
    color: #3498db;
}

.content section {
    margin-bottom: 3rem;
}

pre {
    background: #f4f4f4;
    padding: 1rem;
    border-radius: 5px;
    overflow-x: auto;
    border-left: 4px solid #3498db;
}

code {
    font-family: 'Courier New', monospace;
    color: #e74c3c;
}

@media (max-width: 768px) {
    body {
        grid-template-columns: 1fr;
    }
    
    .sidebar {
        position: relative;
        width: 100%;
        height: auto;
    }
    
    .content {
        margin-left: 0;
    }
}
```

---

## Template 3: Portfolio Site

### index.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Portfolio</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <nav>
            <h1>John Doe</h1>
            <ul>
                <li><a href="#about">About</a></li>
                <li><a href="#projects">Projects</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>
    
    <section id="hero">
        <div class="hero-content">
            <h2>Software Developer</h2>
            <p>Building amazing web applications</p>
        </div>
    </section>
    
    <section id="about">
        <h2>About Me</h2>
        <p>I'm a software developer with experience in web development.</p>
    </section>
    
    <section id="projects">
        <h2>My Projects</h2>
        <div class="project-grid">
            <div class="project-card">
                <h3>Project 1</h3>
                <p>Description of project 1</p>
                <a href="#" class="project-link">View Project →</a>
            </div>
            <div class="project-card">
                <h3>Project 2</h3>
                <p>Description of project 2</p>
                <a href="#" class="project-link">View Project →</a>
            </div>
            <div class="project-card">
                <h3>Project 3</h3>
                <p>Description of project 3</p>
                <a href="#" class="project-link">View Project →</a>
            </div>
        </div>
    </section>
    
    <section id="contact">
        <h2>Get In Touch</h2>
        <div class="contact-links">
            <a href="mailto:john@example.com">Email</a>
            <a href="https://github.com/johndoe">GitHub</a>
            <a href="https://linkedin.com/in/johndoe">LinkedIn</a>
        </div>
    </section>
    
    <footer>
        <p>&copy; 2025 John Doe. All rights reserved.</p>
    </footer>
</body>
</html>
```

---

## Template 4: Data Dashboard

### index.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Dashboard</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>📊 Data Dashboard</h1>
        <button id="refresh-btn">Refresh Data</button>
    </header>
    
    <main>
        <div class="stats-grid">
            <div class="stat-card">
                <h3>Total Users</h3>
                <p class="stat-value" id="total-users">Loading...</p>
            </div>
            <div class="stat-card">
                <h3>Active Today</h3>
                <p class="stat-value" id="active-today">Loading...</p>
            </div>
            <div class="stat-card">
                <h3>Revenue</h3>
                <p class="stat-value" id="revenue">Loading...</p>
            </div>
            <div class="stat-card">
                <h3>Growth</h3>
                <p class="stat-value" id="growth">Loading...</p>
            </div>
        </div>
        
        <div class="data-table">
            <h2>Recent Activity</h2>
            <table id="activity-table">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>User</th>
                        <th>Action</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody id="table-body">
                    <tr>
                        <td colspan="4">Loading...</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </main>
    
    <script>
        // Load data from JSON file or API
        async function loadData() {
            try {
                // Load from data.json or external API
                const response = await fetch('data.json');
                const data = await response.json();
                
                // Update stats
                document.getElementById('total-users').textContent = data.totalUsers;
                document.getElementById('active-today').textContent = data.activeToday;
                document.getElementById('revenue').textContent = '$' + data.revenue;
                document.getElementById('growth').textContent = data.growth + '%';
                
                // Update table
                const tbody = document.getElementById('table-body');
                tbody.innerHTML = data.recentActivity.map(item => `
                    <tr>
                        <td>${item.date}</td>
                        <td>${item.user}</td>
                        <td>${item.action}</td>
                        <td>${item.status}</td>
                    </tr>
                `).join('');
                
            } catch (error) {
                console.error('Error loading data:', error);
            }
        }
        
        // Refresh button
        document.getElementById('refresh-btn').addEventListener('click', loadData);
        
        // Load data on page load
        loadData();
    </script>
</body>
</html>
```

### data.json
```json
{
    "totalUsers": 1523,
    "activeToday": 342,
    "revenue": 12450,
    "growth": 23.5,
    "recentActivity": [
        {
            "date": "2025-12-17",
            "user": "John Doe",
            "action": "Login",
            "status": "Success"
        },
        {
            "date": "2025-12-17",
            "user": "Jane Smith",
            "action": "Purchase",
            "status": "Completed"
        }
    ]
}
```

---

## Template 5: Search Interface

### index.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search Interface</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>🔍 Search Tool</h1>
        </header>
        
        <div class="search-box">
            <input type="text" 
                   id="search-input" 
                   placeholder="Search for items..." 
                   autocomplete="off">
            <button id="search-btn">Search</button>
        </div>
        
        <div id="results-container">
            <p class="hint">Start typing to search...</p>
        </div>
    </div>
    
    <script>
        let allData = [];
        
        // Load data
        async function loadData() {
            const response = await fetch('data.json');
            allData = await response.json();
        }
        
        // Search function
        function search(query) {
            if (!query) {
                document.getElementById('results-container').innerHTML = 
                    '<p class="hint">Start typing to search...</p>';
                return;
            }
            
            const results = allData.filter(item => 
                item.name.toLowerCase().includes(query.toLowerCase()) ||
                item.description.toLowerCase().includes(query.toLowerCase())
            );
            
            displayResults(results);
        }
        
        // Display results
        function displayResults(results) {
            const container = document.getElementById('results-container');
            
            if (results.length === 0) {
                container.innerHTML = '<p class="no-results">No results found</p>';
                return;
            }
            
            container.innerHTML = results.map(item => `
                <div class="result-card">
                    <h3>${item.name}</h3>
                    <p>${item.description}</p>
                </div>
            `).join('');
        }
        
        // Event listeners
        document.getElementById('search-input').addEventListener('input', (e) => {
            search(e.target.value);
        });
        
        document.getElementById('search-btn').addEventListener('click', () => {
            const query = document.getElementById('search-input').value;
            search(query);
        });
        
        // Load data on page load
        loadData();
    </script>
</body>
</html>
```

---

## Deployment Scripts

### deploy.ps1
```powershell
# deploy.ps1 - Deploy to GitHub Pages

Write-Host "Deploying to GitHub Pages..." -ForegroundColor Cyan

# Build (if needed)
# npm run build

# Commit all changes
git add -A
git commit -m "Deploy $(Get-Date -Format 'yyyy-MM-dd HH:mm')"

# Push to GitHub
git push origin main

Write-Host "Deployment complete!" -ForegroundColor Green
Write-Host "Site will be live at: https://username.github.io/my-project/" -ForegroundColor Yellow
Write-Host "Wait 1-2 minutes for GitHub to rebuild the site"
```

### build-and-deploy.ps1
```powershell
# build-and-deploy.ps1 - Build and deploy

Write-Host "Building project..." -ForegroundColor Cyan

# Run build command (adjust for your project)
npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "Build successful!" -ForegroundColor Green

# Copy build to docs/ folder (if using /docs)
if (Test-Path "dist") {
    Copy-Item -Path "dist/*" -Destination "docs/" -Recurse -Force
    Write-Host "Copied build to docs/" -ForegroundColor Green
}

# Deploy
git add -A
git commit -m "Build and deploy $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
git push origin main

Write-Host "Deployment complete!" -ForegroundColor Green
```

---

**Use These Templates**: Copy and customize for your projects!
