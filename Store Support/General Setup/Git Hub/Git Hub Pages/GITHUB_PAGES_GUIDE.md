# GitHub Pages - Complete Deployment Guide

## Overview

GitHub Pages is a free static site hosting service that turns your GitHub repository into a live website.

**Key Features**:
- **Free Hosting** - No cost for public repositories
- **Custom Domains** - Use your own domain or `username.github.io`
- **HTTPS Support** - Automatic SSL certificates
- **Jekyll Integration** - Built-in static site generator
- **Version Control** - Git-based deployment workflow
- **CI/CD Integration** - GitHub Actions for automated builds

**Limitations**:
- Static sites only (HTML, CSS, JavaScript)
- No server-side code (PHP, Python, Node.js)
- 1 GB repository size limit
- 100 GB bandwidth/month soft limit
- Public sites only (unless GitHub Pro)

---

## 🚀 Quick Start

### Option 1: Simple HTML Site

**1. Create Repository**:
```
Repository name: my-project
Public repository
Initialize with README
```

**2. Add Files**:
```
index.html          # Your main page
style.css           # Styles
script.js           # JavaScript
```

**3. Enable GitHub Pages**:
- Go to Settings → Pages
- Source: Deploy from branch
- Branch: `main` / `docs` / `gh-pages`
- Folder: `/` (root) or `/docs`
- Click Save

**4. Access Your Site**:
```
https://username.github.io/my-project/
```

### Option 2: Project Documentation Site

**1. Create `/docs` Folder**:
```
/docs
  index.html
  README.md
  styles.css
```

**2. Enable GitHub Pages**:
- Source: Deploy from branch
- Branch: `main`
- Folder: `/docs`

**3. Access**:
```
https://username.github.io/my-project/
```

### Option 3: User/Organization Site

**1. Create Special Repository**:
```
Repository name: username.github.io
(Must match your username exactly)
```

**2. Add Files**:
```
index.html
```

**3. Enable GitHub Pages**:
- Automatically enabled for username.github.io repos
- No configuration needed

**4. Access**:
```
https://username.github.io/
```

---

## 📁 Repository Structure Options

### Structure 1: Root-Based (Simple Projects)

```
my-project/
├── index.html          # Main page
├── about.html          # Additional pages
├── css/
│   └── style.css
├── js/
│   └── script.js
├── images/
│   └── logo.png
└── README.md           # Project documentation
```

**Configuration**:
- Branch: `main`
- Folder: `/` (root)

### Structure 2: Docs-Based (Code + Docs)

```
my-project/
├── src/                # Source code
│   ├── main.py
│   └── utils.py
├── docs/               # GitHub Pages content
│   ├── index.html
│   ├── api.html
│   └── css/
│       └── style.css
├── tests/              # Tests
└── README.md           # Main README
```

**Configuration**:
- Branch: `main`
- Folder: `/docs`

**Benefits**: Separates code from documentation

### Structure 3: Branch-Based (Clean Separation)

```
main branch:            # Source code
my-project/
├── src/
├── tests/
└── README.md

gh-pages branch:        # Deployed site
my-project/
├── index.html
├── css/
└── js/
```

**Configuration**:
- Branch: `gh-pages`
- Folder: `/` (root)

**Benefits**: Complete separation of source and deployment

---

## 🎨 Frontend Development

### Basic HTML Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Project</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <nav>
            <a href="index.html">Home</a>
            <a href="about.html">About</a>
            <a href="docs.html">Docs</a>
        </nav>
    </header>
    
    <main>
        <h1>Welcome to My Project</h1>
        <p>This is a GitHub Pages site.</p>
    </main>
    
    <footer>
        <p>&copy; 2025 My Project</p>
    </footer>
    
    <script src="js/script.js"></script>
</body>
</html>
```

### Responsive CSS

```css
/* style.css */
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
    background: #0071ce;
    color: white;
    padding: 1rem;
}

nav a {
    color: white;
    text-decoration: none;
    margin: 0 1rem;
}

main {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 1rem;
}

/* Responsive design */
@media (max-width: 768px) {
    nav a {
        display: block;
        margin: 0.5rem 0;
    }
}
```

### Loading External Data

```javascript
// script.js - Fetch data from external API or JSON file

async function loadData() {
    try {
        // Load from external API
        const response = await fetch('https://api.example.com/data');
        const data = await response.json();
        displayData(data);
    } catch (error) {
        console.error('Error loading data:', error);
        document.getElementById('content').innerHTML = 
            'Failed to load data. Please try again later.';
    }
}

function displayData(data) {
    const container = document.getElementById('content');
    container.innerHTML = data.map(item => `
        <div class="item">
            <h3>${item.title}</h3>
            <p>${item.description}</p>
        </div>
    `).join('');
}

// Load data when page loads
document.addEventListener('DOMContentLoaded', loadData);
```

---

## 🔧 Advanced Features

### Custom 404 Page

Create `404.html` in root:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Page Not Found</title>
</head>
<body>
    <h1>404 - Page Not Found</h1>
    <p>The page you're looking for doesn't exist.</p>
    <a href="/">Go Home</a>
</body>
</html>
```

### Single Page Application (SPA)

For React/Vue/Angular apps with client-side routing:

**1. Create `404.html`** (redirect to index.html):
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>
        // Redirect to index.html with path preserved
        sessionStorage.redirect = location.href;
    </script>
    <meta http-equiv="refresh" content="0;URL='/'">
</head>
</html>
```

**2. Add to `index.html`**:
```html
<script>
    // Restore path after redirect
    (function() {
        var redirect = sessionStorage.redirect;
        delete sessionStorage.redirect;
        if (redirect && redirect != location.href) {
            history.replaceState(null, null, redirect);
        }
    })();
</script>
```

### Environment-Specific Configuration

```javascript
// config.js
const config = {
    development: {
        apiUrl: 'http://localhost:3000/api',
        debug: true
    },
    production: {
        apiUrl: 'https://api.example.com',
        debug: false
    }
};

// Detect environment
const environment = window.location.hostname === 'localhost' 
    ? 'development' 
    : 'production';

export default config[environment];
```

---

## 🌐 Custom Domains

### Option 1: Custom Domain (www.example.com)

**1. Add CNAME File**:
Create `CNAME` file in repository root:
```
www.example.com
```

**2. Configure DNS**:
Add CNAME record at your domain provider:
```
Type: CNAME
Host: www
Value: username.github.io
TTL: 3600
```

**3. Enable in GitHub**:
- Settings → Pages
- Custom domain: `www.example.com`
- Enforce HTTPS: Check

### Option 2: Apex Domain (example.com)

**1. Add CNAME File**:
```
example.com
```

**2. Configure DNS**:
Add A records:
```
Type: A
Host: @
Value: 185.199.108.153
       185.199.109.153
       185.199.110.153
       185.199.111.153
TTL: 3600
```

**3. Add AAAA Records** (IPv6):
```
Type: AAAA
Host: @
Value: 2606:50c0:8000::153
       2606:50c0:8001::153
       2606:50c0:8002::153
       2606:50c0:8003::153
```

### Subdomain for Project

```
Type: CNAME
Host: project
Value: username.github.io
```

Access: `https://project.example.com`

---

## 🔄 Deployment Workflows

### Method 1: Direct Git Push (Simple)

```powershell
# Make changes to files
git add .
git commit -m "Update site"
git push origin main

# GitHub automatically rebuilds and deploys
# Wait 1-2 minutes for deployment
```

### Method 2: GitHub Actions (Automated Build)

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm install
      
      - name: Build site
        run: npm run build
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v2
        with:
          path: ./dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v2
```

**Configure**:
- Settings → Pages
- Source: GitHub Actions

### Method 3: Branch-Based Deployment

```powershell
# Work on main branch
git checkout main
# Make changes

# Build for production
npm run build

# Switch to gh-pages branch
git checkout gh-pages

# Copy build files
Copy-Item -Path dist/* -Destination . -Recurse -Force

# Commit and push
git add .
git commit -m "Deploy update"
git push origin gh-pages

# Switch back to main
git checkout main
```

### Method 4: Automated Script

**PowerShell deployment script** (`deploy.ps1`):
```powershell
# deploy.ps1 - Deploy to GitHub Pages

Write-Host "Building site..." -ForegroundColor Cyan

# Build (if needed)
# npm run build

# Create temporary directory
$tempDir = "gh-pages-temp"
if (Test-Path $tempDir) {
    Remove-Item -Recurse -Force $tempDir
}

# Clone gh-pages branch
git clone --branch gh-pages --single-branch . $tempDir

# Copy new files
Copy-Item -Path "dist/*" -Destination $tempDir -Recurse -Force

# Commit and push
Push-Location $tempDir
git add -A
git commit -m "Deploy $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
git push origin gh-pages
Pop-Location

# Cleanup
Remove-Item -Recurse -Force $tempDir

Write-Host "Deployment complete!" -ForegroundColor Green
Write-Host "Site will be live in 1-2 minutes"
```

**Usage**:
```powershell
.\deploy.ps1
```

---

## 📊 Static Data Patterns

### Pattern 1: Embedded JSON

```html
<script>
    const data = {
        "items": [
            {"name": "Item 1", "value": 100},
            {"name": "Item 2", "value": 200}
        ]
    };
    
    // Use data directly
    console.log(data.items);
</script>
```

### Pattern 2: External JSON File

**data.json**:
```json
{
    "items": [
        {"name": "Item 1", "value": 100},
        {"name": "Item 2", "value": 200}
    ]
}
```

**script.js**:
```javascript
async function loadData() {
    const response = await fetch('data.json');
    const data = await response.json();
    return data.items;
}
```

### Pattern 3: Generated at Build Time

**build.ps1**:
```powershell
# Extract data from source
$data = Get-Content "source.csv" | ConvertFrom-Csv

# Convert to JSON
$json = $data | ConvertTo-Json

# Write to file
$json | Out-File "docs/data.json" -Encoding UTF8

# Commit and push
git add docs/data.json
git commit -m "Update data"
git push
```

### Pattern 4: External API

```javascript
// Fetch from external API
async function loadLiveData() {
    const response = await fetch('https://api.example.com/data');
    const data = await response.json();
    return data;
}

// Cache in localStorage
function getCachedData() {
    const cached = localStorage.getItem('data');
    if (cached) {
        const { data, timestamp } = JSON.parse(cached);
        // Return cached if less than 1 hour old
        if (Date.now() - timestamp < 3600000) {
            return data;
        }
    }
    return null;
}

function setCachedData(data) {
    localStorage.setItem('data', JSON.stringify({
        data: data,
        timestamp: Date.now()
    }));
}
```

---

## 🔐 Security Considerations

### No Sensitive Data

**❌ Never commit**:
- API keys
- Passwords
- Database credentials
- Private tokens
- Personal information

**✅ Use instead**:
- Environment variables (for builds)
- External APIs with CORS
- Public data only
- Client-side authentication redirects

### Content Security

```html
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self' 'unsafe-inline'; 
               style-src 'self' 'unsafe-inline';">
```

### CORS Issues

If calling external APIs:
```javascript
// External API must allow your domain
// Or use a CORS proxy service (development only)

const response = await fetch('https://api.example.com/data', {
    mode: 'cors',
    headers: {
        'Accept': 'application/json'
    }
});
```

---

## 🛠️ Build Tools Integration

### Using with React

```bash
# Create React app
npx create-react-app my-app
cd my-app

# Add homepage to package.json
"homepage": "https://username.github.io/my-app"

# Install gh-pages
npm install --save-dev gh-pages

# Add scripts to package.json
"predeploy": "npm run build"
"deploy": "gh-pages -d build"

# Deploy
npm run deploy
```

### Using with Vue

```bash
# Create Vue app
npm create vue@latest my-app
cd my-app

# Create vue.config.js
module.exports = {
  publicPath: process.env.NODE_ENV === 'production'
    ? '/my-app/'
    : '/'
}

# Build
npm run build

# Deploy dist/ folder to gh-pages branch
```

### Using with Jekyll

GitHub Pages has built-in Jekyll support:

**_config.yml**:
```yaml
title: My Site
description: My GitHub Pages site
theme: jekyll-theme-minimal

# Exclude files
exclude:
  - README.md
  - Gemfile
  - Gemfile.lock
```

**index.md**:
```markdown
---
layout: default
title: Home
---

# Welcome

This is my Jekyll site hosted on GitHub Pages.
```

---

## 📱 Progressive Web App (PWA)

### Manifest File

**manifest.json**:
```json
{
    "name": "My App",
    "short_name": "MyApp",
    "description": "My GitHub Pages App",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#ffffff",
    "theme_color": "#0071ce",
    "icons": [
        {
            "src": "icons/icon-192.png",
            "sizes": "192x192",
            "type": "image/png"
        },
        {
            "src": "icons/icon-512.png",
            "sizes": "512x512",
            "type": "image/png"
        }
    ]
}
```

### Service Worker

**sw.js**:
```javascript
const CACHE_NAME = 'my-app-v1';
const urlsToCache = [
    '/',
    '/css/style.css',
    '/js/script.js',
    '/images/logo.png'
];

// Install service worker
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

// Serve from cache
self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => response || fetch(event.request))
    );
});
```

**Register in index.html**:
```html
<script>
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js')
            .then(reg => console.log('SW registered', reg))
            .catch(err => console.log('SW error', err));
    }
</script>
```

---

## 🐛 Troubleshooting

### Common Issues

**1. 404 Page Not Found**
- Check repository name matches URL
- Verify GitHub Pages is enabled
- Check branch and folder settings
- Wait 1-2 minutes after enabling

**2. CSS/JS Not Loading**
- Use relative paths: `./css/style.css` not `/css/style.css`
- For projects: `/my-project/css/style.css`
- Check file names (case-sensitive)

**3. Site Not Updating**
- Hard refresh browser (Ctrl+F5)
- Clear browser cache
- Check GitHub Actions for build errors
- Wait 1-2 minutes for deployment

**4. Custom Domain Not Working**
- Verify DNS records (use `nslookup`)
- Check CNAME file exists
- Enable "Enforce HTTPS" in settings
- Wait up to 24 hours for DNS propagation

**5. Jekyll Build Errors**
- Check `.github/workflows` for errors
- Verify `_config.yml` syntax
- Check for unsupported plugins
- Review GitHub Pages build logs

### Debugging Tips

**View Build Status**:
- Repository → Actions tab
- Check latest workflow run
- View logs for errors

**Test Locally**:
```powershell
# Simple HTTP server
python -m http.server 8000

# Or with Node.js
npx http-server

# Open http://localhost:8000
```

**Check DNS**:
```powershell
nslookup www.example.com
```

**Validate HTML**:
- Use W3C Validator: https://validator.w3.org/

---

## 📋 Deployment Checklist

### Pre-Deployment
- [ ] Test all pages locally
- [ ] Validate HTML/CSS
- [ ] Check all links work
- [ ] Test on mobile devices
- [ ] Optimize images (compress)
- [ ] Remove console.log statements
- [ ] Add meta tags (title, description)
- [ ] Create favicon.ico

### Repository Setup
- [ ] Create repository (public)
- [ ] Add .gitignore file
- [ ] Write README.md
- [ ] Add LICENSE file

### GitHub Pages Configuration
- [ ] Enable GitHub Pages
- [ ] Select branch and folder
- [ ] Add custom domain (optional)
- [ ] Enforce HTTPS

### Post-Deployment
- [ ] Test live site
- [ ] Check on multiple browsers
- [ ] Verify mobile responsiveness
- [ ] Test all functionality
- [ ] Share URL with team
- [ ] Add to README.md

---

## 🎯 Best Practices

### Performance
- **Minify CSS/JS**: Use build tools
- **Optimize Images**: Compress before upload
- **Use CDN**: For libraries (Bootstrap, jQuery)
- **Lazy Load**: Images below fold
- **Cache Assets**: Use service workers

### SEO
- **Meta Tags**: Title, description, keywords
- **Semantic HTML**: Use proper heading structure
- **Alt Text**: For all images
- **Sitemap**: Add sitemap.xml
- **Robots.txt**: Control crawling

### Accessibility
- **ARIA Labels**: For interactive elements
- **Keyboard Navigation**: Tab through site
- **Color Contrast**: WCAG compliant
- **Screen Readers**: Test with NVDA/JAWS

### Maintainability
- **Documentation**: README with setup
- **Comments**: Explain complex code
- **Version Control**: Meaningful commits
- **Consistent Style**: Use linter/formatter

---

## 📚 Resources

### Official Documentation
- GitHub Pages: https://pages.github.com/
- GitHub Actions: https://docs.github.com/actions
- Jekyll: https://jekyllrb.com/

### Tools
- **Validators**:
  - HTML: https://validator.w3.org/
  - CSS: https://jigsaw.w3.org/css-validator/
  
- **Image Optimization**:
  - TinyPNG: https://tinypng.com/
  - Squoosh: https://squoosh.app/

- **Icons**:
  - Font Awesome: https://fontawesome.com/
  - Feather Icons: https://feathericons.com/

### Themes & Templates
- **Jekyll Themes**: https://jekyllthemes.io/
- **HTML5 UP**: https://html5up.net/
- **Bootstrap**: https://getbootstrap.com/

---

**Last Updated**: December 17, 2025  
**Version**: 1.0  
**Status**: Production Ready
