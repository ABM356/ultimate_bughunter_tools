# Managed PostgreSQL via RDS Multi-AZ.
# For higher scale or read-replicas, switch to Aurora (commented below).

resource "random_password" "rds" {
  length  = 32
  special = true
  # RDS forbids /, @, ", and space
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "aws_db_subnet_group" "rds" {
  name       = "${local.cluster_name}-rds"
  subnet_ids = module.vpc.private_subnet_ids
  tags       = local.common_tags
}

resource "aws_security_group" "rds" {
  name        = "${local.cluster_name}-rds"
  description = "RDS security group"
  vpc_id      = module.vpc.vpc_id

  ingress {
    description     = "Postgres from EKS workers"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [module.eks_cluster.node_security_group_id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = local.common_tags
}

resource "aws_db_parameter_group" "postgres16" {
  name   = "${local.cluster_name}-pg16"
  family = "postgres16"

  parameter {
    name  = "log_statement"
    value = "ddl"
  }
  parameter {
    name  = "log_min_duration_statement"
    value = "1000"  # log slow (>1s) queries
  }
  parameter {
    name  = "shared_preload_libraries"
    value = "pg_stat_statements"
    apply_method = "pending-reboot"
  }
}

resource "aws_db_instance" "main" {
  identifier            = "${local.cluster_name}-postgres"
  engine                = "postgres"
  engine_version        = "16.2"
  instance_class        = var.rds_instance_class
  allocated_storage     = 100
  max_allocated_storage = 1000
  storage_type          = "gp3"
  storage_encrypted     = true
  kms_key_id            = aws_kms_key.rds.arn

  db_name  = "hopeup"
  username = "hopeup"
  password = random_password.rds.result
  port     = 5432

  multi_az               = true
  publicly_accessible    = false
  db_subnet_group_name   = aws_db_subnet_group.rds.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  parameter_group_name   = aws_db_parameter_group.postgres16.name

  backup_retention_period = 30
  backup_window           = "03:00-04:00"
  maintenance_window      = "sun:04:00-sun:05:00"
  copy_tags_to_snapshot   = true
  deletion_protection     = var.environment == "production"
  skip_final_snapshot     = var.environment != "production"
  final_snapshot_identifier = "${local.cluster_name}-postgres-final-${formatdate("YYYY-MM-DD", timestamp())}"

  performance_insights_enabled    = true
  performance_insights_retention_period = 7
  monitoring_interval = 60
  monitoring_role_arn = aws_iam_role.rds_monitoring.arn

  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]

  tags = merge(local.common_tags, { Name = "${local.cluster_name}-postgres" })
}

resource "aws_kms_key" "rds" {
  description             = "RDS encryption key"
  deletion_window_in_days = 30
  enable_key_rotation     = true
  tags                    = local.common_tags
}

resource "aws_iam_role" "rds_monitoring" {
  name = "${local.cluster_name}-rds-monitoring"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "monitoring.rds.amazonaws.com" }
      Action = "sts:AssumeRole"
    }]
  })
  tags = local.common_tags
}

resource "aws_iam_role_policy_attachment" "rds_monitoring" {
  role       = aws_iam_role.rds_monitoring.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole"
}

# ----- Aurora alternative (commented) -----
#
# When you outgrow RDS or need cross-region replication, switch to Aurora:
#
# resource "aws_rds_cluster" "aurora" {
#   cluster_identifier      = "${local.cluster_name}-aurora"
#   engine                  = "aurora-postgresql"
#   engine_version          = "16.1"
#   database_name           = "hopeup"
#   master_username         = "hopeup"
#   master_password         = random_password.rds.result
#   db_subnet_group_name    = aws_db_subnet_group.rds.name
#   vpc_security_group_ids  = [aws_security_group.rds.id]
#   storage_encrypted       = true
#   kms_key_id              = aws_kms_key.rds.arn
#   backup_retention_period = 30
#   skip_final_snapshot     = false
#   tags                    = local.common_tags
# }
#
# resource "aws_rds_cluster_instance" "aurora_instances" {
#   count              = 2
#   identifier         = "${local.cluster_name}-aurora-${count.index}"
#   cluster_identifier = aws_rds_cluster.aurora.id
#   instance_class     = "db.r6g.large"
#   engine             = aws_rds_cluster.aurora.engine
#   engine_version     = aws_rds_cluster.aurora.engine_version
# }
