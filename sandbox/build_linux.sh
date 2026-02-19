#!/usr/bin/env bash
set -euo pipefail

IMAGE="${1:-mercury-sandbox:latest}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Building Docker image ${IMAGE}"
docker build -f "${REPO_ROOT}/sandbox/Dockerfile" -t "${IMAGE}" "${REPO_ROOT}"
