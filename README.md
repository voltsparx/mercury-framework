# Mercury Framework v3.0

Mercury Framework is an advanced, safe simulation framework for authorized
security testing labs. It is built for realistic training workflows while
enforcing local-only policy controls and isolation-first execution paths.

Author: `voltsparx`  
Contact: `voltsparx@gmail.com`

## Core Principles

- Safe by default: no malware or unauthorized-access payloads
- Professional workflows: CLI automation + guided beginner mode
- Isolation first: subprocess sandbox and Docker isolation
- Structured operations: diagnostics, reporting, metadata, and validation

## What Is New In v3.0

- Global release uplift to `v3.0` (`3.0.0` package version)
- Central metadata module: `mercury/metadata.py`
- Enhanced launcher:
  - `--quickstart`
  - `--doctor`
  - `--show-metadata`
  - `--strict`
  - `--no-color`
- Richer console command surface:
  - `metadata`
  - `doctor`
  - `quickstart`
- Better error handling and command return codes in non-interactive mode
- Updated docs map in `docs/Usage.txt` (A-Z plain text)

## Safety Notice

Use only in authorized and isolated environments.

- `RESPONSIBLE_USE.md`
- `SECURITY.md`
- `LAB_SETUP.md`

## Architecture

```text
mercury-framework/
  mercury/                 core framework package
  mercury_plugins/         runnable plugins and templates
  detection/               defensive parsing helpers
  tools/                   static analyzers and validation tools
  sandbox/                 Docker isolation scripts and compose
  docs/                    text usage reference (A-Z)
  tests/                   automated tests
  run.py                   repository launcher
```

## Installation

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

Linux/macOS shell:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

Entry points:

- `python run.py`
- `python -m mercury`
- `mercury`

## Quickstart Paths

Fast onboarding flow:

```bash
python run.py --quickstart
```

Guided beginner wizard:

```bash
python run.py --wizard
```

Doctor diagnostics:

```bash
python run.py --doctor
```

Metadata output:

```bash
python run.py --show-metadata
```

## Launcher Flags

```text
-c, --command <cmd>          Execute one console command and exit
-s, --script <file>          Execute commands from script file
-y, --yes                    Auto-install missing requirements
--wizard                     Guided beginner mode
--quickstart                 Baseline onboarding workflow
--doctor                     Environment diagnostics + report
--show-metadata              Print framework metadata and exit
--list-plugins               List runnable plugins and exit
--docker                     Use Docker in guided quick flows
--report-dir <path>          Report output directory
--theme <name>               Theme: mercury, mono, sunset
--device-profile <profile>   Initial simulated device profile
--strict                     Stop command/script mode on first error
--no-color                   Disable ANSI color output
--no-clear                   Do not clear terminal at startup
```

## Console Commands

```text
help
clear
banner
metadata
doctor
quickstart
modules
info <plugin>
run <plugin> [setup,run,cleanup] [--timeout <sec>] [--docker] [--report-dir <path>]
device list
device use <profile_key>
device current
sim device|contacts|sensors|storage
echo start|stop|send <message>
analyze manifest <path_to_AndroidManifest.xml>
logparse <file>
report list|latest
exit | quit
```

## Simulated Device Profiles

- `android_pixel_lab`
- `android_legacy_avd`
- `windows_workstation`
- `linux_analyst_vm`
- `macos_research_vm`
- `iot_gateway_lab`

Example:

```bash
python run.py --device-profile windows_workstation -c "device current"
```

## Plugin System

Built-in runnable plugins:

- `example_simulator`
- `defensive_port_scan`
- `educational_offense_template`
- `plugin_template`
- `incident_reporter`
- `telemetry_snapshot`
- `local_log_watch`
- `sandbox_healthcheck`
- `compliance_checklist`

Plugin command examples:

```bash
python run.py -c "modules"
python run.py -c "info incident_reporter"
python run.py -c "run incident_reporter run"
python run.py -c "run sandbox_healthcheck setup,run,cleanup"
```

## Reporting

Each run writes:

- `reports/<timestamp>_<plugin>.json`
- `reports/<timestamp>_<plugin>.md`

Diagnostics writes:

- `reports/<timestamp>_diagnostics.json`

## Docker Isolation (Windows + Linux)

Windows:

```powershell
.\sandbox\build_windows.ps1 -Image mercury-sandbox:latest
.\sandbox\run_windows.ps1 -Plugin incident_reporter -Phases run
```

Linux/macOS:

```bash
./sandbox/build_linux.sh mercury-sandbox:latest
./sandbox/run_linux.sh mercury-sandbox:latest incident_reporter run
```

Compose:

```bash
docker compose -f sandbox/docker-compose.yml run --rm mercury-sandbox
```

Integrated Docker run:

```bash
python run.py -c "run incident_reporter run --docker"
```

## Packaging

Package metadata and entrypoints:

- `pyproject.toml`
- `setup.py`

Build/install scripts:

- `scripts/build_windows_installer.ps1`
- `scripts/build_msi.ps1`
- `scripts/build_debian.sh`
- `scripts/build_arch.sh`
- `scripts/build_macos_installer.sh`

Detailed packaging instructions:

- `INSTALL.md`

## CI Quality Gates

GitHub Actions enforces quality on every push and pull request:

- Ruff lint gate
- Mypy type-check gate for core framework modules
- Manifest validation gate
- Multi-OS and multi-Python test matrix
- Coverage threshold gate (>=80% on core framework modules)

Workflow file:

- `.github/workflows/ci.yml`

## Hardened Release Pipeline

Tag pushes (`v*`) trigger a hardened release workflow that produces:

- wheel and source distribution
- SHA256 checksum manifest
- signed checksum artifact (keyless signing)
- CycloneDX SBOM
- build provenance attestation
- GitHub release asset upload

Workflow file:

- `.github/workflows/release.yml`

## Governance and Project Operations

Governance assets included:

- `CODE_OF_CONDUCT.md`
- `.github/CODEOWNERS`
- `.github/ISSUE_TEMPLATE/bug_report.yml`
- `.github/ISSUE_TEMPLATE/feature_request.yml`
- `.github/pull_request_template.md`
- `.github/release-drafter.yml`
- `.github/workflows/release-drafter.yml`
- `.github/dependabot.yml`

## Documentation Map

- Main docs: `README.md`
- A-Z usage map: `docs/Usage.txt`
- Plugin authoring: `PLUGIN_AUTHOR_GUIDE.md`
- Lab preparation: `LAB_SETUP.md`
- Responsible use: `RESPONSIBLE_USE.md`

## Validation

```bash
python -m pytest -q
python tools/check_manifests.py
```

## License

MIT. See `LICENSE`.
