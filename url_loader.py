"""URL_Loader: reads and normalises URLs from the input CSV file."""

import logging

import pandas as pd

logger = logging.getLogger(__name__)


class URL_Loader:
    """Read base_url.csv, normalise URLs, deduplicate, and return a list."""

    def __init__(self, csv_path: str = "base_url.csv") -> None:
        self.csv_path = csv_path

    def load(self) -> list[str]:
        """
        Read the input CSV, normalise URLs, and return a deduplicated list.

        Raises:
            FileNotFoundError: if csv_path does not exist.
            ValueError: if the 'base_url' column is absent.
        """
        try:
            df = pd.read_csv(self.csv_path)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Input CSV file not found: '{self.csv_path}'. "
                "Please ensure the file exists at the expected path."
            )

        if "base_url" not in df.columns:
            raise ValueError(
                f"The CSV file '{self.csv_path}' does not contain a 'base_url' column. "
                f"Found columns: {list(df.columns)}"
            )

        urls: list[str] = []
        for idx, value in enumerate(df["base_url"]):
            # Skip NaN / blank rows
            if pd.isna(value) or str(value).strip() == "":
                logger.warning("Row %d: empty or whitespace URL — skipping.", idx)
                continue

            url = str(value).strip()

            # Normalise: prepend https:// if no scheme present
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://" + url

            urls.append(url)

        # Deduplicate while preserving insertion order
        return list(dict.fromkeys(urls))
