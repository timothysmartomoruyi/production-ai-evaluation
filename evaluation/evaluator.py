import json
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_dataset():
    dataset_path = PROJECT_ROOT / "evaluation" / "dataset.json"
    with dataset_path.open("r") as file:
        return json.load(file)


def evaluate_report(report, test_case):

    report_lower = report.lower()

    expected_cause = test_case["expected_root_cause"].lower()

    cause_match = expected_cause in report_lower

    evidence_matches = []

    for evidence in test_case["required_evidence"]:
        if evidence.lower() in report_lower:
            evidence_matches.append(evidence)

    evidence_score = len(evidence_matches) / len(
        test_case["required_evidence"]
    )

    unsupported_language = [
        "database outage",
        "network failure",
        "infrastructure failure",
        "configuration error"
    ]

    unsupported_claims = [
        claim for claim in unsupported_language
        if claim in report_lower
    ]

    grounding_score = 1.0 if not unsupported_claims else 0.0

    overall_score = (
        (1.0 if cause_match else 0.0)
        + evidence_score
        + grounding_score
    ) / 3

    return {
        "cause_match": cause_match,
        "evidence_score": round(evidence_score, 2),
        "grounding_score": grounding_score,
        "overall_score": round(overall_score, 2),
        "unsupported_claims": unsupported_claims,
        "passed": overall_score >= 0.7
    }


def evaluate_saved_reports():

    dataset = load_dataset()

    reports_directory = PROJECT_ROOT / "incidents" / "reports"

    if not reports_directory.exists():
        print("No incident reports directory found.")
        return

    report_files = [
        file for file in os.listdir(reports_directory)
        if file.endswith(".json")
        and not file.endswith("_evaluation.json")
    ]

    if not report_files:
        print("No saved incident reports found.")
        return

    print("\n=== AI INCIDENT EVALUATION ===\n")

    for report_file in sorted(report_files):

        path = reports_directory / report_file

        with path.open("r") as file:
            report_data = json.load(file)

        report = report_data["report"]

        incident_type = report_data["incident"]["type"]

        matching_test = None

        for test_case in dataset:

            if test_case["incident"]["type"] == incident_type:
                matching_test = test_case
                break

        if matching_test is None:
            print(f"No evaluation test found for {incident_type}")
            continue

        result = evaluate_report(report, matching_test)

        evaluation_path = path.with_name(path.stem + "_evaluation.json")

        evaluation_data = {
            "report_file": report_file,
            "incident": report_data["incident"],
            "evaluation": result
        }

        with evaluation_path.open("w") as file:
            json.dump(evaluation_data, file, indent=2)

        print(f"Report: {report_file}")
        print(f"Incident: {incident_type}")
        print(f"Overall score: {result['overall_score']}")
        print(f"Passed: {result['passed']}")
        print(f"Evidence score: {result['evidence_score']}")
        print(f"Grounding score: {result['grounding_score']}")

        if result["unsupported_claims"]:
            print(
                f"Unsupported claims: "
                f"{result['unsupported_claims']}"
            )

        print("-" * 50)


if __name__ == "__main__":
    evaluate_saved_reports()