# Mercury Framework v0.3.0

Mercury Framework is a professional-grade, safe RAT-style simulation platform
for defenders, educators, and red/blue training labs. It is designed for
authorized environments only, with strict local-only defaults and isolation
options for repeatable learning workflows.

## Why Mercury

- Safe-by-design simulation (no malware, no persistence payloads, no exfiltration logic)
- Dual user experience:
  - guided beginner wizard
  - advanced command-driven console
- Plugin-first architecture with manifest policy validation
- Rich terminal themes and structured output
- Built-in reporting (JSON and Markdown)
- Cross-platform Docker isolation for Windows and Linux
- Multi-device simulation profiles for realistic training scenarios

## Safety Notice

Mercury is for authorized security training and simulation only.

- Read `RESPONSIBLE_USE.md`
- Read `SECURITY.md`
- Read `LAB_SETUP.md`

Do not use this framework against systems without explicit written permission.

## Feature Set (v0.3.0)

- Launcher modes:
  - `argparse` command/script mode for developers
  - guided wizard mode for beginners
- Console capabilities:
  - plugin discovery, info, execution
  - log parsing and static manifest analysis
  - local echo server demo
  - report browsing
  - device profile management
- Built-in simulated device profiles:
  - `android_pixel_lab`
  - `android_legacy_avd`
  - `windows_workstation`
  - `linux_analyst_vm`
  - `macos_research_vm`
  - `iot_gateway_lab`
- Safe plugin sandbox execution:
  - subprocess mode
  - Docker mode (`--docker`) with network disabled
- Report artifacts per plugin run:
  - `reports/<timestamp>_<plugin>.json`
  - `reports/<timestamp>_<plugin>.md`

## Project Layout

```text
mercury-framework/
  mercury/                 # core framework package
  mercury_plugins/         # runnable plugins + templates
  detection/               # defensive parsing helpers
  tools/                   # static analyzers and utilities
  sandbox/                 # Docker isolation files and scripts
  tests/                   # test suite
  run.py                   # repo launcher
```

## Installation

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

### Linux/macOS (bash)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

### Installed command

After installation, use either:

- `python run.py`
- `python -m mercury`
- `mercury`

## Quick Start

### Interactive launcher

```bash
python run.py
```

### Beginner wizard

```bash
python run.py --wizard
```

### Advanced one-shot command

```bash
python run.py -c "modules"
```

### Command script execution

```bash
python run.py -s my_commands.txt
```

### List plugins

```bash
python run.py --list-plugins
```

## Launcher Arguments (argparse mode)

```text
-c, --command <cmd>          Execute one console command and exit
-s, --script <file>          Execute commands from a script file
-y, --yes                    Auto-install missing requirements
--wizard                     Start guided beginner mode
--list-plugins               Print discovered plugins
--docker                     Use Docker mode in wizard-guided runs
--report-dir <path>          Output directory for run reports
--theme <name>               Console theme (mercury, sunset, mono)
--device-profile <profile>   Initial simulated device profile
--no-clear                   Skip clear-screen behavior
```

## Console Commands

```text
help
clear
banner
modules
info <plugin>
run <plugin> [setup,run,cleanup] [--docker] [--report-dir <path>]
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

## Usage Examples

### 1) Run a plugin locally (subprocess mode)

```bash
python run.py -c "run incident_reporter run"
```

### 2) Run setup+run+cleanup lifecycle

```bash
python run.py -c "run sandbox_healthcheck setup,run,cleanup"
```

### 3) Run a plugin with Docker isolation

```bash
python run.py -c "run telemetry_snapshot run --docker"
```

### 4) Switch device profile in console

```text
mercury> device list
mercury> device use windows_workstation
mercury> device current
```

### 5) Parse suspicious lines from a log file

```bash
python run.py -c "logparse sample.log"
```

### 6) Inspect generated reports

```text
mercury> report list
mercury> report latest
```

## Built-in Plugins

Core + added plugins:

- `example_simulator`
- `defensive_port_scan`
- `educational_offense_template`
- `plugin_template`
- `incident_reporter`
- `telemetry_snapshot`
- `local_log_watch`
- `sandbox_healthcheck`
- `compliance_checklist`

## Docker Isolation (Windows + Linux)

### Windows scripts (PowerShell)

Build:

```powershell
.\sandbox\build_windows.ps1 -Image mercury-sandbox:latest
```

Run:

```powershell
.\sandbox\run_windows.ps1 -Plugin incident_reporter -Phases run
```

### Linux scripts (bash)

Build:

```bash
./sandbox/build_linux.sh mercury-sandbox:latest
```

Run:

```bash
./sandbox/run_linux.sh mercury-sandbox:latest incident_reporter run
```

### Docker Compose

```bash
docker compose -f sandbox/docker-compose.yml run --rm mercury-sandbox
```

## Reporting

Each plugin execution writes:

- structured JSON report (automation-friendly)
- Markdown report (human-readable)

Reports include:

- plugin metadata
- runner mode (subprocess or Docker)
- phase list
- return code and timeout state
- captured stdout/stderr
- execution timing

## Packaging and Distribution

Professional packaging metadata is provided in:

- `pyproject.toml`
- `setup.py`

Installed entry points:

- `mercury` command
- `python -m mercury`

Installer/release scripts:

- `scripts/build_windows_installer.ps1`
- `scripts/build_msi.ps1`
- `scripts/build_debian.sh`
- `scripts/build_arch.sh`
- `scripts/build_macos_installer.sh`

See `INSTALL.md` for platform-specific packaging details.

## Plugin Authoring

Read `PLUGIN_AUTHOR_GUIDE.md` for:

- required manifest fields
- lifecycle conventions (`--setup`, `--run`, `--cleanup`)
- responsible-use requirements
- testing expectations

## Quality and Validation

Run tests:

```bash
python -m pytest -q
```

Validate plugin manifests:

```bash
python tools/check_manifests.py
```

## License

MIT License. See `LICENSE`.
