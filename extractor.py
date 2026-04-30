"""Extractor: orchestrates the full contact-information extraction pipeline."""

import logging
from dataclasses import dataclass, field

from contact_extractor.contact_page_resolver import Contact_Page_Resolver
from contact_extractor.data_cleaner import Data_Cleaner
from contact_extractor.html_parser import HTML_Parser
from contact_extractor.http_client import HTTP_Client
from contact_extractor.regex_engine import Regex_Engine
from contact_extractor.result_writer import Result_Writer
from contact_extractor.url_loader import URL_Loader

logger = logging.getLogger(__name__)


@dataclass
class ExtractorConfig:
    """All runtime parameters for the extraction pipeline."""

    input_csv: str = "base_url.csv"
    output_csv: str = "output_contacts.csv"
    http_timeout: int = 10          # seconds
    http_delay: float = 1.0         # seconds between requests
    user_agent: str = "ContactExtractorBot/1.0"
    log_level: int = logging.INFO
    contact_paths: list[str] = field(
        default_factory=lambda: ["/contact", "/contact-us", "/about", "/about-us"]
    )


class Extractor:
    """
    Orchestrate the full pipeline:
      URL loading → HTTP fetching → HTML parsing → contact extraction
      → contact page resolution (if needed) → data cleaning → result writing.
    """

    def __init__(
        self,
        input_csv: str = "base_url.csv",
        output_csv: str = "output_contacts.csv",
        log_level: int = logging.INFO,
        config: ExtractorConfig | None = None,
    ) -> None:
        if config is not None:
            self.config = config
        else:
            self.config = ExtractorConfig(
                input_csv=input_csv,
                output_csv=output_csv,
                log_level=log_level,
            )

    def run(self) -> None:
        """Execute the full pipeline end-to-end and log a summary on completion."""
        logging.basicConfig(
            level=self.config.log_level,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        )

        # Instantiate all components
        url_loader = URL_Loader(csv_path=self.config.input_csv)
        http_client = HTTP_Client(
            timeout=self.config.http_timeout,
            delay=self.config.http_delay,
            user_agent=self.config.user_agent,
        )
        html_parser = HTML_Parser()
        regex_engine = Regex_Engine()
        contact_page_resolver = Contact_Page_Resolver(
            http_client=http_client,
            html_parser=html_parser,
            regex_engine=regex_engine,
        )
        data_cleaner = Data_Cleaner()
        result_writer = Result_Writer(output_path=self.config.output_csv)

        # Load URLs
        urls = url_loader.load()
        total = len(urls)
        logger.info("Loaded %d URL(s) from '%s'.", total, self.config.input_csv)

        records: list[dict] = []
        with_contacts = 0
        without_contacts = 0

        for i, url in enumerate(urls):
            logger.debug("Processing URL %d/%d: %s", i + 1, total, url)

            try:
                html = http_client.get(url)
                text = html_parser.extract_text(html)
                emails = regex_engine.extract_emails(text)
                phones = regex_engine.extract_phones(text)

                # Fall back to contact page resolution if root page yielded nothing
                if not emails and not phones:
                    emails, phones = contact_page_resolver.resolve(url)

                # Deduplicate and validate
                emails, phones = data_cleaner.clean(emails, phones)

                if not emails and not phones:
                    logger.warning("No contact information found for: %s", url)
                    without_contacts += 1
                else:
                    with_contacts += 1

                records.append(
                    {
                        "base_url": url,
                        "emails": emails,
                        "phone_numbers": phones,
                    }
                )

            except Exception as exc:  # noqa: BLE001
                logger.error("Error processing '%s': %s", url, exc)
                # Still record the URL with empty contacts so it appears in output
                records.append(
                    {
                        "base_url": url,
                        "emails": [],
                        "phone_numbers": [],
                    }
                )

        # Write results
        result_writer.write(records)

        # Summary
        logger.info(
            "Pipeline complete. Total: %d | With contacts: %d | Without contacts: %d",
            total,
            with_contacts,
            without_contacts,
        )
        logger.info("Results written to '%s'.", self.config.output_csv)
