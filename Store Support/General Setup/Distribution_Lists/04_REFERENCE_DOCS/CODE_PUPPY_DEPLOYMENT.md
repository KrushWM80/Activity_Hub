# Code Puppy Pages Deployment - Distribution List Selector

## Step 1: Create New Page in Code Puppy

1. Go to Code Puppy Pages dashboard
2. Click "Create New Page" or "New Application"
3. Name it: **Distribution List Selector**
4. Description: **Browse and select from 134,681 Walmart distribution lists**

## Step 2: Upload Files

Upload these 2 files:
- `index.html` (main application)
- `all_distribution_lists.csv` (data file with 134,681 DLs)

## Step 3: Configure Access Control

Set AD Group permissions for who can access this tool:
- Recommended: Your team's AD group or department group
- Example: `OPS-Support-Team` or `Distribution-List-Managers`

## Step 4: HTML Code for Code Puppy Pages

Copy and paste the contents of `index.html` (already prepared and ready to use)

## Step 5: CSV Data Upload

Upload the `all_distribution_lists.csv` file to the same location as your HTML file in Code Puppy Pages.

**Important:** Ensure the CSV file is named exactly `all_distribution_lists.csv` so the HTML can reference it correctly.

## Step 6: Test Your Deployment

Once deployed, your URL will be something like:
```
https://codepuppy.walmart.com/dl-selector
```

Test the following features:
- ✅ Search functionality
- ✅ Type-ahead autocomplete
- ✅ Filters (Category, Size)
- ✅ Multi-select with checkboxes and tags
- ✅ Member counts display correctly
- ✅ "Compose Email" opens Outlook Web with selected DLs

## Optional: Set Up Auto-Update

If you want the CSV to refresh daily at 5 AM:

1. Set up the Windows scheduled task on your server:
   ```powershell
   .\schedule_dl_update.ps1
   ```

2. Configure the task to copy the updated CSV to Code Puppy Pages location after extraction

3. Or manually upload a fresh CSV weekly/monthly as needed

## Access Restrictions (Recommended)

Suggested AD Groups to grant access:
- OPS Support teams
- IT administrators
- Communication/email managers
- Business owners who manage DLs

## Features Available

Users will be able to:
- Search 134,681 distribution lists
- Filter by category and size
- Type-ahead selection for quick access
- Multi-select multiple lists
- Compose emails directly to selected DLs
- View member counts and descriptions
- Export selections (via email composition)

## Support

For issues with Code Puppy Pages deployment, contact your Code Puppy administrator or IT help desk.
