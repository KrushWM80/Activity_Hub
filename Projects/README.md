# IH Project Data Management Interface

A comprehensive HTML-based interface for managing records from the `wmt-assetprotection-prod.Store_Support.IH_Project_Data` data source. This application provides full CRUD (Create, Read, Update, Delete) functionality with a responsive, user-friendly interface.

## Features

### 🚀 Core Functionality
- **Create New Records**: Add new IH project records with comprehensive data fields
- **Search & Filter**: Advanced search capabilities with multiple filter options
- **Update Records**: Edit existing records with pre-populated forms
- **Delete Records**: Secure deletion with confirmation prompts
- **View All Records**: Tabular view of all records with sorting capabilities
- **Data Export**: Export records to CSV format for external use

### 🎨 User Interface
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Tabbed Navigation**: Organized interface with clear navigation
- **Status Indicators**: Visual badges for status and priority levels
- **Modal Dialogs**: Clean update forms in overlay modals
- **Real-time Feedback**: Success/error messages for all operations

### 🔧 Technical Features
- **Local Storage**: Data persistence using browser local storage
- **Form Validation**: Client-side validation with error messaging
- **Sample Data**: Pre-loaded demo data for testing
- **Debounced Search**: Performance-optimized search functionality
- **CSV Export**: Full data export capabilities

## Project Structure

```
IH-Project-Data-Interface/
├── index.html          # Main application interface
├── styles.css          # Responsive CSS styling
├── script.js           # JavaScript functionality
├── README.md           # This documentation
└── .github/
    └── copilot-instructions.md  # Project configuration
```

## Data Fields

The interface manages the following data fields for each IH Project record:

### Required Fields
- **Project ID**: Unique identifier for the project
- **Project Name**: Descriptive name for the project

### Optional Fields
- **Store Number**: Associated store location
- **Region**: Geographic region (North, South, East, West, Central)
- **District**: District designation
- **Market**: Market classification
- **Project Type**: Investigation, Prevention, Training, Audit, Compliance
- **Priority Level**: Low, Medium, High, Critical
- **Status**: Planning, In Progress, On Hold, Completed, Cancelled
- **Assigned To**: Person responsible for the project
- **Start Date**: Project start date
- **Target Completion Date**: Expected completion date
- **Project Description**: Detailed project description
- **Additional Notes**: Supplementary information

### Metadata (Auto-generated)
- **Created Date**: Timestamp of record creation
- **Last Modified**: Timestamp of last update
- **Record ID**: System-generated unique identifier

## Getting Started

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- No server setup required - runs entirely in the browser

### Installation
1. Download or clone all project files
2. Ensure all files are in the same directory
3. Open `index.html` in a web browser

### First Time Setup
1. The application will automatically load sample data on first use
2. Navigate between tabs to explore functionality
3. Create, edit, or delete records as needed
4. Data is automatically saved to browser storage

## Usage Guide

### Creating New Records
1. Click the **"Create New Record"** tab
2. Fill in the required fields (Project ID and Project Name)
3. Complete optional fields as needed
4. Click **"Create Record"** to save
5. Form will reset and show success message

### Searching and Updating Records
1. Click the **"Search & Update Records"** tab
2. Use search filters to find specific records:
   - Project ID search
   - Project Name search
   - Store Number search
   - Status filter
3. Click **"Search"** to filter results
4. Click **"Edit"** on any record to update it
5. Make changes in the modal form and click **"Update Record"**

### Viewing All Records
1. Click the **"View All Records"** tab
2. Browse all records in a sortable table
3. Use **"Refresh Data"** to reload the table
4. Click **"Export to CSV"** to download all data
5. Use **"Edit"** or **"Delete"** buttons for individual records

### Data Export
1. Navigate to the **"View All Records"** tab
2. Click **"Export to CSV"**
3. File will download automatically with timestamp
4. Contains all fields and metadata

## Customization

### Adding New Fields
1. Update the HTML form in `index.html`
2. Add corresponding CSS styles in `styles.css`
3. Update JavaScript validation and handling in `script.js`

### Modifying Field Options
1. Edit dropdown options in the HTML forms
2. Update validation logic in the JavaScript
3. Adjust CSS classes for new status types

### Styling Changes
1. Modify color scheme in `styles.css`
2. Update the CSS custom properties for consistent theming
3. Adjust responsive breakpoints as needed

## Browser Compatibility

### Supported Browsers
- Chrome 60+
- Firefox 60+
- Safari 12+
- Edge 79+

### Features Used
- ES6 Classes and Arrow Functions
- LocalStorage API
- CSS Grid and Flexbox
- Modern DOM APIs

## Data Storage

### Local Storage
- Data is stored in browser's localStorage
- Key: `ihProjectData`
- Format: JSON array of objects
- Automatic backup on each operation

### Data Persistence
- Data persists between browser sessions
- Clearing browser data will remove stored records
- No server-side storage required

## Performance Considerations

### Optimization Features
- Debounced search (300ms delay)
- Lazy loading for large datasets
- Efficient DOM updates
- Minimal CSS and JavaScript footprint

### Scalability
- Optimized for up to 1000 records
- Consider server-side storage for larger datasets
- Search performance degrades with very large datasets

## Security Considerations

### Data Protection
- All data stored locally in browser
- No server transmission by default
- User data never leaves the local machine
- XSS protection through proper input handling

### Input Validation
- Client-side validation for all inputs
- SQL injection protection (no database queries)
- Proper data sanitization for CSV export

## Troubleshooting

### Common Issues

**Data Not Saving**
- Check if localStorage is enabled in browser
- Verify browser supports localStorage API
- Check for browser storage quotas

**Interface Not Loading**
- Ensure all files are in same directory
- Check browser console for JavaScript errors
- Verify file paths are correct

**Search Not Working**
- Check for JavaScript errors in console
- Verify search inputs are properly formatted
- Try clearing browser cache

**Export Failing**
- Check if browser supports Blob API
- Verify popup blockers aren't preventing download
- Ensure browser has write permissions

### Browser Console
Use browser developer tools (F12) to:
- Check for JavaScript errors
- Monitor localStorage contents
- Debug search functionality
- Verify form submissions

## Development

### Code Structure
- **HTML**: Semantic markup with accessibility features
- **CSS**: Mobile-first responsive design with CSS Grid
- **JavaScript**: ES6 classes with modular architecture

### Key Classes and Functions
- `IHProjectDataManager`: Main application class
- `loadRecords()`: Data persistence management
- `validateRecord()`: Input validation
- `searchRecords()`: Search and filtering logic
- `exportData()`: CSV export functionality

## Contributing

### Code Standards
- Use ES6+ JavaScript features
- Follow semantic HTML practices
- Maintain responsive CSS design
- Include comprehensive comments

### Testing
- Test on multiple browsers
- Verify mobile responsiveness
- Validate form submissions
- Test data export functionality

## License

This project is designed for internal use with Walmart Asset Protection data systems. Please ensure compliance with all corporate data handling policies.

## Support

For technical issues or feature requests, please contact the development team or create an issue in the project repository.

---

**Version**: 1.0.0  
**Last Updated**: October 28, 2025  
**Compatibility**: Modern browsers with ES6 support