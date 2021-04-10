from typing import Optional
from urllib.parse import urlparse

from .routes.discussions import DiscussionsRoute


class Flarum:
    """
    Creates a Flarum instance.

    **Parameters:**

    * **url** - Direct URL to the website.
    * **master_key** - Flarum master key
    """

    def __init__(self, url: str, master_key: Optional[str] = None) -> None:
        parse = urlparse(url)
        if not parse.scheme.startswith(("http", "https")):
            raise ValueError("url parameter should start with http or https.")

        self.url = url
        self.master_key = master_key

    def discussions(self) -> DiscussionsRoute:
        """
        Discussions API Route.
        """
        d = DiscussionsRoute(self.url, self.master_key)
        return d
