from evaluator import evaluate_report


def test_good_report():

    report = """
    The most likely root cause is SQL tool failures.

    Evidence shows increased SQL failures and an elevated
    production error rate.

    No evidence confirms a database outage or network failure.
    """

    test_case = {
        "expected_root_cause": "SQL tool failures",
        "required_evidence": [
            "sql",
            "error rate",
            "failures"
        ]
    }

    result = evaluate_report(report, test_case)

    assert result["passed"] is True


def test_unsupported_root_cause():

    report = """
    The incident was caused by a database outage.
    """

    test_case = {
        "expected_root_cause": "SQL tool failures",
        "required_evidence": [
            "sql",
            "error rate",
            "failures"
        ]
    }

    result = evaluate_report(report, test_case)

    assert result["passed"] is False
    assert "database outage" in result["unsupported_claims"]


if __name__ == "__main__":

    test_good_report()
    test_unsupported_root_cause()

    print("All regression tests passed.")