"""Data_Cleaner: deduplicates and validates extracted contact data."""

import re

from contact_extractor.regex_engine import EMAIL_PATTERN


class Data_Cleaner:
    """Deduplicate and validate email addresses and phone numbers."""

    def clean(
        self,
        emails: list[str],
        phones: list[str],
    ) -> tuple[list[str], list[str]]:
        """
        Deduplicate and validate emails and phones.

        Emails:
          - Lowercased
          - Validated against EMAIL_PATTERN (full match)
          - Deduplicated (case-insensitive, insertion order preserved)

        Phones:
          - Stripped to digits only
          - Kept only if digit count is 7–15
          - Deduplicated (insertion order preserved)

        Returns (clean_emails, clean_phones).
        """
        clean_emails = self._clean_emails(emails)
        clean_phones = self._clean_phones(phones)
        return clean_emails, clean_phones

    def _clean_emails(self, emails: list[str]) -> list[str]:
        seen: dict[str, None] = {}
        for email in emails:
            normalised = email.lower()
            # Full-match validation
            if EMAIL_PATTERN.fullmatch(normalised) and normalised not in seen:
                seen[normalised] = None
        return list(seen.keys())

    def _clean_phones(self, phones: list[str]) -> list[str]:
        seen: dict[str, None] = {}
        for phone in phones:
            digits = re.sub(r"\D", "", phone)
            if 7 <= len(digits) <= 15 and digits not in seen:
                seen[digits] = None
        return list(seen.keys())

