"""Entry point for the Contact Information Extractor pipeline."""

import argparse
import logging

from contact_extractor.extractor import Extractor, ExtractorConfig


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract email addresses and phone numbers from a list of websites."
    )
    parser.add_argument(
        "--input",
        default="base_url.csv",
        help="Path to the input CSV file (default: base_url.csv)",
    )
    parser.add_argument(
        "--output",
        default="output_contacts.csv",
        help="Path to the output CSV file (default: output_contacts.csv)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="HTTP request timeout in seconds (default: 10)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay between HTTP requests in seconds (default: 1.0)",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level (default: INFO)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    config = ExtractorConfig(
        input_csv=args.input,
        output_csv=args.output,
        http_timeout=args.timeout,
        http_delay=args.delay,
        log_level=getattr(logging, args.log_level),
    )

    extractor = Extractor(config=config)
    extractor.run()


if __name__ == "__main__":
    main()
