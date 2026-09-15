
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import ollama
from datetime import datetime
from governance.policy import check_action
from governance.saftey_checks import check_report
from governance.pii_detection import detect_pii

if __package__ in (None, ""):
    from ai_agent.tools import (
        get_metrics,
        get_tool_metrics,
        get_recent_errors,
        compare_periods,
    )
else:
    from .tools import (
        get_metrics,
        get_tool_metrics,
        get_recent_errors,
        compare_periods,
    )


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

    print(f"\nReport saved to: {filename}")

def investigate_incident(incident):

    metrics = get_metrics()
    tool_metrics = get_tool_metrics()
    recent_errors = get_recent_errors()
    period_comparison = compare_periods()

    evidence = {
        "incident": incident,
        "overall_metrics": metrics,
        "tool_metrics": tool_metrics,
        "recent_errors": recent_errors,
        "period_comparison": period_comparison
    }

    prompt = f"""
You are an AI Site Reliability Engineer investigating a
production AI system incident.

Your job is to investigate the evidence rather than guess.

INCIDENT:
{json.dumps(incident, indent=2)}

SYSTEM METRICS:
{json.dumps(metrics, indent=2)}

TOOL METRICS:
{json.dumps(tool_metrics, indent=2)}

RECENT ERRORS:
{json.dumps(recent_errors, indent=2)}

PERIOD COMPARISON:
{json.dumps(period_comparison, indent=2)}

Produce an incident investigation containing:

1. Incident summary
2. Most likely root cause
3. Evidence supporting the conclusion
4. User/system impact
5. Recommended actions
6. Confidence level

IMPORTANT INVESTIGATION RULES:

- Only make claims directly supported by the supplied evidence.
- Do not invent infrastructure failures, database problems, API failures,
  network problems, or configuration problems unless the evidence explicitly
  supports them.
- If the exact root cause cannot be determined, say:
  "Root cause cannot be confirmed from the available evidence."
- Clearly distinguish between:
  A. Observed evidence
  B. Likely explanation
  C. Unconfirmed hypothesis
- Confidence must reflect the strength of the available evidence.
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]
    safety_result = check_report(report)
    pii_result = detect_pii(report)

    if not safety_result["safe"]:
        report += (
            "\n\n[ GOVERNANCE WARNING ]\n"
            "Potentially unsafe recommendation detected.\n"
            f"Detected: {safety_result['dangerous_content']}\n"
            "Human review is required."
        )

    if pii_result["contains_pii"]:
        report += (
            "\n\n[ PII WARNING ]\n"
            "Potential personally identifiable information detected.\n"
            f"Emails: {pii_result['emails_detected']}\n"
            f"Phone numbers: {pii_result['phone_numbers_detected']}\n"
        )

    return report



if __name__ == "__main__":

    incident = {
        "type": "MANUAL_INVESTIGATION",
        "severity": "HIGH",
        "message": "Investigate current production performance"
    }

    report = investigate_incident(incident)

    print("\nAI Incident Investigation")
    print("=========================\n")
    print(report)

    save_report(incident, report)