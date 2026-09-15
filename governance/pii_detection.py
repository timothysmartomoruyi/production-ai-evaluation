import re


def detect_pii(text):

    emails = re.findall(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        text
    )

    phone_numbers = re.findall(
        r"\b(?:\+44\s?7\d{3}|\b07\d{3})\s?\d{3}\s?\d{3}\b",
        text
    )

    return {
        "emails_detected": len(emails),
        "phone_numbers_detected": len(phone_numbers),
        "contains_pii": bool(emails or phone_numbers)
    }