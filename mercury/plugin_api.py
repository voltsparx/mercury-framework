"""Plugin API helpers and guidelines for Mercury plugins.

This module provides a lightweight abstract base class for plugin authors
and a small CLI helper `dispatch_lifecycle` that plugin `plugin.py` files
can use to expose `--setup`, `--run`, and `--cleanup` entrypoints.
"""
from abc import ABC, abstractmethod
import argparse
import sys


class BasePlugin(ABC):
    """Abstract base class for plugin authors to implement lifecycle hooks."""

    @abstractmethod
    def setup(self) -> int:
        """Optional setup steps. Return 0 on success."""
        return 0

    @abstractmethod
    def run(self) -> int:
        """Main plugin action. Return 0 on success."""
        return 0

    @abstractmethod
    def cleanup(self) -> int:
        """Optional cleanup steps. Return 0 on success."""
        return 0


def dispatch_lifecycle(plugin: BasePlugin):
    """Parse CLI flags and dispatch to plugin lifecycle hooks.

    Plugins should call this from `if __name__ == '__main__':` after creating
    an instance of their plugin class.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--setup", action="store_true", help="Run setup hook")
    parser.add_argument("--run", action="store_true", help="Run main hook")
    parser.add_argument("--cleanup", action="store_true", help="Run cleanup hook")
    args, _extra = parser.parse_known_args()

    # simple safety: require MERCURY_SAFE in env when running via sandbox
    # (the sandbox sets MERCURY_SAFE=1 before invoking the plugin)
    import os
    if os.environ.get("MERCURY_SAFE") != "1":
        print("[mercury] Plugins must be run via Mercury sandbox (MERCURY_SAFE=1)")
        return 1

    # Default behavior: run main phase when no lifecycle flag is provided.
    if not (args.setup or args.run or args.cleanup):
        args.run = True

    code = 0
    if args.setup:
        code = plugin.setup() or 0
    if args.run and code == 0:
        code = plugin.run() or 0
    if args.cleanup and code == 0:
        code = plugin.cleanup() or 0
    return code


if __name__ == "__main__":
    print("This module is a helper for plugin authors. Import and use `dispatch_lifecycle`.")
    sys.exit(0)
