from typing import Any, Optional

from httpx import Client

from ..utils import authorization_header


class DiscussionsRoute:
    def __init__(self, url: str, session: Client) -> None:
        self.url = f"{url}/discussions"
        self.session = session

    def index(self) -> tuple[int, dict[Any, Any]]:
        """
        List discussions.

        **Returns:**

        * **tuple** - Status code, Response
        """
        r = self.session.get(self.url)
        return (r.status_code, r.json())

    def create(
        self,
        master_key: str,
        title: str,
        content: str,
        tags: list[int] = [],
        user_id: int = 1,
    ) -> tuple[int, dict[Any, Any]]:
        """
        Create a discussion.

        **Parameters:**

        * **master_key** - Flarum API key.
        * **user_id** - ID of the user to impersonate.
        * **title** - Title of the discussion.
        * **content** - Content of the discussion.
        * **tags** - List of tags to associate to the discussion.

        **Returns:**

        * **tuple** - Status code, Response
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

        r = self.session.post(
            self.url,
            headers=authorization_header(master_key, user_id),
            json=json,
        )
        return (r.status_code, r.json())

    def show(self, discussion_id: int) -> tuple[int, dict[Any, Any]]:
        """
        Show a single discussion.

        **Parameters:**

        * **discussion_id** - ID of the discussion to fetch.

        **Returns:**

        * **tuple** - Status code, response
        """
        r = self.session.get(f"{self.url}/{discussion_id}")
        return (r.status_code, r.json())

    def update(
        self,
        master_key: str,
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

        * **master_key** - Flarum API key.
        * **discussion_id** - ID of the discussion to update.
        * **user_id** - ID of the user to impersonate.
        * **title** - New title of the discussion.
        * **is_hidden** - Hide or not the discussion.
        * **is_locked** - Lock or not the discussion.
        * **is_sticky** - Stick or not the discussion.
        * **tags** - New list of tags for the discussion.

        **Returns:**

        * **tuple** - Status code, response
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

        r = self.session.patch(
            f"{self.url}/{discussion_id}",
            headers=authorization_header(master_key, user_id),
            json=json,
        )

        return (r.status_code, r.json())

    def delete(
        self, master_key: str, discussion_id: int, user_id: int = 1
    ) -> tuple[int, dict[Any, Any]]:
        """
        Delete a discussion.

        **Parameters:**

        * **master_key** - Flarum API key.
        * **discussion_id** - ID of the discussion to delete.
        * **user_id** - ID of the user to impersonate.

        **Returns:**

        * **tuple** - Status code, response
        """
        r = self.session.delete(
            f"{self.url}/{discussion_id}",
            headers=authorization_header(master_key, user_id),
        )

        return (r.status_code, r.json())
