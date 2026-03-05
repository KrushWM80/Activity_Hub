# Complete System Setup Requirements

## Operating System & Core
- Windows, Mac, or Linux OS
- Git version control system
- Internet connection (required for BigQuery and cloud services)

## Python (for AMP & Pricing applications)
- Python 3.8+
- pip package manager
- **Required Packages**:
  - pandas >= 1.5.0
  - numpy >= 1.21.0
  - google-cloud-bigquery >= 3.0.0
  - pyarrow >= 8.0.0
  - openpyxl >= 3.0.0
  - sqlalchemy >= 1.4.0
  - db-dtypes >= 1.0.0
  - matplotlib >= 3.5.0
  - seaborn >= 0.11.0
  - plotly >= 5.0.0
  - folium >= 0.12.0
  - geopandas >= 0.10.0
  - xlsxwriter >= 3.0.0
  - fastparquet >= 0.8.0
  - textract >= 2.5.0

## Node.js (for Evaluation System & Refresh Guide)
- Node.js 18+
- npm 8+

### Evaluation System Dependencies
- express ^4.18.2
- express-fileupload ^1.5.0
- cors ^2.8.5
- csv-parser ^3.0.0
- xlsx ^0.18.5
- dotenv ^16.3.1
- handlebars ^4.7.7
- nodemon ^3.0.2 (dev only)

### Refresh Guide Dependencies
- Backend:
  - @google-cloud/bigquery ^8.1.1
  - express
  - dotenv ^17.2.3
  - mammoth ^1.11.0
  - textract ^2.5.0
  - xlsx ^0.18.5
- Frontend:
  - React 18+
  - TypeScript
  - Material-UI v5
  - i18next (internationalization)
- Development:
  - concurrently ^8.2.2

## Database
- PostgreSQL (required for Refresh Guide)

## External Services & Cloud Access
- **Google Cloud Project Access**
  - BigQuery access to `athena-gateway-prod.store_refresh.store_refresh_data`
  - BigQuery access to `wmt-assetprotection-prod.Store_Support_Dev.Store Cur Data`
  - Service account credentials file (JSON) for authentication
- **Walmart GitHub Access**
  - gecgithub01.walmart.com repository access

## Browser Requirements
- Chrome, Firefox, Safari, or Edge (latest versions)

## Directory Structure
Each application needs the following local directories:
- output/
- logs/
- config/
- temp/
- data/ (Refresh Guide)

## Environment Configuration Files
Create `.env` files with:
- `PORT` (application port)
- `DATABASE_URL` (PostgreSQL connection string)
- `BIGQUERY_PROJECT_ID` (Google Cloud project ID)
- `BIGQUERY_CREDENTIALS_PATH` (path to service account JSON)
- API keys and credentials (application-specific)

## Data Files (Not in Git - Must Regenerate)
- Refresh Guide large datasets (~320+ MB):
  - `data/EmbeddedData2/reviewAssignments.json`
  - `data/business_overview_/reviewAssignments.json`
  - Generated via BigQuery extraction scripts

## Authentication
- JWT-based authentication (Refresh Guide)
- 5 role-based access control levels
- Google Cloud service account credentials

## Optional/Development Tools
- Docker (for containerized deployment)
- Nodemon (for Node.js auto-reload during development)

## Storage & Memory Requirements
- Minimum 4GB RAM recommended
- 500MB+ disk space for data files and dependencies
- SSD recommended for faster performance

## Credentials (Contact Admin For)
- Google Cloud BigQuery service account JSON file
- PostgreSQL database credentials
- Walmart GitHub SSH key or personal access token
