from typing import Any, Optional, Union

from httpx import delete as httpx_delete
from httpx import get as httpx_get
from httpx import patch as httpx_patch
from httpx import post as httpx_post


class DiscussionsRoute:
    def __init__(self, url: str, master_key: Optional[str] = None) -> None:
        self.url = f"{url}/api/discussions"
        self.master_key = master_key

    def __get_authorization_header(self, user_id: int) -> dict[Any, Any]:
        """
        Builds authorization header
        """
        return {"Authorization": f"Token {self.master_key}; userId={user_id}"}

    def index(self) -> dict[Any, Any]:
        """
        List discussions.
        """
        r = httpx_get(self.url)
        response: dict[Any, Any] = r.json()
        return response

    def create(
        self,
        title: str,
        content: str,
        tags: list[int] = [],
        user_id: int = 1,
    ) -> tuple[int, dict[Any, Any]]:
        """
        Create a discussion.

        **Parameters:**

        * **user_id** - ID of the user to impersonate.
        * **title** - Title of the discussion.
        * **content** - Content of the discussion.
        * **tags** - List of tags to associate to the discussion.

        **Returns:**

        * **tuple** - Status code, Response

        * Requires master key
        """
        discussion_tags = []
        for i in tags:
            discussion_tags.append({"id": i, "type": "tags"})

        json = {
            "data": {
                "attributes": {
                    "content": content,
                    "title": title,
                },
                "relationships": {"tags": {"data": discussion_tags}},
                "type": "discussions",
            }
        }

        r = httpx_post(
            self.url, headers=self.__get_authorization_header(user_id), json=json
        )
        response: dict[Any, Any] = r.json()

        return (r.status_code, response)

    def show(self, discussion_id: int) -> tuple[int, dict[Any, Any]]:
        """
        Show a single discussion.

        **Parameters:**

        * **discussion_id** - ID of the discussion to fetch

        **Returns:**

        * **tuple** - Status code, response
        """
        r = httpx_get(f"{self.url}/{discussion_id}")
        response: dict[Any, Any] = r.json()
        return (r.status_code, response)

    def update(
        self,
        discussion_id: int,
        user_id: int = 1,
        title: Optional[str] = None,
        is_hidden: bool = False,
        is_locked: bool = False,
        is_sticky: bool = False,
        tags: Optional[list[int]] = None,
    ) -> tuple[int, dict[Any, Any]]:
        """
        Edit a discussion.

        **Parameters:**

        * **discussion_id** - ID of the discussion to update
        * **user_id** - ID of the user to impersonate
        * **title** - New title of the discussion
        * **is_hidden** - Hide or not the discussion
        * **is_locked** - Lock or not the discussion
        * **is_sticky** - Stick or not the discussion
        * **tags** - New list of tags for the discussion

        **Returns:**

        * **tuple** - Status code, response

        * Requires master key
        """
        discussion_tags = []
        if tags:
            for i in tags:
                discussion_tags.append({"type": "tags", "id": i})

        json = {
            "data": {
                "attributes": {
                    "title": title,
                    "isHidden": is_hidden,
                    "isLocked": is_locked,
                    "isSticky": is_sticky,
                },
                "relationships": {"tags": {"data": discussion_tags or tags}},
            }
        }

        r = httpx_patch(
            f"{self.url}/{discussion_id}",
            headers=self.__get_authorization_header(user_id),
            json=json,
        )

        return (r.status_code, r.json())

    def delete(
        self, discussion_id: int, user_id: int = 1
    ) -> tuple[int, dict[Any, Any]]:
        """
        Delete a discussion.

        **Parameters:**

        * **discussion_id** - ID of the discussion to delete
        * **user_id** - ID of the user to impersonate

        **Returns:**

        * **tuple** - Status code, response

        * Requires master key
        """
        r = httpx_delete(
            f"{self.url}/{discussion_id}",
            headers=self.__get_authorization_header(user_id),
        )
        response: dict[Any, Any] = r.json()

        return (r.status_code, response)
