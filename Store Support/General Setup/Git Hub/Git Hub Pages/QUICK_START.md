# GitHub Pages - Quick Start Guide

## 🚀 Deploy in 5 Minutes

### 1. Create Repository
```
1. Go to GitHub.com
2. Click "New Repository"
3. Name: my-project
4. Public repository
5. Initialize with README
6. Create repository
```

### 2. Add Your Files
```
Create: index.html
```

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Project</title>
</head>
<body>
    <h1>Hello World!</h1>
    <p>Welcome to my GitHub Pages site.</p>
</body>
</html>
```

### 3. Enable GitHub Pages
```
1. Go to Settings → Pages
2. Source: Deploy from branch
3. Branch: main
4. Folder: / (root)
5. Click Save
```

### 4. Visit Your Site
```
https://username.github.io/my-project/
```

**Done!** 🎉

---

## 📁 Repository Structures

### Option 1: Simple Site (Root)
```
my-project/
├── index.html
├── style.css
└── script.js

Settings:
- Branch: main
- Folder: / (root)
```

### Option 2: Documentation Site (/docs)
```
my-project/
├── src/              # Your code
├── docs/             # GitHub Pages
│   ├── index.html
│   └── style.css
└── README.md

Settings:
- Branch: main
- Folder: /docs
```

### Option 3: User Site (username.github.io)
```
username.github.io/   # Special repo name
├── index.html
└── css/
    └── style.css

Access: https://username.github.io/
```

---

## 🔄 Update Your Site

```powershell
# Edit files locally
# Then commit and push

git add .
git commit -m "Update site"
git push origin main

# Wait 1-2 minutes
# Site automatically rebuilds
```

---

## 🌐 Custom Domain (Optional)

### Add CNAME File
```
Create file: CNAME
Content: www.example.com
```

### Configure DNS
```
Type: CNAME
Host: www
Value: username.github.io
```

### Enable HTTPS
```
Settings → Pages
☑ Enforce HTTPS
```

---

## 🛠️ Common Commands

### Local Testing
```powershell
# Start simple server
python -m http.server 8000

# Open browser
http://localhost:8000
```

### Git Commands
```powershell
# Clone repository
git clone https://github.com/username/my-project.git

# Create new branch
git checkout -b new-feature

# Add files
git add .

# Commit changes
git commit -m "Description"

# Push to GitHub
git push origin main
```

---

## 📊 Load External Data

### JSON File
```javascript
// data.json
{
    "items": ["Item 1", "Item 2", "Item 3"]
}

// script.js
async function loadData() {
    const response = await fetch('data.json');
    const data = await response.json();
    console.log(data.items);
}
```

### External API
```javascript
async function loadAPI() {
    const response = await fetch('https://api.example.com/data');
    const data = await response.json();
    // Use data
}
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| 404 Error | Check Settings → Pages is enabled |
| CSS Not Loading | Use relative paths: `./style.css` |
| Site Not Updating | Clear cache (Ctrl+F5), wait 2 min |
| Domain Not Working | Check DNS, wait 24 hours |

---

## 📚 Next Steps

- **Full Guide**: See `GITHUB_PAGES_GUIDE.md`
- **Examples**: See `EXAMPLES.md`
- **Templates**: See `TEMPLATES.md`

---

## 🔗 Quick Links

- **Your Sites**: https://github.com/username?tab=repositories
- **GitHub Pages**: https://pages.github.com/
- **Documentation**: https://docs.github.com/pages

---

**Ready to Deploy!** 🚀
