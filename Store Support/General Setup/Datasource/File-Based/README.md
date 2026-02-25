# 📄 File-Based Datasources

## Overview

Activity Hub supports importing data through files, including CSV, Excel, and JSON formats. This enables quick data uploads, manual imports, and configuration management.

---

## File-Based Data Sources Overview

| Format | Purpose | Used By | Max Size | Validation |
|---|---|---|---|---|
| **CSV** | Bulk project data import | Projects, Intake Hub | 100 MB | Column headers required |
| **Excel (.xlsx)** | Project uploads, bulk updates | Upload Projects | 100 MB | Schema validation |
| **JSON** | Configuration, API responses | All modules | 50 MB | Schema validation |
| **TXT/Logs** | Data exports, reports | General Setup | 50 MB | No strict validation |

---

## 1. 📊 CSV Files

### Purpose
Quick import of project data, employee lists, store assignments, and bulk updates.

### CSV File Fields Expected

#### Projects Import
```csv
project_id,project_title,project_status,owner_email,start_date,end_date,store_number,budget,priority
IH-001,Q1 Refresh,Active,john.doe@walmart.com,2026-01-01,2026-03-31,1497,50000,High
IH-002,Q1 Refresh,Active,jane.smith@walmart.com,2026-01-01,2026-03-31,1502,75000,Medium
```

**Required Columns**:
- `project_id` - Unique identifier
- `project_title` - Project name
- `project_status` - Active, Pending, Completed, On Hold
- `owner_email` - Project owner email

**Optional Columns**:
- `store_number` - Primary store assignment
- `start_date` - Project start (YYYY-MM-DD)
- `end_date` - Project end (YYYY-MM-DD)
- `budget` - Budget amount (numeric)
- `priority` - High, Medium, Low
- `description` - Project description

#### Store/Location Import
```csv
store_number,store_name,market,region,area_manager,phone
1497,Rogers AR,Northwest Arkansas,Central,John Doe,479-555-0123
1502,Benton AR,Northwest Arkansas,Central,Jane Smith,479-555-0124
```

#### Employee/Associate Import
```csv
associate_id,employee_name,email,store_number,job_code,job_title,store_area
12345,John Doe,john.doe@walmart.com,1497,2000,Sales Associate,Dry Grocery
12346,Jane Smith,jane.smith@walmart.com,1502,2100,Department Manager,Produce
```

### Validation Rules

```python
import pandas as pd
from datetime import datetime

class CSVValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_projects_csv(self, file_path: str) -> bool:
        """Validate projects CSV format"""
        df = pd.read_csv(file_path)
        
        # Check required columns
        required = ['project_id', 'project_title', 'project_status', 'owner_email']
        if not all(col in df.columns for col in required):
            self.errors.append(f"Missing required columns: {required}")
            return False
        
        # Validate data types
        if not df['project_id'].dtype == 'object':
            self.errors.append("project_id must be text")
        
        # Validate email format
        for email in df['email']:
            if '@' not in str(email):
                self.errors.append(f"Invalid email: {email}")
        
        # Validate status values
        valid_status = ['Active', 'Pending', 'Completed', 'On Hold']
        invalid = df[~df['project_status'].isin(valid_status)]['project_status'].unique()
        if len(invalid) > 0:
            self.errors.append(f"Invalid status values: {invalid}")
        
        return len(self.errors) == 0
    
    def get_report(self) -> dict:
        return {
            'is_valid': len(self.errors) == 0,
            'errors': self.errors,
            'warnings': self.warnings
        }
```

### Used By
- [Interface/Projects/Upload Projects/](../../../Interface/Projects/Upload%20Projects/)
- Intake Hub bulk import feature

### Example Upload
```bash
# Using the web interface:
1. Go to Projects > Upload > Browse Files
2. Select CSV file
3. Map columns to Activity Hub fields
4. Preview data
5. Click Import
```

---

## 2. 📑 Excel Files (.xlsx)

### Purpose
Professional project management with multiple sheets, formulas, and formatting.

### Supported Features
- **Multi-sheet workbooks**: Each sheet = different data type
- **Data validation**: Dropdown lists in Excel enforced
- **Formulas**: Calculated fields preserved where applicable
- **Formatting**: Color-coded rows, conditional formatting
- **Comments**: Cell comments imported as notes

### Required Sheet Structure

**Sheet 1: Projects**
```
A        B              C          D            E
------   ----------     ------     -----------  ------
ID       Title          Status     Owner        Budget
IH-001   Q1 Refresh     Active     john@wmt.com 50000
IH-002   Q2 Refresh     Pending    jane@wmt.com 75000
```

**Sheet 2: Store Assignments (Optional)**
```
A              B           C        D
-----          -----       --       ---
Project_ID     Store       Region   Market
IH-001         1497        Central  NWA
IH-001         1502        Central  NWA
IH-002         1508        South    Arkansas
```

**Sheet 3: Timeline (Optional)**
```
A          B              C           D
------     ----           -----       -----
ProjectID  Phase          StartDate   EndDate
IH-001     Planning       1/1/2026    1/15/2026
IH-001     Execution      1/16/2026   3/31/2026
```

### Validation

```python
import openpyxl
from openpyxl.utils import get_column_letter

class ExcelValidator:
    def __init__(self, file_path: str):
        self.workbook = openpyxl.load_workbook(file_path)
        self.errors = []
    
    def validate_structure(self) -> bool:
        """Check Excel has required sheets"""
        required_sheets = ['Projects']
        for sheet_name in required_sheets:
            if sheet_name not in self.workbook.sheetnames:
                self.errors.append(f"Missing required sheet: {sheet_name}")
        
        return len(self.errors) == 0
    
    def validate_projects_sheet(self) -> bool:
        """Validate Projects sheet structure"""
        ws = self.workbook['Projects']
        required_headers = ['ID', 'Title', 'Status', 'Owner', 'Budget']
        
        # Check headers in row 1
        actual_headers = [cell.value for cell in ws[1]]
        for header in required_headers:
            if header not in actual_headers:
                self.errors.append(f"Missing header: {header}")
        
        # Validate data rows
        for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=False), start=2):
            if row[0].value is None:  # Skip empty rows
                continue
            
            # Validate status is valid
            status = row[2].value
            if status not in ['Active', 'Pending', 'Completed']:
                self.errors.append(f"Row {row_idx}: Invalid status '{status}'")
        
        return len(self.errors) == 0
```

### File Size Limits
- **Max file size**: 100 MB
- **Max rows**: 1,000,000 (though performance may degrade)
- **Max sheets**: 100

### Used By
- [Interface/Projects/Upload Projects/](../../../Interface/Projects/Upload%20Projects/)
- Store Support bulk operations

---

## 3. ⚙️ JSON Configuration Files

### Purpose
Configuration management, API responses, and structured data storage.

### JSON Schemas Used

#### Role Configuration
Path: `Interface/Admin/role-configuration.json`

```json
{
    "roles": [
        {
            "id": "admin",
            "name": "Administrator",
            "description": "Full system access",
            "permissions": [
                "manage_users",
                "manage_projects",
                "view_reports",
                "manage_settings"
            ]
        },
        {
            "id": "manager",
            "name": "Manager",
            "description": "Team and project management",
            "permissions": [
                "view_team_data",
                "manage_projects",
                "view_reports"
            ]
        }
    ]
}
```

#### Access Groups
Path: `Interface/Admin/access-groups.json`

```json
{
    "groups": [
        {
            "id": "activity-hub-admins",
            "name": "Activity Hub Administrators",
            "description": "System administration team",
            "ad_group": "activity-hub-admins@walmart.com",
            "role": "admin",
            "permissions": ["*"]
        }
    ]
}
```

#### Dynamic Links
Path: `Interface/Admin/dynamic-links.json`

```json
{
    "links": [
        {
            "id": "projects",
            "label": "Projects",
            "icon": "📁",
            "target": "/projects",
            "roles": ["admin", "manager", "employee"],
            "visible": true
        }
    ]
}
```

### Validation Schema

```python
from jsonschema import validate, ValidationError

class JSONValidator:
    ROLE_SCHEMA = {
        "type": "object",
        "properties": {
            "roles": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "description": {"type": "string"},
                        "permissions": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["id", "name"]
                }
            }
        },
        "required": ["roles"]
    }
    
    @staticmethod
    def validate_roles(data: dict) -> bool:
        try:
            validate(instance=data, schema=JSONValidator.ROLE_SCHEMA)
            return True
        except ValidationError as e:
            raise ValueError(f"JSON validation failed: {e.message}")
```

### Used By
- [Interface/Admin/](../../../Interface/Admin/)
- Configuration management
- API response serialization

---

## 🔄 File Import Process

### Step-by-Step Workflow

```
1. Upload File
   ↓
2. Validate File Type & Size
   ↓
3. Parse File Contents
   ↓
4. Validate Data Schema
   ↓
5. Check for Duplicates
   ↓
6. Transform Data (if needed)
   ↓
7. Load into System
   ↓
8. Generate Import Report
```

### Python Import Handler

```python
import pandas as pd
import json
from pathlib import Path

class FileImportHandler:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.file_type = self.file_path.suffix.lower()
        self.data = None
        self.errors = []
    
    def import_file(self) -> dict:
        """Main import process"""
        try:
            # 1. Validate file
            self._validate_file()
            
            # 2. Parse file
            self._parse_file()
            
            # 3. Validate data
            self._validate_data()
            
            # 4. Load data
            self._load_data()
            
            return {
                'success': True,
                'records_imported': len(self.data),
                'errors': []
            }
        except Exception as e:
            return {
                'success': False,
                'records_imported': 0,
                'errors': [str(e)]
            }
    
    def _validate_file(self):
        """Check file exists and is valid type"""
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
        
        if self.file_type not in ['.csv', '.xlsx', '.json', '.txt']:
            raise ValueError(f"Unsupported file type: {self.file_type}")
        
        if self.file_path.stat().st_size > 100 * 1024 * 1024:  # 100 MB
            raise ValueError("File size exceeds 100 MB limit")
    
    def _parse_file(self):
        """Parse file based on type"""
        if self.file_type == '.csv':
            self.data = pd.read_csv(self.file_path)
        elif self.file_type == '.xlsx':
            self.data = pd.read_excel(self.file_path)
        elif self.file_type == '.json':
            with open(self.file_path) as f:
                self.data = json.load(f)
    
    def _validate_data(self):
        """Validate data content"""
        # Implement data validation logic
        pass
    
    def _load_data(self):
        """Load data into system"""
        # Implement data loading logic
        pass
```

---

## ❌ Common Issues & Solutions

### Issue 1: "File Format Not Supported"
```
Cause: Unsupported file type or extension
Solution:
1. Convert file to CSV, XLSX, or JSON
2. Check file extension is correct
3. Verify not corrupt/zipped
```

### Issue 2: "Column Headers Missing"
```
Cause: CSV lacks required header row
Solution:
1. Ensure first row contains column names
2. Match required column names exactly
3. No spaces or special characters in headers
```

### Issue 3: "Data Validation Failed"
```
Cause: Invalid data format or values
Solution:
1. Check date format (use YYYY-MM-DD)
2. Ensure emails are valid format
3. Verify required fields are populated
4. Check for duplicates
```

### Issue 4: "File Size Too Large"
```
Cause: File exceeds 100 MB limit
Solution:
1. Split into multiple files
2. Remove unnecessary columns
3. Use database import instead
```

---

## 🛠️ Templates

### CSV Template: Projects Import
```csv
project_id,project_title,project_status,owner_email,start_date,end_date,store_number,budget,priority
[ID],[Title],[Status],[Email],[Start],[End],[Store],[Budget],[Priority]
,,Active,,YYYY-MM-DD,YYYY-MM-DD,,000000,High|Medium|Low
```

### Excel Template Structure
See: [Excel templates folder](./templates/)

### JSON Template: Configuration
```json
{
    "version": "1.0",
    "last_updated": "2026-02-25T10:00:00Z",
    "data": []
}
```

---

## 📊 File Import Statistics

### Current Volumes
- **CSV imports/month**: ~250
- **Excel uploads/month**: ~400  
- **JSON configs**: 50+ configuration files
- **Average file size**: 2.5 MB

### Popular Import Scenarios
1. **Bulk Project Uploads**: 60% of imports
2. **Store Assignment Updates**: 20% of imports
3. **Employee/Associate Data**: 15% of imports
4. **Reporting Exports**: 5% of imports

---

## 📞 Support

- **File Format Help**: Check format in relevant datasource README
- **Validation Issues**: Review data against templates
- **Upload Errors**: Check file size, type, and content
- **Troubleshooting**: See Common Issues section above

