# Security Policy

Applies to Mercury Framework v3.0.

We take security research and disclosure seriously. If you discover a
vulnerability or an issue in code that might be misused, follow responsible
disclosure:

- Do not publicize the issue before contacting the maintainer: voltsparx@gmail.com
- Provide clear repro steps, affected versions, and suggested mitigations.
- Prefer private disclosure for sensitive reports.

Supply-chain and release hardening:

- CI enforces lint, type-check, tests, coverage, and manifest validation.
- Release pipeline produces checksums, signed checksum artifacts, SBOM, and provenance.

This repository intentionally contains only benign simulation code. If you find
code that could be dangerous, report it immediately.
