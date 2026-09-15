import json
import statistics
from collections import Counter


def load_logs(path="incidents/production_logs.json"):
    with open(path, "r") as file:
        return json.load(file)


def calculate_metrics(logs):
    total_requests = len(logs)

    successful_requests = sum(
        1 for log in logs
        if log["status"] == "success"
    )

    failed_requests = total_requests - successful_requests

    error_rate = (
        failed_requests / total_requests
    ) * 100

    latencies = [
        log["latency_ms"]
        for log in logs
    ]

    average_latency = statistics.mean(latencies)

    return {
        "total_requests": total_requests,
        "successful_requests": successful_requests,
        "failed_requests": failed_requests,
        "error_rate": round(error_rate, 2),
        "average_latency_ms": round(average_latency, 2)
    }

def analyse_tools(logs):
    tool_stats = {}

    tools = set(log["tool"] for log in logs)

    for tool in tools:
        tool_logs = [
            log for log in logs
            if log["tool"] == tool
        ]

        failures = sum(
            1 for log in tool_logs
            if log["status"] == "error"
        )

        avg_latency = statistics.mean(
            log["latency_ms"]
            for log in tool_logs
        )

        tool_stats[tool] = {
            "requests": len(tool_logs),
            "failures": failures,
            "error_rate": round(
                failures / len(tool_logs) * 100,
                2
            ),
            "average_latency_ms": round(
                avg_latency,
                2
            )
        }

    return tool_stats

if __name__ == "__main__":
    logs = load_logs()

    metrics = calculate_metrics(logs)

    print("\nProduction Metrics")
    print("------------------")

    for key, value in metrics.items():
        print(f"{key}: {value}")

    print("\nTool Analysis")
    print("-------------")

    tool_stats = analyse_tools(logs)

    for tool, stats in tool_stats.items():
        print(f"\n{tool}")

        for key, value in stats.items():
            print(f"  {key}: {value}")