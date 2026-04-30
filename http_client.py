"""HTTP_Client: sends HTTP GET requests with rate-limiting and error handling."""

import logging
import time

import requests

logger = logging.getLogger(__name__)


class HTTP_Client:
    """Perform HTTP GET requests with configurable timeout, delay, and User-Agent."""

    def __init__(
        self,
        timeout: int = 10,
        delay: float = 0.3,
        user_agent: str = "ContactExtractorBot/1.0",
    ) -> None:
        self.timeout = timeout
        self.delay = delay
        self.user_agent = user_agent

    def get(self, url: str) -> str | None:
        """
        Perform an HTTP GET request.

        Returns the response body as a UTF-8 string on HTTP 200.
        Returns None on non-200 status or network/timeout error.
        Sleeps `delay` seconds after every call.
        """
        headers = {"User-Agent": self.user_agent}
        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
            if response.status_code == 200:
                return response.text
            else:
                logger.warning(
                    "Non-200 response for '%s': status %d", url, response.status_code
                )
                return None
        except requests.exceptions.RequestException as exc:
            logger.warning("Network error fetching '%s': %s", url, exc)
            return None
        finally:
            time.sleep(self.delay)
