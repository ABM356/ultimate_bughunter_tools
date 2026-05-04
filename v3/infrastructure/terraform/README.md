# Terraform - HopeUp Security Platform

Provisions all AWS infrastructure for HopeUp:

- VPC across 3 AZs with NAT-gateway HA
- EKS cluster with system + workload node groups
- RDS PostgreSQL Multi-AZ (Aurora variant in comments)
- ElastiCache Redis with multi-AZ failover
- OpenSearch managed cluster (3 data + 3 master nodes)
- S3 buckets for reports, scans, logs (KMS-encrypted, versioned)
- IAM roles (node group + IRSA for backend / external-secrets)

## Prerequisites

- Terraform >= 1.6.0
- AWS CLI authenticated with admin access for first-time provisioning
- An S3 bucket for state (`hopeup-terraform-state`) and DynamoDB lock table
  (`hopeup-terraform-locks`). Create both manually before `init`.

## Layout

```
main.tf          # provider + backend + locals
variables.tf     # all input vars
outputs.tf       # exported endpoints + ARNs
vpc.tf           # network
eks.tf           # Kubernetes control plane + node groups
rds.tf           # PostgreSQL (RDS Multi-AZ; Aurora in comments)
elasticache.tf   # Redis
opensearch.tf    # OpenSearch
iam.tf           # IAM roles for nodes + IRSA
s3.tf            # buckets
```

## Usage

```bash
# 1. Pick your environment
cd infrastructure/terraform
export TF_VAR_environment=dev    # dev | staging | production
export TF_VAR_aws_region=us-east-1

# 2. Initialize
terraform init

# 3. Plan
terraform plan -out plan.bin

# 4. Apply (review first)
terraform apply plan.bin

# 5. Configure kubectl
$(terraform output -raw kubeconfig_command)

# 6. Verify
kubectl get nodes
```

## Per-environment overrides

Place tfvars under `envs/`:

```
envs/dev.tfvars
envs/staging.tfvars
envs/production.tfvars
```

Apply with:
```bash
terraform apply -var-file=envs/production.tfvars
```

## Tearing it down

```bash
# RDS deletion protection is on for production. Disable in console first.
terraform destroy -var-file=envs/dev.tfvars
```

## Notes / compromises

- The `module.eks_cluster` and `module.vpc` references in this repo are
  placeholders for the canonical AWS modules:
    - terraform-aws-modules/eks/aws (>= 20.0)
    - terraform-aws-modules/vpc/aws (>= 5.0)
  Replace `source = "./modules/..."` with the registry source when wiring up
  for real.
- Spot instances are used for the workload node group. Switch to ON_DEMAND
  for tighter SLA workloads.
- Aurora is provided as a commented-out alternative in `rds.tf`.
- Backups: 30-day retention on RDS; 7 days on Redis; lifecycle rules on S3.
