#!/usr/bin/env bash
# HopeUp Security Platform - production deploy
#
# Apply Kubernetes manifests via kustomize. Use the GH Actions workflow as the
# primary path; this script is for break-glass and engineer-driven deploys.
#
# Usage:
#   ./scripts/deploy.sh <env> <image-tag>
#     env       dev | staging | production
#     image-tag e.g. v1.2.3 or git short sha
set -euo pipefail

ENVIRONMENT="${1:-}"
IMAGE_TAG="${2:-}"

if [ -z "$ENVIRONMENT" ] || [ -z "$IMAGE_TAG" ]; then
  echo "Usage: $0 <env> <image-tag>" >&2
  exit 64
fi

case "$ENVIRONMENT" in
  dev|staging|production) ;;
  *) echo "Invalid env: $ENVIRONMENT" >&2; exit 64 ;;
esac

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OVERLAY="$REPO_ROOT/infrastructure/kubernetes/overlays/$([ "$ENVIRONMENT" = "production" ] && echo prod || echo dev)"
NAMESPACE="hopeup$([ "$ENVIRONMENT" = "production" ] && echo "" || echo "-$ENVIRONMENT")"

require() { command -v "$1" >/dev/null 2>&1 || { echo "Missing: $1" >&2; exit 1; }; }
require kubectl
require kustomize

echo ">> Confirming target context"
kubectl config current-context
read -p "Continue with deploy to $ENVIRONMENT (tag=$IMAGE_TAG)? [y/N] " yn
[[ "$yn" == "y" || "$yn" == "Y" ]] || { echo "Aborted"; exit 1; }

ECR_REGISTRY="${ECR_REGISTRY:-$(aws ecr describe-registry --query registryId --output text).dkr.ecr.us-east-1.amazonaws.com}"

echo ">> Setting image tags"
(cd "$OVERLAY" && kustomize edit set image \
  ghcr.io/hopeup/backend="$ECR_REGISTRY/hopeup-backend:$IMAGE_TAG" \
  ghcr.io/hopeup/frontend="$ECR_REGISTRY/hopeup-frontend:$IMAGE_TAG")

echo ">> Running migrations"
kubectl apply -f "$REPO_ROOT/infrastructure/kubernetes/base/migration-job.yaml" -n "$NAMESPACE"
kubectl wait --for=condition=complete --timeout=600s -n "$NAMESPACE" job/db-migrate

echo ">> Applying manifests"
kubectl apply -k "$OVERLAY"

echo ">> Waiting for rollouts"
for d in backend frontend worker beat; do
  kubectl rollout status -n "$NAMESPACE" "deployment/$d" --timeout=10m
done

echo ">> Done. Verify:"
echo "kubectl get pods -n $NAMESPACE"
