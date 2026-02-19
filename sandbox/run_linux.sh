#!/usr/bin/env bash
set -euo pipefail

IMAGE="${1:-mercury-sandbox:latest}"
PLUGIN="${2:-incident_reporter}"
PHASES="${3:-run}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Running plugin '${PLUGIN}' in Docker isolation"
docker run --rm \
  --network none \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=64m \
  -e MERCURY_SAFE=1 \
  -e PYTHONDONTWRITEBYTECODE=1 \
  -v "${REPO_ROOT}:/app:ro" \
  -w /app \
  "${IMAGE}" \
  python run.py -c "run ${PLUGIN} ${PHASES}"
