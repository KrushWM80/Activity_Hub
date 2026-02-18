# Distribution List Selector

A web-based tool for browsing, searching, and selecting Walmart distribution lists.

## 🚀 Features

- **Smart Search**: Real-time keyword search across 134,681+ distribution lists
- **Type-ahead Selection**: Autocomplete dropdown with type-ahead support for quick list selection
- **Advanced Filtering**: Filter by category (General, Market, Team, Operations, etc.) and size
- **Multi-Select**: Select multiple lists with checkboxes or type-ahead
- **Visual Tags**: See selected lists as removable tags
- **Direct Email Composition**: Opens Outlook Web with selected lists
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Fast Performance**: Client-side filtering for instant results

## 📊 Statistics

- **Total Distribution Lists**: 134,681
- **Categories**: 7 (General, Market, Team, Operations, Support, Management, Region)
- **Size Filters**: Small (<50), Medium (50-499), Large (500+)

## 🎯 Usage

### Search & Filter
1. Use the keyword search to find lists by email, name, or description
2. Use the type-ahead input to quickly select specific lists
3. Filter by category or size for targeted results
4. View statistics at the top of the page

### Select Lists
- **Click autocomplete suggestions** to add lists directly
- **Check boxes** in the table to select multiple lists
- **Use "Select All"** checkbox to select all lists on current page
- **Remove selections** by clicking the × on any tag

### Compose Email
1. Select one or more distribution lists
2. Click "Compose Email" button
3. Outlook Web will open with selected lists in the "To" field

## 🔧 GitHub Pages Deployment

### Option 1: Upload to Your Repository

1. Create a new repository (e.g., `dl-selector`)
2. Upload these files:
   - `index.html`
   - `all_distribution_lists.csv`
   - `DEPLOYMENT.md` (this file)
3. Go to Settings → Pages
4. Select "Deploy from a branch"
5. Choose `main` branch and `/ (root)` folder
6. Click Save
7. Your site will be live at: `https://yourusername.github.io/dl-selector/`

### Option 2: Command Line Deployment

```powershell
# Initialize git repository
git init

# Add files
git add index.html all_distribution_lists.csv DEPLOYMENT.md

# Commit
git commit -m "Initial commit: Distribution List Selector"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/yourusername/dl-selector.git

# Push to GitHub
git branch -M main
git push -u origin main
```

Then enable GitHub Pages in repository settings.

### Option 3: GitHub Desktop

1. Open GitHub Desktop
2. File → Add Local Repository
3. Select this folder
4. Publish repository to GitHub
5. Enable GitHub Pages in repository settings

## 📁 Files Required for Deployment

- **index.html**: Main application (standalone, no dependencies)
- **all_distribution_lists.csv**: Distribution list data (134,681 lists)
- **DEPLOYMENT.md**: This deployment guide

## 🔄 Updating Data

To update the distribution list catalog:

1. Run `extract_all_dls_optimized.py` to generate new CSV
2. Copy the latest CSV file to `all_distribution_lists.csv`
3. Commit and push to GitHub

Or set up automatic daily updates:

```powershell
# Run the scheduler script (Windows Task Scheduler)
.\schedule_dl_update.ps1
```

This will update the CSV every day at 5:00 AM.

## 🎨 Customization

The application uses Walmart brand colors:
- Primary Blue: #0071ce
- Dark Blue: #004c91

To customize, edit the CSS variables in `index.html`:

```css
/* Find and modify these colors */
background: #0071ce;  /* Primary brand color */
background: #004c91;  /* Dark variant */
```

## 🌐 Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## 📱 Mobile Support

Fully responsive design optimized for:
- Desktop (1920px+)
- Laptop (1366px)
- Tablet (768px)
- Mobile (375px)

## 🔒 Privacy & Security

- **No server required**: Runs entirely in the browser
- **No data collection**: No analytics or tracking
- **Static files only**: No backend or database
- **Secure**: HTTPS via GitHub Pages

## 💡 Tips

- Use **keyboard navigation** in autocomplete (↑↓ arrows, Enter to select)
- Press **Escape** to close autocomplete dropdown
- Use **Ctrl+F** for browser search within the page
- **Bookmark** the page for quick access

## 📝 Technical Details

- **Pure HTML/CSS/JavaScript**: No frameworks or dependencies
- **CSV parsing**: Custom parser handles commas in descriptions
- **Performance**: Client-side filtering of 100K+ records
- **Memory efficient**: Pagination prevents DOM overload

## 🐛 Troubleshooting

**Lists not loading?**
- Ensure `all_distribution_lists.csv` is in the same directory as `index.html`
- Check browser console (F12) for errors
- Verify CSV file is not corrupted

**Autocomplete not working?**
- Make sure JavaScript is enabled
- Try clearing browser cache
- Check for ad blockers interfering

**Email compose not working?**
- Ensure you're logged into Outlook Web
- Check popup blocker settings
- Try manually copying selected emails

## 📧 Support

For issues or feature requests, contact your IT administrator or project maintainer.

---

**Last Updated**: December 17, 2025  
**Version**: 2.0  
**Data Source**: Active Directory (134,681 distribution lists)
