def check_report(report):

    report_lower = report.lower()

    dangerous_claims = [
        "delete the database",
        "shutdown production",
        "disable security",
        "remove authentication",
        "delete all data"
    ]

    detected = []

    for claim in dangerous_claims:

        if claim in report_lower:
            detected.append(claim)

    return {
        "safe": len(detected) == 0,
        "dangerous_content": detected
    }