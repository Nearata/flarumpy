from typing import Optional
from urllib.parse import urlparse

from .routes.discussions import DiscussionsRoute
from .routes.root import RouteRoot


class Flarum:
    """
    Creates a Flarum instance.

    **Parameters:**

    * **url** - Website API URL.
    * **master_key** - Flarum master key.
    """

    def __init__(
        self,
        url: str = "https://discuss.flarum.org/api",
        master_key: Optional[str] = None,
    ) -> None:
        parse = urlparse(url)
        if not parse.scheme.startswith(("http", "https")):
            raise ValueError("url parameter should start with http or https.")

        self.url = url
        self.master_key = master_key

    def discussions(self) -> DiscussionsRoute:
        """
        Discussions API Route.
        """
        i = DiscussionsRoute(self.url, self.master_key)
        return i

    def root(self) -> RouteRoot:
        """
        Root API Route.
        """
        i = RouteRoot(self.url, self.master_key)
        return i
