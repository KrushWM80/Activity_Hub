# Terraform Configuration Templates

This directory contains Terraform templates for setting up GCP resources following Walmart's standards and best practices.

## Templates Available

1. **`project-setup.tf`** - Basic project setup with IAM and APIs
2. **`networking.tf`** - VPC, subnets, and firewall configuration
3. **`security.tf`** - Security policies, KMS, and compliance settings
4. **`monitoring.tf`** - Cloud Monitoring and logging setup
5. **`compute.tf`** - Compute instances and managed instance groups
6. **`storage.tf`** - Cloud Storage buckets and lifecycle policies
7. **`variables.tf`** - Variable definitions
8. **`outputs.tf`** - Output definitions
9. **`terraform.tfvars.example`** - Example variable values

## Usage Instructions

1. Copy the relevant template files to your project directory
2. Rename `terraform.tfvars.example` to `terraform.tfvars`
3. Update the variables in `terraform.tfvars` with your project-specific values
4. Review and customize the templates based on your requirements
5. Run `terraform plan` to review the changes
6. Run `terraform apply` to create the resources

## Prerequisites

- Terraform >= 1.0
- Google Cloud SDK installed and authenticated
- Required GCP APIs enabled
- Appropriate IAM permissions

## Best Practices

- Always run `terraform plan` before `terraform apply`
- Use remote state storage (Cloud Storage bucket)
- Version control all Terraform configurations
- Use meaningful resource names and labels
- Follow Walmart's naming conventions