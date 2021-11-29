from typing import Any, Optional
from httpx import Client

from ..utils import authorization_header


class UsersRoute:
    def __init__(self, url: str, session: Client) -> None:
        self.url = f"{url}/users"
        self.session = session

    def index(self, token: str, user_id: int) -> tuple[int, dict[Any, Any]]:
        """
        List users.

        **Parameters:**

        * **token** - User access token or API key.
        * **user_id** - User ID associated to the token.

        **Returns:**

        * **tuple** - Status code, response
        """
        r = self.session.get(self.url, headers=authorization_header(token, user_id))
        return (r.status_code, r.json())

    def create(
        self,
        token: str,
        username: str,
        email: str,
        password: str,
        user_id: Optional[int] = None,
        is_email_confirmed: bool = False,
    ) -> tuple[int, dict[Any, Any]]:
        """
        Register a user.

        **Parameters:**

        * **token** - User Access Token or API key.
        * **username** - Username of the user.
        * **email** - Email to associate to the user.
        * **password** - Password used to login.
        * **user_id** - User ID associated to the token. (required if `token` is API key)
        * **is_email_confirmed** - Confirm the email without sending a confirmation email. (Requires API key)

        **Returns:**

        * **tuple** - Status code, response
        """
        payload = {
            "data": {
                "attributes": {
                    "username": username,
                    "email": email,
                    "password": password,
                    "isEmailConfirmed": is_email_confirmed,
                }
            }
        }

        r = self.session.post(
            self.url,
            headers=authorization_header(token, user_id),
            json=payload,
        )
        return (r.status_code, r.json())

    def show(self, user_id: int) -> tuple[int, dict[Any, Any]]:
        """
        Get a single user.

        **Parameters:**

        * **user_id** - ID of the user to retrieve.

        **Returns:**

        * **tuple** - Status code, response
        """
        r = self.session.get(f"{self.url}/{user_id}")
        return (r.status_code, r.json())

    def update(
        self,
        user_id: int,
        token: str,
        attributes: Optional[dict[Any, Any]] = {},
        relationships: Optional[dict[Any, Any]] = {},
    ) -> tuple[int, dict[Any, Any]]:
        """
        Edit a user.
        """
        payload = {
            "data": {
                "attributes": attributes,
                "relationships": relationships
            }
        }

        r = self.session.patch(
            f"{self.url}/{user_id}",
            headers=authorization_header(token),
            json=payload
        )
        return (r.status_code, r.json())

    def delete(self, user_id: int) -> tuple[int, dict[Any, Any]]:
        """
        Delete a user.
        """
        r = self.session.delete(f"{self.url}/{user_id}")
        return (r.status_code, r.json())

    def upload_avatar(self, user_id: int) -> tuple[int, dict[Any, Any]]:
        """
        Upload avatar.
        """
        r = self.session.post(f"{self.url}/{user_id}/avatar")
        return (r.status_code, r.json())

    def delete_avatar(self, user_id: int) -> tuple[int, dict[Any, Any]]:
        """
        Delete avatar.
        """
        r = self.session.delete(f"{self.url}/{user_id}/avatar")
        return (r.status_code, r.json())

    def send_confirmation_email(self, user_id: int) -> tuple[int, dict[Any, Any]]:
        """
        Send confirmation email.
        """
        r = self.session.post(f"{self.url}/{user_id}")
        return (r.status_code, r.json())
