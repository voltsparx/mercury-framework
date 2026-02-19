Containerized sandbox (Windows + Linux)

This folder provides a hardened Docker setup for running Mercury v3.0 plugin
workloads in isolation.

Security defaults:
- no external network (`--network none`)
- read-only root filesystem
- dedicated tmpfs for `/tmp`
- dropped Linux capabilities
- no new privileges

Build image (Windows PowerShell):

```powershell
.\sandbox\build_windows.ps1 -Image mercury-sandbox:latest
```

Build image (Linux/macOS shell):

```bash
./sandbox/build_linux.sh mercury-sandbox:latest
```

Run a plugin in Docker (Windows PowerShell):

```powershell
.\sandbox\run_windows.ps1 -Plugin incident_reporter -Phases run
```

Run a plugin in Docker (Linux/macOS shell):

```bash
./sandbox/run_linux.sh mercury-sandbox:latest incident_reporter run
```

Compose workflow:

```bash
docker compose -f sandbox/docker-compose.yml run --rm mercury-sandbox
```

Mercury integrated Docker mode from repo root:

```powershell
python run.py -c "run incident_reporter run --docker"
```

This is an isolation helper, not a perfect security boundary. For higher
assurance, run inside dedicated VMs and enforce host firewall rules.
