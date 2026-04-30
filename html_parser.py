"""HTML_Parser: extracts visible text from raw HTML using BeautifulSoup."""

from bs4 import BeautifulSoup


class HTML_Parser:
    """Parse HTML and return visible text, excluding <script> and <style> content."""

    def extract_text(self, html: str | None) -> str:
        """
        Parse HTML and return visible text, excluding <script> and <style>.

        Returns empty string for None or empty input.
        """
        if html is None or html.strip() == "":
            return ""

        soup = BeautifulSoup(html, "html.parser")

        # Remove script and style elements entirely
        for tag in soup(["script", "style"]):
            tag.decompose()

        return soup.get_text(separator=" ", strip=True)