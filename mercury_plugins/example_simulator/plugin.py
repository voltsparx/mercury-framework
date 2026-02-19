from mercury.plugin_api import BasePlugin, dispatch_lifecycle


class ExampleSimulatorPlugin(BasePlugin):
    def setup(self):
        print("Setup complete for example_simulator")
        return 0

    def run(self):
        print("Running safe example plugin")
        return 0

    def cleanup(self):
        print("Cleanup done for example_simulator")
        return 0


if __name__ == "__main__":
    raise SystemExit(dispatch_lifecycle(ExampleSimulatorPlugin()))
