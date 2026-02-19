"""Main launcher for Mercury Framework."""
from __future__ import annotations

import argparse
import importlib
import os
import subprocess
import sys
from typing import List

from .device_profiles import DEFAULT_PROFILE


def ensure_requirements(reqfile: str = "requirements.txt", auto_yes: bool = False) -> None:
    """Best-effort helper to install missing requirements in dev environments."""
    if not os.path.isfile(reqfile):
        return
    try:
        with open(reqfile, "r", encoding="utf-8") as handle:
            lines = [line.strip() for line in handle if line.strip() and not line.strip().startswith("#")]
    except Exception:
        return

    missing: List[str] = []
    for package in lines:
        import_name = package.split("==")[0].split(">=")[0].split("<=")[0].strip().replace("-", "_")
        try:
            importlib.import_module(import_name)
        except Exception:
            missing.append(package)

    if not missing:
        return

    print("Missing packages detected:")
    for package in missing:
        print(f" - {package}")

    if not auto_yes:
        response = input("Install missing packages now? [y/N]: ").strip().lower()
        if response not in {"y", "yes"}:
            print("Skipping installation. Install manually with:")
            print(f"{sys.executable} -m pip install {' '.join(missing)}")
            return

    for package in missing:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def _read_script(path: str) -> list[str]:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return [line.strip() for line in handle if line.strip() and not line.strip().startswith("#")]
    except FileNotFoundError as exc:
        raise SystemExit(f"Script file not found: {path}") from exc


def _choose_mode() -> str:
    from .ui import print_menu, prompt

    print_menu(
        "Choose startup mode",
        [
            "Beginner wizard (guided prompts)",
            "Advanced console (full command prompt)",
            "Exit",
        ],
    )
    choice = prompt("Enter choice [1-3]: ").strip()
    if choice == "1":
        return "wizard"
    if choice == "2":
        return "advanced"
    return "exit"


def _pick_device_profile(theme: str, current_profile: str) -> str:
    from .device_profiles import profile_keys
    from .ui import print_status, prompt

    print_status("info", f"Current device profile: {current_profile}", theme=theme)
    keys = profile_keys()
    for idx, key in enumerate(keys, start=1):
        print(f" {idx}. {key}")
    selected = prompt("Select profile number (blank to keep current): ").strip()
    if not selected:
        return current_profile
    try:
        profile = keys[int(selected) - 1]
        return profile
    except Exception:
        print_status("warn", "Invalid selection. Keeping current profile.", theme=theme)
        return current_profile


def _guided_wizard(
    *,
    theme: str,
    report_dir: str,
    docker_mode: bool,
    clear_screen: bool,
    device_profile: str,
) -> int:
    from .console import start_console
    from .plugin_loader import discover_plugins
    from .simulated_device import SimulatedDevice
    from .ui import clear_terminal, color_text, print_status, print_menu, prompt

    if clear_screen:
        clear_terminal(force=True)

    current_profile = device_profile
    device = SimulatedDevice(profile_key=current_profile)

    while True:
        print_menu(
            "Beginner wizard",
            [
                "List available plugins",
                "Run plugin (guided)",
                "Show simulated device preview",
                "Change simulated device profile",
                "Open advanced console",
                "Exit",
            ],
            theme=theme,
        )
        choice = prompt("Enter choice [1-6]: ").strip()

        if choice == "1":
            plugins = discover_plugins()
            if not plugins:
                print_status("warn", "No runnable plugins found.", theme=theme)
            else:
                print(color_text("Runnable plugins:", "primary", bold=True, theme=theme))
                for index, plugin in enumerate(plugins, start=1):
                    manifest = plugin.get("manifest", {})
                    print(f" {index}. {plugin['name']} - {manifest.get('description', '')}")
        elif choice == "2":
            plugins = discover_plugins()
            if not plugins:
                print_status("warn", "No runnable plugins found.", theme=theme)
                continue
            for index, plugin in enumerate(plugins, start=1):
                print(f" {index}. {plugin['name']}")
            selected = prompt("Select plugin number: ").strip()
            try:
                plugin = plugins[int(selected) - 1]
            except Exception:
                print_status("error", "Invalid plugin selection.", theme=theme)
                continue
            phases = prompt("Phases [run | setup,run,cleanup] (default run): ").strip() or "run"
            command = f"run {plugin['name']} {phases}"
            if docker_mode:
                command += " --docker"
            start_console(
                non_interactive=True,
                commands=[command],
                theme=theme,
                report_dir=report_dir,
                clear_on_start=False,
                device_profile=current_profile,
            )
        elif choice == "3":
            print(device.device_info())
            print("\nSample SMS:")
            for msg in device.fake_sms():
                print(f" - {msg}")
        elif choice == "4":
            current_profile = _pick_device_profile(theme, current_profile)
            device.switch_profile(current_profile)
        elif choice == "5":
            return start_console(
                theme=theme,
                report_dir=report_dir,
                clear_on_start=clear_screen,
                device_profile=current_profile,
            )
        elif choice == "6":
            return 0
        else:
            print_status("error", "Invalid choice.", theme=theme)


def build_parser() -> argparse.ArgumentParser:
    from .colors import theme_names
    from .device_profiles import profile_keys

    parser = argparse.ArgumentParser(
        prog="mercury-framework",
        description="Mercury Framework - safe educational simulation scaffold",
    )
    parser.add_argument("-c", "--command", help="Execute one console command and exit")
    parser.add_argument("-s", "--script", help="Execute a command script file and exit")
    parser.add_argument("-y", "--yes", action="store_true", help="Auto-accept missing dependency installs")
    parser.add_argument("--wizard", action="store_true", help="Start guided beginner mode")
    parser.add_argument("--list-plugins", action="store_true", help="List discovered runnable plugins and exit")
    parser.add_argument("--docker", action="store_true", help="Use Docker mode for guided plugin runs")
    parser.add_argument("--report-dir", default="reports", help="Directory for generated run reports")
    parser.add_argument("--theme", choices=theme_names(), default="mercury", help="Terminal color theme")
    parser.add_argument("--no-clear", action="store_true", help="Do not clear terminal before interactive mode")
    parser.add_argument(
        "--device-profile",
        choices=profile_keys(),
        default=DEFAULT_PROFILE,
        help="Initial simulated device profile key (use 'device list' in console).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    ensure_requirements("requirements.txt", auto_yes=args.yes)

    from .console import start_console
    from .plugin_loader import discover_plugins
    from .ui import clear_terminal

    if args.list_plugins:
        plugins = discover_plugins()
        if not plugins:
            print("No runnable plugins found under mercury_plugins/.")
            return 0
        for plugin in plugins:
            print(plugin["name"])
        return 0

    if args.command:
        return start_console(
            non_interactive=True,
            commands=[args.command],
            theme=args.theme,
            report_dir=args.report_dir,
            clear_on_start=False,
            device_profile=args.device_profile,
        )

    if args.script:
        lines = _read_script(args.script)
        return start_console(
            non_interactive=True,
            commands=lines,
            theme=args.theme,
            report_dir=args.report_dir,
            clear_on_start=False,
            device_profile=args.device_profile,
        )

    should_clear = not args.no_clear
    if args.wizard:
        return _guided_wizard(
            theme=args.theme,
            report_dir=args.report_dir,
            docker_mode=args.docker,
            clear_screen=should_clear,
            device_profile=args.device_profile,
        )

    if sys.stdin.isatty():
        mode = _choose_mode()
        if mode == "wizard":
            return _guided_wizard(
                theme=args.theme,
                report_dir=args.report_dir,
                docker_mode=args.docker,
                clear_screen=should_clear,
                device_profile=args.device_profile,
            )
        if mode == "exit":
            return 0

    if should_clear:
        clear_terminal(force=True)
    return start_console(
        theme=args.theme,
        report_dir=args.report_dir,
        clear_on_start=False,
        device_profile=args.device_profile,
    )


if __name__ == "__main__":
    raise SystemExit(main())
