# EKS cluster with two node groups:
#   - "system": runs platform add-ons (ingress, dns, monitoring)
#   - "workload": runs HopeUp application pods, autoscales 3-20

module "eks_cluster" {
  source = "./modules/eks"  # Replace with terraform-aws-modules/eks/aws v20+ in real use

  cluster_name    = local.cluster_name
  cluster_version = var.k8s_version

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnet_ids

  cluster_endpoint_public_access  = true
  cluster_endpoint_private_access = true

  enable_irsa = true

  # API logs
  cluster_enabled_log_types = ["api", "audit", "authenticator", "controllerManager", "scheduler"]

  # Encryption at rest
  cluster_encryption_config = [{
    provider_key_arn = aws_kms_key.eks.arn
    resources        = ["secrets"]
  }]

  tags = local.common_tags
}

resource "aws_kms_key" "eks" {
  description             = "EKS Secret Encryption Key for ${local.cluster_name}"
  deletion_window_in_days = 30
  enable_key_rotation     = true
  tags                    = local.common_tags
}

# System node group: small footprint, on-demand for stability
resource "aws_eks_node_group" "system" {
  cluster_name    = module.eks_cluster.cluster_name
  node_group_name = "system"
  node_role_arn   = aws_iam_role.eks_node.arn
  subnet_ids      = module.vpc.private_subnet_ids

  scaling_config {
    desired_size = 2
    min_size     = 2
    max_size     = 4
  }

  instance_types = ["t3.large"]
  capacity_type  = "ON_DEMAND"
  ami_type       = "AL2_x86_64"
  disk_size      = 50

  labels = {
    "workload-type" = "system"
  }

  taint {
    key    = "system"
    value  = "true"
    effect = "NO_SCHEDULE"
  }

  update_config {
    max_unavailable_percentage = 33
  }

  tags = merge(local.common_tags, { NodeGroup = "system" })

  lifecycle {
    ignore_changes = [scaling_config[0].desired_size]
  }
}

# Workload node group: bigger machines, mix of on-demand + spot
resource "aws_eks_node_group" "workload" {
  cluster_name    = module.eks_cluster.cluster_name
  node_group_name = "workload"
  node_role_arn   = aws_iam_role.eks_node.arn
  subnet_ids      = module.vpc.private_subnet_ids

  scaling_config {
    desired_size = 3
    min_size     = 3
    max_size     = 20
  }

  instance_types = ["m6i.xlarge", "m5.xlarge"]
  capacity_type  = "SPOT"
  ami_type       = "AL2_x86_64"
  disk_size      = 100

  labels = {
    "workload-type" = "application"
  }

  update_config {
    max_unavailable_percentage = 25
  }

  tags = merge(local.common_tags, { NodeGroup = "workload" })

  lifecycle {
    ignore_changes = [scaling_config[0].desired_size]
  }
}

# Cluster Autoscaler IRSA
resource "aws_iam_role" "cluster_autoscaler" {
  name = "${local.cluster_name}-cluster-autoscaler"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Federated = module.eks_cluster.oidc_provider_arn
      }
      Action = "sts:AssumeRoleWithWebIdentity"
      Condition = {
        StringEquals = {
          "${module.eks_cluster.oidc_provider}:sub" = "system:serviceaccount:kube-system:cluster-autoscaler"
        }
      }
    }]
  })

  tags = local.common_tags
}

resource "aws_iam_role_policy_attachment" "cluster_autoscaler" {
  role       = aws_iam_role.cluster_autoscaler.name
  policy_arn = aws_iam_policy.cluster_autoscaler.arn
}

resource "aws_iam_policy" "cluster_autoscaler" {
  name = "${local.cluster_name}-cluster-autoscaler"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "autoscaling:DescribeAutoScalingGroups",
        "autoscaling:DescribeAutoScalingInstances",
        "autoscaling:DescribeLaunchConfigurations",
        "autoscaling:DescribeTags",
        "autoscaling:SetDesiredCapacity",
        "autoscaling:TerminateInstanceInAutoScalingGroup",
        "ec2:DescribeLaunchTemplateVersions"
      ]
      Resource = "*"
    }]
  })
}
