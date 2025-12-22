# -*- coding: utf-8 -*-
"""
Example Simulator Plugin for Mercury
This plugin is safe and does not perform harmful operations.
Supports --setup, --run, and --cleanup commands.
"""

import sys

def setup():
    print("Setup completed for example_simulator.")
    return 0

def run():
    print("Running safe example plugin...")
    return 0

def cleanup():
    print("Cleanup completed for example_simulator.")
    return 0

def main():
    if len(sys.argv) < 2:
        print("No command specified. Use --setup, --run, or --cleanup.")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    if cmd == "--setup":
        sys.exit(setup())
    elif cmd == "--run":
        sys.exit(run())
    elif cmd == "--cleanup":
        sys.exit(cleanup())
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
