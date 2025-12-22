import sys
import time

def setup():
    print("Setup: initializing example simulator plugin...")
    # Put any setup code here (like creating temp files, configs)
    time.sleep(0.1)  # simulate some work
    print("Setup complete.")

def run():
    print("Run: running safe example plugin...")
    # Your main plugin logic goes here
    time.sleep(0.1)  # simulate some work
    print("Plugin is running safely.")

def cleanup():
    print("Cleanup: cleaning up example simulator plugin...")
    # Cleanup resources here
    time.sleep(0.1)  # simulate some work
    print("Cleanup complete.")

if __name__ == "__main__":
    try:
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
    except Exception as e:
        print(f"Error in plugin: {e}")
        sys.exit(2)
