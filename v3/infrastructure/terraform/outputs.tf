output "cluster_name" {
  description = "EKS cluster name"
  value       = module.eks_cluster.cluster_name
}

output "cluster_endpoint" {
  description = "EKS API endpoint"
  value       = module.eks_cluster.cluster_endpoint
}

output "cluster_oidc_provider_arn" {
  description = "OIDC provider ARN for IRSA"
  value       = module.eks_cluster.oidc_provider_arn
}

output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "private_subnet_ids" {
  description = "Private subnet IDs"
  value       = module.vpc.private_subnet_ids
}

output "rds_endpoint" {
  description = "RDS endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = false
}

output "rds_password" {
  description = "RDS master password"
  value       = random_password.rds.result
  sensitive   = true
}

output "redis_primary_endpoint" {
  description = "ElastiCache primary endpoint"
  value       = aws_elasticache_replication_group.redis.primary_endpoint_address
}

output "redis_auth_token" {
  description = "ElastiCache AUTH token"
  value       = random_password.redis.result
  sensitive   = true
}

output "opensearch_endpoint" {
  description = "OpenSearch domain endpoint"
  value       = "https://${aws_opensearch_domain.main.endpoint}"
}

output "opensearch_password" {
  description = "OpenSearch master password"
  value       = random_password.opensearch.result
  sensitive   = true
}

output "s3_reports_bucket" {
  description = "Reports bucket name"
  value       = aws_s3_bucket.reports.id
}

output "s3_scans_bucket" {
  description = "Scans bucket name"
  value       = aws_s3_bucket.scans.id
}

output "backend_iam_role_arn" {
  description = "IAM role ARN for backend pods (IRSA)"
  value       = aws_iam_role.backend.arn
}

output "kubeconfig_command" {
  description = "Command to update kubeconfig"
  value       = "aws eks update-kubeconfig --region ${var.aws_region} --name ${module.eks_cluster.cluster_name}"
}
