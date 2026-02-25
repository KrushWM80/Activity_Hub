# BigQuery Integration Reference

## Overview
This document provides general, production-ready guidance for integrating Google BigQuery with any Walmart project. It covers authentication, connection setup, best practices, and includes Intake Hub as an example implementation.

---

## 1. End-to-End Architecture Patterns
- **Frontend:** HTML5/JS dashboard (fetch API or AJAX)
- **Backend:** Python (FastAPI, Flask, Django, etc.) or Node.js (Express)
- **Data Source:** Google BigQuery (service account or gcloud authentication)
- **Authentication:** gcloud CLI for development, service account JSON for production
- **Status:** Real-time data access, secure backend proxy recommended

---

## 2. BigQuery Connection & Authentication
- Install Google Cloud SDK and authenticate:
  - `gcloud auth login` (for user authentication)
  - `gcloud config set project <your-project-id>`
  - `gcloud auth application-default login` (for local development)
- For production, use a service account JSON key and set `GOOGLE_APPLICATION_CREDENTIALS` environment variable.
- Example .env:
  ```env
  GCP_PROJECT_ID=wmt-assetprotection-prod
  GOOGLE_APPLICATION_CREDENTIALS=  # Leave empty to use gcloud credentials
  BIGQUERY_DATASET=Store_Support_Dev
  BIGQUERY_TABLE=<your-table-name>
  ```
- Use the `google-cloud-bigquery` Python package or BigQuery REST API for data access.

---

## 3. Dependency Mapping
- Map all frontend, backend, and data dependencies for your project.
- Document package versions, file relationships, and environment variables.
- Use Intake Hub's DEPENDENCY_MAPPING.md as a template for detailed mapping.

---

## 4. Best Practices
- Always verify authentication before deploying
- Use a backend API as a secure proxy for BigQuery (never expose credentials to frontend)
- Document all environment variables and connection steps
- Keep dependency mapping up to date
- Test in development before production deployment
- Monitor query costs and set up budget alerts

---

## 5. Example: Intake Hub Projects in Stores
- Intake Hub uses FastAPI backend, Google BigQuery, and secure authentication
- Real-time data is served via backend API endpoints
- All endpoints verified with real data (Feb 2026)
- See KNOWLEDGE_BASE.md, BIGQUERY_SETUP.md, and DEPENDENCY_MAPPING.md in Intake Hub for implementation details

---

**For more, see the other documentation in this folder. Use these patterns to ensure your BigQuery project is secure, maintainable, and production-ready.**
- Keep dependency mapping up to date

---

## 5. References
- Intake Hub KNOWLEDGE_BASE.md: System overview, architecture, and status
- Intake Hub BIGQUERY_SETUP.md: Step-by-step GCP and BigQuery setup
- Intake Hub DEPENDENCY_MAPPING.md: Example for mapping all dependencies

---

**For more, see the Intake Hub ProjectsinStores folder. Use these patterns to ensure your BigQuery project is secure, maintainable, and production-ready.**
