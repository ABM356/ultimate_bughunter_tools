# S3 buckets for HopeUp:
#   - reports:    customer-facing PDF/HTML reports (download links)
#   - scans:      raw scan output (JSON, logs)
#   - logs:       application + cluster log archive

resource "aws_s3_bucket" "reports" {
  bucket = "${local.cluster_name}-reports"
  tags   = merge(local.common_tags, { Purpose = "reports" })
}

resource "aws_s3_bucket" "scans" {
  bucket = "${local.cluster_name}-scans"
  tags   = merge(local.common_tags, { Purpose = "scan-outputs" })
}

resource "aws_s3_bucket" "logs" {
  bucket = "${local.cluster_name}-logs"
  tags   = merge(local.common_tags, { Purpose = "logs" })
}

locals {
  buckets = {
    reports = aws_s3_bucket.reports
    scans   = aws_s3_bucket.scans
    logs    = aws_s3_bucket.logs
  }
}

# Versioning, encryption, public access blocking — apply uniformly to all buckets
resource "aws_s3_bucket_versioning" "this" {
  for_each = local.buckets
  bucket   = each.value.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  for_each = local.buckets
  bucket   = each.value.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.s3.arn
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "this" {
  for_each = local.buckets
  bucket   = each.value.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Lifecycle rules: move to cheaper storage / expire old objects
resource "aws_s3_bucket_lifecycle_configuration" "reports" {
  bucket = aws_s3_bucket.reports.id

  rule {
    id     = "transition-to-ia"
    status = "Enabled"

    filter {}

    transition {
      days          = 90
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 365
      storage_class = "GLACIER"
    }

    noncurrent_version_expiration {
      noncurrent_days = 90
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "scans" {
  bucket = aws_s3_bucket.scans.id

  rule {
    id     = "expire-old-scans"
    status = "Enabled"
    filter {}

    expiration {
      days = 90
    }

    noncurrent_version_expiration {
      noncurrent_days = 30
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "logs" {
  bucket = aws_s3_bucket.logs.id

  rule {
    id     = "tiered-logs"
    status = "Enabled"
    filter {}

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }
    transition {
      days          = 90
      storage_class = "GLACIER"
    }
    expiration {
      days = 730  # 2 years for compliance
    }
  }
}

# CORS for reports bucket (browser downloads via signed URLs)
resource "aws_s3_bucket_cors_configuration" "reports" {
  bucket = aws_s3_bucket.reports.id

  cors_rule {
    allowed_methods = ["GET", "HEAD"]
    allowed_origins = ["https://${var.domain}"]
    allowed_headers = ["*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
}

resource "aws_kms_key" "s3" {
  description             = "S3 buckets encryption key"
  deletion_window_in_days = 30
  enable_key_rotation     = true
  tags                    = local.common_tags
}
