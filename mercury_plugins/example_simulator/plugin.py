import sys

def setup():
    print("Setup: initializing example simulator plugin...")

def run():
    print("Run: running safe example plugin...")
    print("Plugin is running safely.")

def cleanup():
    print("Cleanup: cleaning up example simulator plugin...")

if __name__ == "__main__":
    if "--setup" in sys.argv:
        setup()
        sys.exit(0)
    elif "--run" in sys.argv:
        run()
        sys.exit(0)
    elif "--cleanup" in sys.argv:
        cleanup()
        sys.exit(0)
    else:
        print("No valid argument provided. Use --setup, --run, or --cleanup")
        sys.exit(1)
