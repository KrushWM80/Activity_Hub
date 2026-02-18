# Terraform configuration for GCP project setup
# This template creates a new GCP project with basic configuration

terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 4.0"
    }
  }
  
  # Configure remote state storage
  backend "gcs" {
    bucket = "wmt-terraform-state"
    prefix = "projects"
  }
}

# Configure the Google Cloud Provider
provider "google" {
  project = var.project_id
  region  = var.region
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}

# Local values for consistent labeling
locals {
  common_labels = {
    cost-center    = var.cost_center
    business-unit  = var.business_unit
    team          = var.team
    environment   = var.environment
    application   = var.application
    managed-by    = "terraform"
    created-date  = formatdate("YYYY-MM-DD", timestamp())
  }
}

# Create the project
resource "google_project" "main" {
  name            = var.project_name
  project_id      = var.project_id
  billing_account = var.billing_account
  org_id          = var.organization_id
  
  labels = local.common_labels
}

# Enable required APIs
resource "google_project_service" "required_apis" {
  for_each = toset([
    "compute.googleapis.com",
    "container.googleapis.com",
    "cloudsql.googleapis.com",
    "storage.googleapis.com",
    "cloudkms.googleapis.com",
    "monitoring.googleapis.com",
    "logging.googleapis.com",
    "cloudasset.googleapis.com",
    "securitycenter.googleapis.com",
    "binaryauthorization.googleapis.com",
    "dns.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "iam.googleapis.com",
    "serviceusage.googleapis.com",
    "billingbudgets.googleapis.com"
  ])
  
  project = google_project.main.project_id
  service = each.value
  
  disable_dependent_services = false
  disable_on_destroy        = false
}

# Create service accounts
resource "google_service_account" "application" {
  account_id   = "${var.application}-app-sa"
  display_name = "Application Service Account for ${var.application}"
  description  = "Service account for running ${var.application} application"
  project      = google_project.main.project_id
  
  depends_on = [google_project_service.required_apis]
}

resource "google_service_account" "cicd" {
  account_id   = "${var.application}-cicd-sa"
  display_name = "CI/CD Service Account for ${var.application}"
  description  = "Service account for CI/CD pipelines"
  project      = google_project.main.project_id
  
  depends_on = [google_project_service.required_apis]
}

resource "google_service_account" "monitoring" {
  account_id   = "${var.application}-monitor-sa"
  display_name = "Monitoring Service Account for ${var.application}"
  description  = "Service account for monitoring and logging"
  project      = google_project.main.project_id
  
  depends_on = [google_project_service.required_apis]
}

# Custom IAM roles
resource "google_project_iam_custom_role" "developer_role" {
  role_id     = "walmart.developer"
  title       = "Walmart Developer Role"
  description = "Custom role for Walmart developers with limited permissions"
  project     = google_project.main.project_id
  
  permissions = [
    "compute.instances.get",
    "compute.instances.list",
    "compute.instanceGroups.get",
    "compute.instanceGroups.list",
    "logging.entries.list",
    "logging.logs.list",
    "monitoring.dashboards.get",
    "monitoring.dashboards.list",
    "storage.objects.get",
    "storage.objects.list",
    "container.clusters.get",
    "container.pods.get",
    "container.pods.list"
  ]
  
  depends_on = [google_project_service.required_apis]
}

resource "google_project_iam_custom_role" "devops_role" {
  role_id     = "walmart.devops"
  title       = "Walmart DevOps Role"
  description = "Custom role for Walmart DevOps engineers"
  project     = google_project.main.project_id
  
  permissions = [
    "compute.*",
    "container.*",
    "storage.*",
    "logging.*",
    "monitoring.*",
    "iam.serviceAccounts.actAs",
    "iam.serviceAccounts.get",
    "iam.serviceAccounts.list",
    "resourcemanager.projects.get"
  ]
  
  depends_on = [google_project_service.required_apis]
}

# IAM bindings for service accounts
resource "google_project_iam_member" "application_sa_bindings" {
  for_each = toset([
    "roles/storage.objectViewer",
    "roles/cloudsql.client",
    "roles/logging.logWriter",
    "roles/monitoring.metricWriter"
  ])
  
  project = google_project.main.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.application.email}"
}

resource "google_project_iam_member" "cicd_sa_bindings" {
  for_each = toset([
    "roles/container.developer",
    "roles/storage.admin",
    "roles/cloudbuild.builds.editor",
    "roles/source.repos.admin"
  ])
  
  project = google_project.main.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.cicd.email}"
}

resource "google_project_iam_member" "monitoring_sa_bindings" {
  for_each = toset([
    "roles/monitoring.editor",
    "roles/logging.admin",
    "roles/errorreporting.writer"
  ])
  
  project = google_project.main.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.monitoring.email}"
}

# Organization policies for Walmart compliance
resource "google_org_policy_policy" "restrict_external_ip" {
  name   = "projects/${google_project.main.project_id}/policies/compute.vmExternalIpAccess"
  parent = "projects/${google_project.main.project_id}"
  
  spec {
    rules {
      deny_all = "TRUE"
    }
  }
  
  depends_on = [google_project_service.required_apis]
}

resource "google_org_policy_policy" "require_os_login" {
  name   = "projects/${google_project.main.project_id}/policies/compute.requireOsLogin"
  parent = "projects/${google_project.main.project_id}"
  
  spec {
    rules {
      enforce = "TRUE"
    }
  }
  
  depends_on = [google_project_service.required_apis]
}

resource "google_org_policy_policy" "uniform_bucket_access" {
  name   = "projects/${google_project.main.project_id}/policies/storage.uniformBucketLevelAccess"
  parent = "projects/${google_project.main.project_id}"
  
  spec {
    rules {
      enforce = "TRUE"
    }
  }
  
  depends_on = [google_project_service.required_apis]
}

resource "google_org_policy_policy" "restrict_locations" {
  name   = "projects/${google_project.main.project_id}/policies/gcp.resourceLocations"
  parent = "projects/${google_project.main.project_id}"
  
  spec {
    rules {
      condition {
        expression = "true"
      }
      values {
        allowed_values = [
          "us-central1",
          "us-east1",
          "us-west1"
        ]
      }
    }
  }
  
  depends_on = [google_project_service.required_apis]
}

# Budget alerts
resource "google_billing_budget" "project_budget" {
  billing_account = var.billing_account
  display_name    = "${var.project_name} Budget"
  
  budget_filter {
    projects = ["projects/${google_project.main.number}"]
  }
  
  amount {
    specified_amount {
      currency_code = "USD"
      units         = "5000"  # $5,000 default budget
    }
  }
  
  threshold_rules {
    threshold_percent = 0.5
    spend_basis      = "CURRENT_SPEND"
  }
  
  threshold_rules {
    threshold_percent = 0.8
    spend_basis      = "CURRENT_SPEND"
  }
  
  threshold_rules {
    threshold_percent = 1.0
    spend_basis      = "CURRENT_SPEND"
  }
  
  all_updates_rule {
    monitoring_notification_channels = var.monitoring_notification_channels
    disable_default_iam_recipients   = true
  }
}

# Audit logging configuration
resource "google_project_iam_audit_config" "audit_config" {
  project = google_project.main.project_id
  service = "allServices"
  
  audit_log_config {
    log_type = "ADMIN_READ"
  }
  
  audit_log_config {
    log_type = "DATA_WRITE"
  }
  
  audit_log_config {
    log_type = "DATA_READ"
  }
}