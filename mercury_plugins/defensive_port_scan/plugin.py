from mercury.plugin_api import BasePlugin, dispatch_lifecycle
from mercury.defensive_tools import local_port_scan
import argparse


class DefensivePortScan(BasePlugin):
    def __init__(self, args=None):
        self.args = args

    def setup(self):
        print('Defensive port scan: setup (no-op)')

    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--ports', default='22,80,443', help='Comma-separated ports to scan')
        ns, _ = parser.parse_known_args(self.args)
        ports = [int(p.strip()) for p in ns.ports.split(',') if p.strip().isdigit()]
        print(f"Scanning localhost ports: {ports}")
        open_ports = local_port_scan('127.0.0.1', ports=ports)
        if open_ports:
            print('Open ports found:', open_ports)
        else:
            print('No open ports found on localhost (common for isolated lab).')

    def cleanup(self):
        print('Defensive port scan: cleanup (no-op)')


if __name__ == '__main__':
    import sys
    p = DefensivePortScan(sys.argv[1:])
    raise SystemExit(dispatch_lifecycle(p))
