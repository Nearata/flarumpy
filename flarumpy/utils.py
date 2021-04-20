from typing import Any


def authorization_header(token: str, user_id: int) -> dict[Any, Any]:
    """
    Builds authorization header.
    """
    return {"Authorization": f"Token {token}; userId={user_id}"}
