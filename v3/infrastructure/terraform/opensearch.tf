# OpenSearch Service domain (replaces self-managed Elasticsearch in production).

resource "random_password" "opensearch" {
  length  = 24
  special = true
  override_special = "!@#$%^&*"
}

resource "aws_security_group" "opensearch" {
  name        = "${local.cluster_name}-opensearch"
  description = "OpenSearch security group"
  vpc_id      = module.vpc.vpc_id

  ingress {
    description     = "OpenSearch from EKS workers"
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [module.eks_cluster.node_security_group_id]
  }

  tags = local.common_tags
}

resource "aws_opensearch_domain" "main" {
  domain_name    = "${local.cluster_name}-search"
  engine_version = "OpenSearch_2.11"

  cluster_config {
    instance_type            = var.opensearch_instance_type
    instance_count           = 3
    zone_awareness_enabled   = true
    zone_awareness_config {
      availability_zone_count = 3
    }
    dedicated_master_enabled = true
    dedicated_master_count   = 3
    dedicated_master_type    = "m6g.large.search"
  }

  ebs_options {
    ebs_enabled = true
    volume_size = 200
    volume_type = "gp3"
  }

  vpc_options {
    subnet_ids         = module.vpc.private_subnet_ids
    security_group_ids = [aws_security_group.opensearch.id]
  }

  encrypt_at_rest {
    enabled    = true
    kms_key_id = aws_kms_key.opensearch.arn
  }

  node_to_node_encryption {
    enabled = true
  }

  domain_endpoint_options {
    enforce_https       = true
    tls_security_policy = "Policy-Min-TLS-1-2-2019-07"
  }

  advanced_security_options {
    enabled                        = true
    internal_user_database_enabled = true
    master_user_options {
      master_user_name     = "admin"
      master_user_password = random_password.opensearch.result
    }
  }

  log_publishing_options {
    cloudwatch_log_group_arn = aws_cloudwatch_log_group.opensearch.arn
    log_type                 = "INDEX_SLOW_LOGS"
    enabled                  = true
  }

  log_publishing_options {
    cloudwatch_log_group_arn = aws_cloudwatch_log_group.opensearch.arn
    log_type                 = "SEARCH_SLOW_LOGS"
    enabled                  = true
  }

  log_publishing_options {
    cloudwatch_log_group_arn = aws_cloudwatch_log_group.opensearch.arn
    log_type                 = "ES_APPLICATION_LOGS"
    enabled                  = true
  }

  auto_tune_options {
    desired_state = "ENABLED"
    rollback_on_disable = "NO_ROLLBACK"
  }

  tags = merge(local.common_tags, { Name = "${local.cluster_name}-search" })
}

resource "aws_kms_key" "opensearch" {
  description             = "OpenSearch encryption key"
  deletion_window_in_days = 30
  enable_key_rotation     = true
  tags                    = local.common_tags
}

resource "aws_cloudwatch_log_group" "opensearch" {
  name              = "/aws/opensearch/${local.cluster_name}"
  retention_in_days = 30
  tags              = local.common_tags
}

resource "aws_cloudwatch_log_resource_policy" "opensearch" {
  policy_name = "${local.cluster_name}-opensearch-log-policy"

  policy_document = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "es.amazonaws.com" }
      Action = [
        "logs:PutLogEvents",
        "logs:CreateLogStream"
      ]
      Resource = "${aws_cloudwatch_log_group.opensearch.arn}:*"
    }]
  })
}
