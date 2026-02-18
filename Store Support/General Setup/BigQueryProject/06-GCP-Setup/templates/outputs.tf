# Project Information
output "project_id" {
  description = "The project ID"
  value       = google_project.main.project_id
}

output "project_number" {
  description = "The project number"
  value       = google_project.main.number
}

output "project_name" {
  description = "The project name"
  value       = google_project.main.name
}

# Service Account Information
output "application_service_account_email" {
  description = "Email address of the application service account"
  value       = google_service_account.application.email
}

output "cicd_service_account_email" {
  description = "Email address of the CI/CD service account"
  value       = google_service_account.cicd.email
}

output "monitoring_service_account_email" {
  description = "Email address of the monitoring service account"
  value       = google_service_account.monitoring.email
}

# Network Information
output "vpc_name" {
  description = "Name of the VPC network"
  value       = google_compute_network.main.name
}

output "vpc_self_link" {
  description = "Self-link of the VPC network"
  value       = google_compute_network.main.self_link
}

output "web_subnet_name" {
  description = "Name of the web tier subnet"
  value       = google_compute_subnetwork.web_tier.name
}

output "web_subnet_cidr" {
  description = "CIDR range of the web tier subnet"
  value       = google_compute_subnetwork.web_tier.ip_cidr_range
}

output "app_subnet_name" {
  description = "Name of the application tier subnet"
  value       = google_compute_subnetwork.app_tier.name
}

output "app_subnet_cidr" {
  description = "CIDR range of the application tier subnet"
  value       = google_compute_subnetwork.app_tier.ip_cidr_range
}

output "data_subnet_name" {
  description = "Name of the data tier subnet"
  value       = google_compute_subnetwork.data_tier.name
}

output "data_subnet_cidr" {
  description = "CIDR range of the data tier subnet"
  value       = google_compute_subnetwork.data_tier.ip_cidr_range
}

# Security Information
output "kms_key_ring_name" {
  description = "Name of the KMS key ring"
  value       = google_kms_key_ring.main.name
}

output "kms_crypto_key_name" {
  description = "Name of the KMS crypto key"
  value       = google_kms_crypto_key.main.name
}

# Database Information
output "database_instance_name" {
  description = "Name of the Cloud SQL instance"
  value       = google_sql_database_instance.main.name
}

output "database_connection_name" {
  description = "Connection name of the Cloud SQL instance"
  value       = google_sql_database_instance.main.connection_name
}

output "database_private_ip" {
  description = "Private IP address of the database instance"
  value       = google_sql_database_instance.main.private_ip_address
}

# Storage Information
output "storage_bucket_name" {
  description = "Name of the Cloud Storage bucket"
  value       = google_storage_bucket.main.name
}

output "storage_bucket_url" {
  description = "URL of the Cloud Storage bucket"
  value       = google_storage_bucket.main.url
}

# GKE Information
output "gke_cluster_name" {
  description = "Name of the GKE cluster"
  value       = google_container_cluster.main.name
}

output "gke_cluster_endpoint" {
  description = "Endpoint of the GKE cluster"
  value       = google_container_cluster.main.endpoint
  sensitive   = true
}

output "gke_cluster_ca_certificate" {
  description = "CA certificate of the GKE cluster"
  value       = google_container_cluster.main.master_auth[0].cluster_ca_certificate
  sensitive   = true
}

# Load Balancer Information
output "load_balancer_ip" {
  description = "IP address of the global load balancer"
  value       = google_compute_global_address.main.address
}

output "ssl_certificate_name" {
  description = "Name of the SSL certificate"
  value       = google_compute_managed_ssl_certificate.main.name
}

# Monitoring Information
output "monitoring_workspace_name" {
  description = "Name of the monitoring workspace"
  value       = google_monitoring_workspace.main.name
}

# Budget Information
output "budget_name" {
  description = "Name of the billing budget"
  value       = google_billing_budget.project_budget.display_name
}

# DNS Information
output "private_dns_zone_name" {
  description = "Name of the private DNS zone"
  value       = google_dns_managed_zone.private.name
}

output "private_dns_zone_dns_name" {
  description = "DNS name of the private DNS zone"
  value       = google_dns_managed_zone.private.dns_name
}

# Useful commands for connecting to resources
output "gke_get_credentials_command" {
  description = "Command to get GKE credentials"
  value       = "gcloud container clusters get-credentials ${google_container_cluster.main.name} --region ${var.region} --project ${var.project_id}"
}

output "database_connection_command" {
  description = "Command to connect to the database via proxy"
  value       = "cloud_sql_proxy -instances=${google_sql_database_instance.main.connection_name}=tcp:3306"
}

# Resource URLs for easy access
output "console_urls" {
  description = "Useful Google Cloud Console URLs"
  value = {
    project_dashboard = "https://console.cloud.google.com/home/dashboard?project=${var.project_id}"
    compute_instances = "https://console.cloud.google.com/compute/instances?project=${var.project_id}"
    gke_clusters     = "https://console.cloud.google.com/kubernetes/list?project=${var.project_id}"
    storage_buckets  = "https://console.cloud.google.com/storage/browser?project=${var.project_id}"
    sql_instances    = "https://console.cloud.google.com/sql/instances?project=${var.project_id}"
    monitoring       = "https://console.cloud.google.com/monitoring?project=${var.project_id}"
    logging          = "https://console.cloud.google.com/logs?project=${var.project_id}"
  }
}