from __future__ import annotations

from mercury.plugin_api import BasePlugin, dispatch_lifecycle


class ComplianceChecklistPlugin(BasePlugin):
    def setup(self) -> int:
        print("compliance_checklist setup complete")
        return 0

    def run(self) -> int:
        checklist = [
            "Written authorization is confirmed.",
            "Testing scope and dates are documented.",
            "Environment is isolated from production and public networks.",
            "Data handling policy for generated logs/reports is defined.",
            "Rollback or cleanup plan is documented.",
        ]
        print("Pre-run compliance checklist:")
        for item in checklist:
            print(f" - [ ] {item}")
        return 0

    def cleanup(self) -> int:
        print("compliance_checklist cleanup complete")
        return 0


if __name__ == "__main__":
    raise SystemExit(dispatch_lifecycle(ComplianceChecklistPlugin()))
