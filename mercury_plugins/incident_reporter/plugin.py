from __future__ import annotations

from datetime import datetime, timezone
import json

from mercury.plugin_api import BasePlugin, dispatch_lifecycle


class IncidentReporterPlugin(BasePlugin):
    def setup(self) -> int:
        print("incident_reporter setup complete")
        return 0

    def run(self) -> int:
        incidents = [
            {
                "id": "INC-0001",
                "severity": "medium",
                "title": "Suspicious local shell pattern",
                "status": "triage",
            },
            {
                "id": "INC-0002",
                "severity": "low",
                "title": "Repeated auth failure in sample logs",
                "status": "open",
            },
        ]
        payload = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source": "simulated_training_data",
            "incident_count": len(incidents),
            "incidents": incidents,
        }
        print(json.dumps(payload, indent=2))
        return 0

    def cleanup(self) -> int:
        print("incident_reporter cleanup complete")
        return 0


if __name__ == "__main__":
    raise SystemExit(dispatch_lifecycle(IncidentReporterPlugin()))
