from typing import Any

from httpx import Client

from ..utils import authorization_header


class RouteRoot:
    def __init__(self, url: str, session: Client) -> None:
        self.url = url
        self.session = session

    def show(self) -> tuple[int, dict[Any, Any]]:
        """
        Get forum information.

        **Returns:**

        * **tuple** - Status code, Response
        """
        r = self.session.get(self.url)
        return (r.status_code, r.json())

    def token(
        self, identification: str, password: str, remember: bool = False
    ) -> tuple[int, dict[Any, Any]]:
        """
        Retrieve authentication token.

        **Parameters:**

        * **identification** - Flarum username.
        * **password** - Flarum password.
        * **remember** - Remember the session.

        **Returns:**

        * **tuple** - Status code, Response
        """
        payload = {
            "identification": identification,
            "password": password,
            "remember": remember,
        }

        r = self.session.post(f"{self.url}/token", json=payload)
        return (r.status_code, r.json())

    def forgot(
        self, token: str, email: str, user_id: int
    ) -> tuple[int, dict[Any, Any]]:
        """
        Send forgot password email.

        **Parameters:**

        * **token** - Flarum API key or user access token.
        * **email** - Email of the account you want to request a password reset.

        **Returns:**

        * **tuple** - Status code, Response
        """
        payload = {"email": email}

        r = self.session.post(
            f"{self.url}/forgot",
            json=payload,
            headers=authorization_header(token, user_id),
        )
        return (r.status_code, r.json())
