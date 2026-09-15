from .metrics import load_logs, calculate_metrics, analyse_tools


ERROR_RATE_THRESHOLD = 10
LATENCY_THRESHOLD = 2000


def detect_incidents(logs):
    incidents = []

    metrics = calculate_metrics(logs)
    tools = analyse_tools(logs)

    if metrics["error_rate"] > ERROR_RATE_THRESHOLD:
        incidents.append({
            "type": "HIGH_ERROR_RATE",
            "severity": "HIGH",
            "message": (
                f"Error rate is "
                f"{metrics['error_rate']}%"
            )
        })

    if metrics["average_latency_ms"] > LATENCY_THRESHOLD:
        incidents.append({
            "type": "HIGH_LATENCY",
            "severity": "HIGH",
            "message": (
                f"Average latency is "
                f"{metrics['average_latency_ms']}ms"
            )
        })

    for tool, stats in tools.items():

        if stats["error_rate"] > ERROR_RATE_THRESHOLD:
            incidents.append({
                "type": "TOOL_FAILURE",
                "severity": "HIGH",
                "tool": tool,
                "message": (
                    f"{tool} error rate is "
                    f"{stats['error_rate']}%"
                )
            })

    return incidents


if __name__ == "__main__":
    logs = load_logs()

    incidents = detect_incidents(logs)

    print("\nDetected Incidents")
    print("------------------")

    for incident in incidents:
        print(incident)