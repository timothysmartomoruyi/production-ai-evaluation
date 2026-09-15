import random
import json
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def generate_logs(num_requests=500):
    logs = []

    start_time = datetime.now() - timedelta(minutes=60)

    for i in range(num_requests):
        timestamp = start_time + timedelta(seconds=i * 7)

        # Normal production behaviour
        latency = random.randint(300, 1200)
        status = "success"
        tool = random.choice(["sql", "weather_api", "none"])
        tokens = random.randint(300, 1200)

        # Inject an incident halfway through the simulation
        if i >= 250:
            latency = random.randint(3000, 7000)

            # SQL becomes the main source of failures
            tool = "sql"

            if random.random() < 0.35:
                status = "error"

        logs.append({
            "request_id": f"REQ-{i+1:05d}",
            "timestamp": timestamp.isoformat(),
            "latency_ms": latency,
            "status": status,
            "tool": tool,
            "tokens": tokens
        })

    return logs


if __name__ == "__main__":
    logs = generate_logs()

    output_path = PROJECT_ROOT / "incidents" / "production_logs.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w") as file:
        json.dump(logs, file, indent=2)

    print(f"Generated {len(logs)} production logs.")