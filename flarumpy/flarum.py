from typing import Optional
from urllib.parse import urlparse

from httpx import Client

from .routes.discussions import DiscussionsRoute
from .routes.root import RouteRoot


class Flarum:
    """
    Creates a Flarum instance.

    **Parameters:**

    * **url** - Website API URL.
    """

    def __init__(
        self,
        url: str = "https://discuss.flarum.org/api",
        session: Optional[Client] = None,
    ) -> None:
        parse = urlparse(url)
        if not parse.scheme.startswith(("http", "https")):
            raise ValueError("url parameter should start with http or https.")

        self.url = url
        self.session = session or Client()

    def discussions(self) -> DiscussionsRoute:
        """
        Discussions API Route.
        """
        i = DiscussionsRoute(self.url, self.session)
        return i

    def root(self) -> RouteRoot:
        """
        Root API Route.
        """
        i = RouteRoot(self.url, self.session)
        return i
