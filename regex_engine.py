"""Regex_Engine: extracts email addresses and phone numbers from plain text."""

import re

# Module-level compiled patterns (compiled once at import time)

# Valid Email: RFC 5322 simplified — domain must contain a dot (enforced by \.[a-zA-Z]{2,})
EMAIL_PATTERN = re.compile(
    r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
)

# Valid Phone: starts with optional + or (, followed by a digit, then 5+ mixed chars, ends with digit
PHONE_PATTERN = re.compile(
    r"[\+\(]?[\d][\d\s\-\.\(\)]{5,}[\d]"
)


class Regex_Engine:
    """Apply regular expressions to extract emails and phone numbers from text."""

    def extract_emails(self, text: str) -> list[str]:
        """
        Return all valid email addresses found in text, lowercased.

        Excludes matches where the domain has no dot (already prevented by the pattern).
        Returns [] for empty or None text.
        """
        if not text:
            return []

        matches = EMAIL_PATTERN.findall(text)
        return [m.lower() for m in matches]

    def extract_phones(self, text: str) -> list[str]:
        """
        Return all valid phone numbers found in text, as digit-only strings.

        Excludes matches with fewer than 7 or more than 15 digits.
        Returns [] for empty or None text.
        """
        if not text:
            return []

        matches = PHONE_PATTERN.findall(text)
        result: list[str] = []
        for match in matches:
            digits = re.sub(r"\D", "", match)
            if 7 <= len(digits) <= 15:
                result.append(digits)
        return result
