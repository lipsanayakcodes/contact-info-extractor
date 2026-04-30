"""Result_Writer: serialises Contact Records to an output CSV file."""

import pandas as pd


class Result_Writer:
    """Write a list of Contact Records to a CSV file using pandas."""

    def __init__(self, output_path: str = "output_contacts.csv") -> None:
        self.output_path = output_path

    def write(self, records: list[dict]) -> None:
        """
        Write Contact Records to the output CSV.

        Columns: base_url, emails, phone_numbers.
        emails and phone_numbers are serialised as semicolon-separated strings.
        Overwrites any existing file at output_path.
        """
        rows = []
        for record in records:
            rows.append(
                {
                    "base_url": record["base_url"],
                    "emails": ";".join(record["emails"]),
                    "phone_numbers": ";".join(record["phone_numbers"]),
                }
            )

        df = pd.DataFrame(rows, columns=["base_url", "emails", "phone_numbers"])
        df.to_csv(self.output_path, index=False)

