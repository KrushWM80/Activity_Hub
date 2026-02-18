# Project Configuration Variables
variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "project_name" {
  description = "The human-readable name for the project"
  type        = string
}

variable "billing_account" {
  description = "The billing account ID to associate with the project"
  type        = string
}

variable "organization_id" {
  description = "The organization ID"
  type        = string
}

variable "region" {
  description = "The primary region for resources"
  type        = string
  default     = "us-central1"
}

variable "zones" {
  description = "The zones to deploy resources in"
  type        = list(string)
  default     = ["us-central1-a", "us-central1-b", "us-central1-c"]
}

# Walmart-specific Labels
variable "cost_center" {
  description = "Walmart cost center code"
  type        = string
}

variable "business_unit" {
  description = "Walmart business unit"
  type        = string
  validation {
    condition = contains([
      "grocery", "ecommerce", "supply-chain", "technology", 
      "finance", "hr", "legal", "retail", "digital"
    ], var.business_unit)
    error_message = "Business unit must be a valid Walmart business unit."
  }
}

variable "team" {
  description = "Development team name"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Environment must be development, staging, or production."
  }
}

variable "application" {
  description = "Application name"
  type        = string
}

# Network Configuration
variable "vpc_name" {
  description = "Name of the VPC network"
  type        = string
}

variable "web_subnet_cidr" {
  description = "CIDR range for web tier subnet"
  type        = string
  default     = "10.1.0.0/24"
}

variable "app_subnet_cidr" {
  description = "CIDR range for application tier subnet"
  type        = string
  default     = "10.1.1.0/24"
}

variable "data_subnet_cidr" {
  description = "CIDR range for data tier subnet"
  type        = string
  default     = "10.1.2.0/24"
}

variable "mgmt_subnet_cidr" {
  description = "CIDR range for management subnet"
  type        = string
  default     = "10.1.10.0/24"
}

# GKE Configuration
variable "gke_cluster_name" {
  description = "Name of the GKE cluster"
  type        = string
}

variable "gke_node_count" {
  description = "Initial number of nodes in the GKE cluster"
  type        = number
  default     = 3
}

variable "gke_machine_type" {
  description = "Machine type for GKE nodes"
  type        = string
  default     = "e2-standard-4"
}

variable "gke_pods_cidr" {
  description = "CIDR range for GKE pods"
  type        = string
  default     = "172.16.0.0/14"
}

variable "gke_services_cidr" {
  description = "CIDR range for GKE services"
  type        = string
  default     = "172.20.0.0/16"
}

# Database Configuration
variable "database_name" {
  description = "Name of the Cloud SQL database instance"
  type        = string
}

variable "database_tier" {
  description = "Machine type for the database instance"
  type        = string
  default     = "db-n1-standard-2"
}

variable "database_version" {
  description = "Database engine version"
  type        = string
  default     = "MYSQL_8_0"
}

# Storage Configuration
variable "storage_bucket_name" {
  description = "Name of the Cloud Storage bucket"
  type        = string
}

variable "storage_class" {
  description = "Storage class for the bucket"
  type        = string
  default     = "STANDARD"
  validation {
    condition = contains([
      "STANDARD", "NEARLINE", "COLDLINE", "ARCHIVE"
    ], var.storage_class)
    error_message = "Storage class must be STANDARD, NEARLINE, COLDLINE, or ARCHIVE."
  }
}

variable "storage_location" {
  description = "Location for the storage bucket"
  type        = string
  default     = "US-CENTRAL1"
}

# Monitoring Configuration
variable "monitoring_notification_channels" {
  description = "List of email addresses for monitoring notifications"
  type        = list(string)
  default     = []
}

# Security Configuration
variable "enable_binary_authorization" {
  description = "Enable Binary Authorization for container images"
  type        = bool
  default     = true
}

variable "enable_pod_security_policy" {
  description = "Enable Pod Security Policy for GKE"
  type        = bool
  default     = true
}

variable "enable_network_policy" {
  description = "Enable Network Policy for GKE"
  type        = bool
  default     = true
}

variable "kms_key_rotation_period" {
  description = "Period for automatic KMS key rotation"
  type        = string
  default     = "7776000s"  # 90 days
}

# Load Balancer Configuration
variable "ssl_domains" {
  description = "List of domains for SSL certificates"
  type        = list(string)
  default     = []
}

# Backup Configuration
variable "backup_retention_days" {
  description = "Number of days to retain backups"
  type        = number
  default     = 30
}

variable "log_retention_days" {
  description = "Number of days to retain logs"
  type        = number
  default     = 2555  # 7 years for compliance
}