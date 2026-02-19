Plugin Author Guide

This document explains how to author safe plugins for Mercury v3.0.

Required files

- `manifest.json` (required): must include `name`, `version`, `network_policy`, and `responsible_use`.
 - `plugin.py` (required): must implement a lifecycle using `mercury.plugin_api.BasePlugin` or accept `--setup`, `--run`, `--cleanup`.

Manifest example

```json
{
  "name": "example_plugin",
  "version": "3.0.0",
  "description": "Describe what this plugin does (safe-only).",
  "author": "yourname",
  "network_policy": "local-only",
  "responsible_use": "Describe how this plugin should be used and tested."
}
```

Lifecycle

- Plugins should implement `setup()`, `run()`, and `cleanup()` hooks where appropriate.
 - Plugins are executed via the Mercury sandbox which sets `MERCURY_SAFE=1` in the environment; plugins should check this variable and refuse to run otherwise.
- Keep plugin actions benign and local-only: prefer `127.0.0.1` and simulated data unless you have explicit written authorization to test remote hosts.
- Use `mercury.plugin_api.dispatch_lifecycle` for consistent `--setup/--run/--cleanup` behavior.
- Plugin runs automatically generate JSON/Markdown reports in `reports/` through the main console workflow.
- Console operators can apply execution controls such as `--timeout <sec>` and `--docker` in the run command.

Testing

 - Add unit tests that exercise the lifecycle by invoking the plugin subprocess with `MERCURY_SAFE=1` and passing `--setup/--run/--cleanup` flags.
- Ensure tests run inside CI and that the manifest checker passes.

Distribution

 - Plugins are distributed as folders under `mercury_plugins/`.
- Keep documentation and `responsible_use` statements clear and explicit.

Security and responsible use

- Do NOT embed exploit code, backdoors, or persistence mechanisms in plugins hosted in this repository.
- Use this framework for authorized testing, emulation, and training only.
- If your work requires higher privileges or network access, document the justification and obtain explicit authorization.


