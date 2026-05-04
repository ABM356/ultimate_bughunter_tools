variable "project" {
  description = "Project identifier used as a prefix for all resources"
  type        = string
  default     = "hopeup"
}

variable "environment" {
  description = "Deployment environment (dev|staging|production)"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "environment must be one of: dev, staging, production"
  }
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "domain" {
  description = "Public domain for the platform (e.g., hopeup.example.com)"
  type        = string
  default     = "hopeup.example.com"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "k8s_version" {
  description = "Kubernetes version"
  type        = string
  default     = "1.29"
}

variable "rds_instance_class" {
  description = "RDS instance type"
  type        = string
  default     = "db.r6g.large"
}

variable "redis_node_type" {
  description = "ElastiCache node type"
  type        = string
  default     = "cache.r6g.large"
}

variable "opensearch_instance_type" {
  description = "OpenSearch data node instance type"
  type        = string
  default     = "r6g.large.search"
}

variable "alert_email" {
  description = "Email for CloudWatch alarms"
  type        = string
  default     = "platform-alerts@hopeup.example.com"
}
