"""Contact_Page_Resolver: discovers and fetches a website's contact page."""

from urllib.parse import urlparse

from contact_extractor.html_parser import HTML_Parser
from contact_extractor.http_client import HTTP_Client
from contact_extractor.regex_engine import Regex_Engine

# Candidate contact page paths to try when the root page yields no contacts
CONTACT_PATHS = ["/contact", "/contact-us", "/about", "/about-us"]


class Contact_Page_Resolver:
    """
    Try common contact page paths under a base URL.
    Returns the first set of contacts found, or empty lists if none found.
    """

    def __init__(
        self,
        http_client: HTTP_Client,
        html_parser: HTML_Parser,
        regex_engine: Regex_Engine,
    ) -> None:
        self.http_client = http_client
        self.html_parser = html_parser
        self.regex_engine = regex_engine

    def resolve(self, base_url: str) -> tuple[list[str], list[str]]:
        """
        Try common contact page paths under base_url.

        Returns (emails, phones) from the first path that yields results.
        Returns ([], []) if no path yields results.
        """
        parsed = urlparse(base_url)
        scheme = parsed.scheme or "https"
        netloc = parsed.netloc

        for path in CONTACT_PATHS:
            candidate = f"{scheme}://{netloc}{path}"
            html = self.http_client.get(candidate)

            if html is not None:
                text = self.html_parser.extract_text(html)
                emails = self.regex_engine.extract_emails(text)
                phones = self.regex_engine.extract_phones(text)

                if emails or phones:
                    return (emails, phones)

        return ([], [])
