# Code Puppy - Documentation & Resources

**Last Updated:** December 3, 2025

## What is Code Puppy?

Code Puppy is Walmart's internal platform for creating and hosting **single HTML page applications** that can connect to BigQuery for data visualization and interactive dashboards.

## Key Constraints

### Single HTML Page Only
- ❌ **Cannot** use multi-file applications
- ❌ **Cannot** use build processes (webpack, React compilation, etc.)
- ❌ **Cannot** reference external JavaScript/CSS files
- ✅ **Must** embed all JavaScript, CSS, and HTML in one file
- ✅ **Can** connect to BigQuery directly
- ✅ **Can** use inline JavaScript for interactivity

### What This Means for React/Node.js Apps
If you have a React + Node.js application like the Refresh Guide:
- Your **React frontend** cannot be used directly (requires compilation & multiple files)
- Your **Node.js backend** cannot be hosted in Code Puppy (server-side only)
- You **must create** a standalone HTML version with embedded JavaScript
- You **can connect** the HTML directly to BigQuery to replace the backend

## Code Puppy Use Cases

### ✅ Good For:
- **Data visualizations** from BigQuery
- **Interactive dashboards** with charts/graphs
- **Simple CRUD interfaces** backed by BigQuery
- **Reporting tools** with filters and search
- **Form-based data entry** to BigQuery tables
- **Proof-of-concept demos** for stakeholders

### ❌ Not Good For:
- Complex multi-page applications
- Apps requiring authentication servers
- Apps with multiple API endpoints
- Apps needing real-time websockets
- Apps requiring npm package compilation
- Full-stack applications with separate frontend/backend

## Creating Code Puppy Pages

### Method 1: Build from Scratch
Create a single HTML file with:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My App</title>
    <style>
        /* All CSS goes here */
    </style>
</head>
<body>
    <!-- All HTML goes here -->
    
    <script>
        // All JavaScript goes here
        // BigQuery connection code here
    </script>
</body>
</html>
```

### Method 2: Convert Existing App
If you have an existing React/Angular/Vue app:

**Option A: Simplify & Recreate**
1. Identify core features needed
2. Recreate UI with vanilla HTML/CSS
3. Recreate logic with vanilla JavaScript
4. Replace backend API calls with BigQuery queries

**Option B: Use AI Assistant**
1. Share your app structure and key components
2. Request a single-file HTML version
3. AI can consolidate your multi-file app into one page
4. Add BigQuery connection points

## BigQuery Integration

### Connection Pattern
```javascript
// Example BigQuery query in Code Puppy
async function loadData() {
    try {
        const query = `
            SELECT * FROM \`project.dataset.table\`
            WHERE condition = true
            ORDER BY column
        `;
        
        const response = await fetch('/api/bigquery', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });
        
        const data = await response.json();
        renderData(data);
    } catch (error) {
        console.error('Error loading data:', error);
    }
}
```

### Common Patterns

**Load Data:**
```javascript
const query = `
    SELECT area_name, topic_name, item_name, status
    FROM \`walmart-project.refresh_guide.items\`
    ORDER BY area_name, topic_name
`;
```

**Insert Data:**
```javascript
const query = `
    INSERT INTO \`walmart-project.refresh_guide.items\`
    (area_name, topic_name, item_name, status, created_at)
    VALUES ('Backroom', 'Optimization', 'Review layout', 'Pending', CURRENT_TIMESTAMP())
`;
```

**Update Data:**
```javascript
const query = `
    UPDATE \`walmart-project.refresh_guide.items\`
    SET status = 'Completed', updated_at = CURRENT_TIMESTAMP()
    WHERE item_id = '123'
`;
```

**Delete Data:**
```javascript
const query = `
    DELETE FROM \`walmart-project.refresh_guide.items\`
    WHERE item_id = '123'
`;
```

## Best Practices

### 1. Structure Your Code
Organize your single HTML file with clear sections:
- **CSS** at the top in `<style>` tags
- **HTML** in the body
- **JavaScript** at the bottom in `<script>` tags

### 2. Use Modern JavaScript
- ES6+ features (const, let, arrow functions, template literals)
- Async/await for cleaner asynchronous code
- Array methods (map, filter, reduce)

### 3. Keep State Management Simple
```javascript
// Global state object
let appState = {
    data: [],
    currentView: 'dashboard',
    filters: {}
};

// Update functions
function updateState(newState) {
    appState = { ...appState, ...newState };
    render();
}
```

### 4. Modular Functions
Break your JavaScript into small, focused functions:
```javascript
// Data functions
function loadData() { /* ... */ }
function saveData() { /* ... */ }

// UI functions
function renderDashboard() { /* ... */ }
function renderTable() { /* ... */ }

// Utility functions
function formatDate() { /* ... */ }
function validateInput() { /* ... */ }
```

### 5. Error Handling
Always include error handling:
```javascript
async function loadData() {
    try {
        const response = await fetch('/api/bigquery', { /* ... */ });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
        showErrorMessage('Failed to load data');
        return [];
    }
}
```

### 6. Loading States
Provide user feedback:
```javascript
function showLoading() {
    document.getElementById('content').innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Loading data...</p>
        </div>
    `;
}

function hideLoading() {
    document.getElementById('content').innerHTML = '';
}
```

## Walmart Branding

### Standard Colors
```css
:root {
    --walmart-blue: #0071ce;
    --walmart-dark-blue: #004f9a;
    --walmart-yellow: #ffc220;
    --walmart-dark-yellow: #f2a900;
    --gray-light: #f8f9fa;
    --gray-medium: #6c757d;
    --gray-dark: #333333;
}
```

### Typography
```css
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #333333;
    line-height: 1.6;
}

h1, h2, h3 {
    color: #004f9a;
    font-weight: 600;
}
```

### Button Styles
```css
.btn-primary {
    background: #0071ce;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    transition: background 0.3s;
}

.btn-primary:hover {
    background: #004f9a;
}
```

## Example Template

See `refresh-guide-template.html` in this folder for a complete example of:
- Walmart-branded UI
- BigQuery integration points
- CRUD operations
- Hierarchical data display (Areas → Topics → Items)
- Search/filter functionality
- Modal dialogs
- Form handling

## Resources

### Internal Resources
- **Code Puppy Platform:** [Internal Link - Add URL]
- **BigQuery Documentation:** [Internal Link - Add URL]
- **Walmart Design System:** [Internal Link - Add URL]

### External Learning Resources
- **MDN Web Docs:** https://developer.mozilla.org/
- **JavaScript Info:** https://javascript.info/
- **CSS Tricks:** https://css-tricks.com/

## Common Issues & Solutions

### Issue: Data Not Loading
**Problem:** BigQuery queries failing or returning empty results

**Solutions:**
1. Check query syntax in BigQuery console first
2. Verify project/dataset/table names are correct
3. Check permissions for the service account
4. Add console.log() to see actual error messages
5. Use browser DevTools Network tab to inspect requests

### Issue: UI Not Updating
**Problem:** Data loads but UI doesn't change

**Solutions:**
1. Ensure you're calling render functions after data updates
2. Check for JavaScript errors in console
3. Verify DOM element IDs match your code
4. Use innerHTML or appendChild to update DOM

### Issue: Styling Not Working
**Problem:** CSS not applying as expected

**Solutions:**
1. Check CSS selector specificity
2. Use browser DevTools to inspect computed styles
3. Verify no typos in class names
4. Check for conflicting styles

### Issue: Forms Not Submitting
**Problem:** Form submission doesn't trigger action

**Solutions:**
1. Add `event.preventDefault()` in form submit handler
2. Verify form ID matches JavaScript selector
3. Check that submit button is type="submit"
4. Add console.log() to confirm function is called

## Migration Checklist

When converting an existing app to Code Puppy:

- [ ] Identify core features needed (remove nice-to-haves)
- [ ] Map data flow (what data comes from where)
- [ ] Design BigQuery schema to replace backend
- [ ] Create single HTML file structure
- [ ] Copy/adapt CSS styling
- [ ] Recreate UI layout in HTML
- [ ] Rewrite JavaScript logic (remove framework-specific code)
- [ ] Add BigQuery connection code
- [ ] Test CRUD operations
- [ ] Add error handling
- [ ] Add loading states
- [ ] Verify Walmart branding
- [ ] Test with real data
- [ ] Get stakeholder approval
- [ ] Deploy to Code Puppy platform

## Contact & Support

**Questions about Code Puppy?**
- Team: [Add team name]
- Slack: [Add channel]
- Email: [Add email]

**Questions about BigQuery?**
- Data Architecture Team
- Slack: [Add channel]

**Questions about this documentation?**
- Created by: Kendall Rush
- Last Updated: December 3, 2025
