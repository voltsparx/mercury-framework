"""Mercury interactive console for safe simulation workflows."""
from __future__ import annotations

import importlib
import shlex
import textwrap
from pathlib import Path
from typing import List, Optional

from .benign_demo import EchoServer, echo_client_send
from .diagnostics import collect_diagnostics, write_diagnostics_report
from .metadata import colored_summary
from .plugin_loader import discover_plugins
from .reporting import list_reports, write_run_report
from .sandbox import run_plugin_docker, run_plugin_subprocess, validate_manifest_local_only
from .simulated_contacts import sample_contacts
from .simulated_device import SimulatedDevice
from .simulated_sensors import sensor_readings
from .simulated_storage import storage_listing
from .ui import clear_terminal, color_text, display_banner, print_status, prompt

try:
    import readline  # type: ignore
except Exception:
    readline = None


class MercuryConsole:
    def __init__(
        self,
        *,
        theme: str = "mercury",
        report_dir: str = "reports",
        clear_on_start: bool = False,
        device_profile: str = "android_pixel_lab",
    ):
        self.theme = theme
        self.report_dir = report_dir
        self.clear_on_start = clear_on_start
        self.prompt = color_text("mercury> ", "primary", theme=self.theme)
        self.device = SimulatedDevice(profile_key=device_profile)
        self.echo_server: Optional[EchoServer] = None
        self.plugins = discover_plugins()
        self._setup_readline()

    def _setup_readline(self) -> None:
        if not readline:
            return
        commands = [
            "help",
            "clear",
            "banner",
            "metadata",
            "doctor",
            "quickstart",
            "modules",
            "info",
            "run",
            "device",
            "sim",
            "echo",
            "analyze",
            "logparse",
            "report",
            "exit",
            "quit",
        ]
        plugin_names = [p["name"] for p in self.plugins]
        words = commands + plugin_names

        def completer(text: str, state: int):
            options = [w for w in words if w.startswith(text)]
            if state < len(options):
                return options[state]
            return None

        try:
            readline.set_completer(completer)
            readline.parse_and_bind("tab: complete")
        except Exception:
            pass

    def _refresh_plugins(self) -> None:
        self.plugins = discover_plugins()

    def _find_plugin(self, name: str) -> Optional[dict]:
        self._refresh_plugins()
        return next((p for p in self.plugins if p["name"] == name), None)

    def start(self) -> None:
        if self.clear_on_start:
            clear_terminal(force=True)
        display_banner(theme=self.theme)
        print(colored_summary(theme=self.theme))
        print_status("info", "Type 'help' for commands. Use isolated labs only.", theme=self.theme)
        while True:
            try:
                line = prompt(self.prompt)
            except (KeyboardInterrupt, EOFError):
                print()
                return
            if not line.strip():
                continue
            try:
                self.execute_line(line)
            except SystemExit:
                return
            except Exception as exc:
                print_status("error", f"Command failed: {exc}", theme=self.theme)

    def execute_line(self, line: str) -> int:
        try:
            args = shlex.split(line)
        except ValueError as exc:
            print_status("error", f"Input parse error: {exc}", theme=self.theme)
            return 2
        if not args:
            return 0
        cmd = args[0].lower()
        handler = getattr(self, f"do_{cmd}", None)
        if not handler:
            print_status("error", f"Unknown command '{cmd}'. Type 'help'.", theme=self.theme)
            return 2
        result = handler(args[1:])
        if isinstance(result, int):
            return result
        return 0

    def do_help(self, argv: List[str]) -> None:
        print(
            textwrap.dedent(
                """
                Mercury console commands:

                help                     Show this help
                clear                    Clear terminal
                banner                   Show another banner
                metadata                 Show project metadata
                doctor                   Run environment diagnostics
                quickstart               Run baseline onboarding flow
                modules                  List runnable plugins
                info <plugin>            Show plugin manifest details
                run <plugin> [phases]    Run plugin (phases: setup,run,cleanup)
                                         Options: --docker --report-dir <path> --timeout <sec>
                device list              List built-in simulated device profiles
                device use <profile>     Switch current simulated device profile
                device current           Show active profile details
                sim <target>             Show simulated data (device|contacts|sensors|storage)
                echo start|stop|send     Control local echo server
                analyze manifest <path>  Run AndroidManifest static analyzer
                logparse <file>          Parse suspicious log lines
                report list|latest       Show generated report files
                exit | quit              Exit console
                """
            ).strip()
        )

    def do_metadata(self, argv: List[str]) -> int:
        print(colored_summary(theme=self.theme))
        return 0

    def do_doctor(self, argv: List[str]) -> int:
        payload = collect_diagnostics(report_dir=self.report_dir)
        checks = payload.get("checks", {})
        print_status("info", f"Python: {payload['environment'].get('python_version')}", theme=self.theme)
        print_status(
            "info",
            f"Docker available: {checks.get('docker_available')}",
            theme=self.theme,
        )
        print_status(
            "info",
            f"Runnable plugins: {payload['plugins'].get('runnable')}",
            theme=self.theme,
        )
        if payload.get("overall_ok"):
            print_status("ok", "Diagnostics passed.", theme=self.theme)
            path = write_diagnostics_report(report_dir=self.report_dir)
            print_status("ok", f"Diagnostics report: {path}", theme=self.theme)
            return 0
        print_status("warn", "Diagnostics found issues. Review report.", theme=self.theme)
        path = write_diagnostics_report(report_dir=self.report_dir)
        print_status("warn", f"Diagnostics report: {path}", theme=self.theme)
        return 1

    def do_quickstart(self, argv: List[str]) -> int:
        print_status("info", "Quickstart flow: metadata, doctor, device current, modules.", theme=self.theme)
        steps = ["metadata", "doctor", "device current", "modules"]
        rc = 0
        for command in steps:
            rc = max(rc, self.execute_line(command))
        return rc

    def do_clear(self, argv: List[str]) -> None:
        clear_terminal(force=True)

    def do_banner(self, argv: List[str]) -> None:
        display_banner(theme=self.theme)

    def do_modules(self, argv: List[str]) -> None:
        self._refresh_plugins()
        if not self.plugins:
            print_status("warn", "No runnable plugins found under mercury_plugins/.", theme=self.theme)
            return
        print(color_text("Discovered plugins:", "primary", bold=True, theme=self.theme))
        for plugin in self.plugins:
            manifest = plugin.get("manifest", {})
            name = manifest.get("name", plugin.get("name"))
            description = manifest.get("description", "")
            print(f" - {name}: {description}")

    def do_info(self, argv: List[str]) -> None:
        if not argv:
            print("Usage: info <plugin_name>")
            return
        plugin = self._find_plugin(argv[0])
        if not plugin:
            print_status("error", "Plugin not found.", theme=self.theme)
            return
        manifest = plugin.get("manifest", {})
        print(color_text(f"Name: {manifest.get('name')}", "primary", bold=True, theme=self.theme))
        print(f"Version: {manifest.get('version')}")
        print(f"Author: {manifest.get('author')}")
        print(f"Network policy: {manifest.get('network_policy')}")
        print(f"Description: {manifest.get('description')}")
        print("Responsible use:")
        print(textwrap.indent(str(manifest.get("responsible_use", "N/A")), "  "))

    def do_run(self, argv: List[str]) -> None:
        if not argv:
            print("Usage: run <plugin_name> [phases] [--docker] [--timeout <sec>] [--report-dir <path>]")
            return 2

        plugin_name = argv[0]
        plugin = self._find_plugin(plugin_name)
        if not plugin:
            print_status("error", "Plugin not found.", theme=self.theme)
            return 2

        manifest = plugin.get("manifest", {})
        if not validate_manifest_local_only(manifest):
            print_status("error", "Plugin rejected: requires network_policy=local-only.", theme=self.theme)
            return 2

        phase_spec = "run"
        use_docker = False
        timeout = 25
        report_dir = self.report_dir
        index = 1
        while index < len(argv):
            token = argv[index]
            if token == "--docker":
                use_docker = True
            elif token == "--timeout":
                if index + 1 >= len(argv):
                    print("Usage error: --timeout requires seconds")
                    return 2
                try:
                    timeout = int(argv[index + 1])
                except ValueError:
                    print("Usage error: --timeout must be an integer")
                    return 2
                index += 1
            elif token.startswith("--timeout="):
                try:
                    timeout = int(token.split("=", 1)[1])
                except ValueError:
                    print("Usage error: --timeout must be an integer")
                    return 2
            elif token == "--report-dir":
                if index + 1 >= len(argv):
                    print("Usage error: --report-dir requires a path")
                    return 2
                report_dir = argv[index + 1]
                index += 1
            elif token.startswith("--report-dir="):
                report_dir = token.split("=", 1)[1]
            elif token.startswith("--"):
                print_status("warn", f"Ignoring unknown option: {token}", theme=self.theme)
            else:
                phase_spec = token
            index += 1

        phase_tokens = [p.strip().lower() for p in phase_spec.split(",") if p.strip()]
        arg_map = {"setup": "--setup", "run": "--run", "cleanup": "--cleanup"}
        lifecycle_args = [arg_map[p] for p in phase_tokens if p in arg_map]
        if not lifecycle_args:
            lifecycle_args = ["--run"]
            phase_tokens = ["run"]

        runner = "docker" if use_docker else "subprocess"
        print_status(
            "info",
            f"Running '{plugin_name}' via {runner} with {phase_tokens} (timeout={timeout}s).",
            theme=self.theme,
        )
        try:
            if use_docker:
                result = run_plugin_docker(plugin["path"], args=lifecycle_args, timeout=timeout)
            else:
                result = run_plugin_subprocess(plugin["path"], args=lifecycle_args, timeout=timeout)
        except Exception as exc:
            print_status("error", f"Execution failed before start: {exc}", theme=self.theme)
            return 1

        print(color_text("--- stdout ---", "success", theme=self.theme))
        print(result.get("stdout", "").rstrip())
        stderr = result.get("stderr", "").rstrip()
        if stderr:
            print(color_text("--- stderr ---", "error", theme=self.theme))
            print(stderr)

        try:
            report = write_run_report(
                report_dir=report_dir,
                plugin_name=plugin_name,
                manifest=manifest,
                phases=phase_tokens,
                execution=result,
                runner=runner,
            )
            print_status("ok", f"JSON report: {report['json_path']}", theme=self.theme)
            print_status("ok", f"Markdown report: {report['md_path']}", theme=self.theme)
        except Exception as exc:
            print_status("error", f"Failed to write report: {exc}", theme=self.theme)
            return 1

        if result.get("returncode") != 0:
            print_status(
                "warn",
                f"Plugin exited with code {result.get('returncode')}. Review report output.",
                theme=self.theme,
            )
            return int(result.get("returncode") or 1)
        return 0

    def do_device(self, argv: List[str]) -> None:
        action = argv[0].lower() if argv else "current"
        if action == "list":
            print(color_text("Available simulated device profiles:", "primary", bold=True, theme=self.theme))
            for profile in self.device.available_profiles():
                print(f" - {profile.key}: {profile.label} [{profile.platform}]")
            return
        if action == "use":
            if len(argv) < 2:
                print("Usage: device use <profile_key>")
                return
            try:
                self.device.switch_profile(argv[1])
            except ValueError as exc:
                print_status("error", str(exc), theme=self.theme)
                return
            print_status("ok", f"Active device profile set to {self.device.profile_key}.", theme=self.theme)
            return
        if action == "current":
            print(self.device.device_info())
            return
        print("Usage: device [list|use <profile_key>|current]")

    def do_sim(self, argv: List[str]) -> None:
        if not argv:
            print("Usage: sim <device|contacts|sensors|storage>")
            return
        target = argv[0].lower()
        if target == "device":
            print(self.device.device_info())
        elif target == "contacts":
            for contact in sample_contacts():
                print(f"- {contact.name} | {contact.phone} | {contact.email}")
        elif target == "sensors":
            print(sensor_readings())
        elif target == "storage":
            for entry in storage_listing():
                print(f"- {entry}")
        else:
            print("Unknown simulated target.")

    def do_echo(self, argv: List[str]) -> None:
        if not argv:
            print("Usage: echo start|stop|send <message>")
            return
        cmd = argv[0]
        if cmd == "start":
            if self.echo_server and self.echo_server._thread and self.echo_server._thread.is_alive():
                print_status("warn", "Echo server already running.", theme=self.theme)
                return
            self.echo_server = EchoServer(host="127.0.0.1", port=8000)
            self.echo_server.start()
            print_status("ok", "Echo server started on 127.0.0.1:8000.", theme=self.theme)
        elif cmd == "stop":
            if not self.echo_server:
                print_status("warn", "No running echo server.", theme=self.theme)
                return
            self.echo_server.stop()
            self.echo_server = None
            print_status("ok", "Echo server stopped.", theme=self.theme)
        elif cmd == "send":
            if len(argv) < 2:
                print("Usage: echo send <message>")
                return
            message = " ".join(argv[1:])
            try:
                response = echo_client_send(message, host="127.0.0.1", port=8000)
                print(f"Received: {response}")
            except Exception as exc:
                print_status("error", f"Send failed: {exc}", theme=self.theme)
        else:
            print("Unknown echo command.")

    def do_analyze(self, argv: List[str]) -> None:
        if len(argv) != 2 or argv[0] != "manifest":
            print("Usage: analyze manifest <path_to_AndroidManifest.xml>")
            return
        path = Path(argv[1])
        if not path.exists():
            print(f"File not found: {path}")
            return
        analyzer = importlib.import_module("tools.apk_manifest_analyzer")
        report = analyzer.analyze_manifest(path)
        analyzer.pretty_print(report)

    def do_logparse(self, argv: List[str]) -> None:
        if not argv:
            print("Usage: logparse <file>")
            return
        path = Path(argv[0])
        if not path.exists():
            print(f"File not found: {path}")
            return
        text = path.read_text(encoding="utf-8", errors="replace")
        parser = importlib.import_module("detection.log_parser")
        matches = parser.find_suspicious_lines(text)
        if not matches:
            print_status("ok", "No suspicious lines found.", theme=self.theme)
            return
        print_status("warn", "Suspicious lines:", theme=self.theme)
        for match in matches:
            print(f" - {match}")

    def do_report(self, argv: List[str]) -> None:
        action = argv[0].lower() if argv else "list"
        reports = list_reports(self.report_dir, limit=30)
        if action == "list":
            if not reports:
                print_status("warn", f"No reports found in '{self.report_dir}'.", theme=self.theme)
                return
            print(color_text("Recent reports:", "primary", bold=True, theme=self.theme))
            for path in reports:
                print(f" - {path}")
            return
        if action == "latest":
            if not reports:
                print_status("warn", f"No reports found in '{self.report_dir}'.", theme=self.theme)
                return
            print(reports[0])
            return
        print("Usage: report [list|latest]")

    def do_exit(self, argv: List[str]) -> None:
        if self.echo_server:
            try:
                self.echo_server.stop()
            except Exception:
                pass
        raise SystemExit(0)

    def do_quit(self, argv: List[str]) -> None:
        self.do_exit(argv)


def start_console(
    *,
    non_interactive: bool = False,
    commands: Optional[List[str]] = None,
    theme: str = "mercury",
    report_dir: str = "reports",
    clear_on_start: bool = False,
    device_profile: str = "android_pixel_lab",
    strict: bool = False,
) -> int:
    """Start the Mercury console in interactive or scripted mode."""
    console = MercuryConsole(
        theme=theme,
        report_dir=report_dir,
        clear_on_start=clear_on_start,
        device_profile=device_profile,
    )
    if non_interactive:
        last_rc = 0
        for line in commands or []:
            try:
                rc = console.execute_line(line)
                if rc != 0:
                    last_rc = rc
                    if strict:
                        return rc
            except SystemExit:
                break
        return last_rc
    console.start()
    return 0


if __name__ == "__main__":
    raise SystemExit(start_console())
