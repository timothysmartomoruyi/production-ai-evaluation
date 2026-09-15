import json
import statistics
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_logs(path=None):
    if path is None:
        path = PROJECT_ROOT / "incidents" / "production_logs.json"
    else:
        path = Path(path)
        if not path.is_absolute():
            path = PROJECT_ROOT / path

    with path.open("r") as file:
        return json.load(file)


def get_metrics():
    logs = load_logs()

    total = len(logs)
    failures = sum(1 for log in logs if log["status"] == "error")

    latencies = [log["latency_ms"] for log in logs]

    return {
        "total_requests": total,
        "failed_requests": failures,
        "error_rate": round((failures / total) * 100, 2),
        "average_latency_ms": round(statistics.mean(latencies), 2)
    }


def get_tool_metrics():
    logs = load_logs()
    tools = {}

    for log in logs:
        tool = log["tool"]

        if tool not in tools:
            tools[tool] = {
                "requests": 0,
                "failures": 0,
                "latencies": []
            }

        tools[tool]["requests"] += 1
        tools[tool]["latencies"].append(log["latency_ms"])

        if log["status"] == "error":
            tools[tool]["failures"] += 1

    results = {}

    for tool, data in tools.items():
        results[tool] = {
            "requests": data["requests"],
            "failures": data["failures"],
            "error_rate": round(
                data["failures"] / data["requests"] * 100, 2
            ),
            "average_latency_ms": round(
                statistics.mean(data["latencies"]), 2
            )
        }

    return results


def get_recent_errors(limit=10):
    logs = load_logs()

    errors = [
        log for log in logs
        if log["status"] == "error"
    ]

    return errors[-limit:]


def compare_periods():
    logs = load_logs()

    midpoint = len(logs) // 2

    before = logs[:midpoint]
    after = logs[midpoint:]

    def calculate(logs):
        errors = sum(
            1 for log in logs
            if log["status"] == "error"
        )

        avg_latency = statistics.mean(
            log["latency_ms"] for log in logs
        )

        return {
            "requests": len(logs),
            "error_rate": round(
                errors / len(logs) * 100, 2
            ),
            "average_latency_ms": round(
                avg_latency, 2
            )
        }

    return {
        "before_incident": calculate(before),
        "after_incident": calculate(after)
    }