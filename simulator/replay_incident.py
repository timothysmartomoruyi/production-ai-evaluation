import json
import os
import sys
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from observability.metrics import load_logs
from observability.alerts import detect_incidents
from ai_agent.agent import investigate_incident


def save_report(incident, report):

    reports_dir = PROJECT_ROOT / "incidents" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = reports_dir / f"incident_{timestamp}.json"

    data = {
        "timestamp": timestamp,
        "incident": incident,
        "report": report
    }

    with filename.open("w") as file:
        json.dump(data, file, indent=2)

    print(f"Report saved: {filename}")


def replay_incident():

    logs = load_logs()

    print("\n=== INCIDENT REPLAY ===\n")

    incidents = detect_incidents(logs)

    if not incidents:
        print("No incidents detected.")
        return

    print(f"Detected {len(incidents)} incident(s).\n")

    for incident in incidents:

        print(f"Severity: {incident['severity']}")
        print(f"Type: {incident['type']}")
        print(f"Message: {incident['message']}")

        if "tool" in incident:
            print(f"Tool: {incident['tool']}")

        print("\nRunning AI investigation...\n")

        report = investigate_incident(incident)

        print("=== AI INVESTIGATION ===")
        print(report)

        save_report(incident, report)

        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    replay_incident()