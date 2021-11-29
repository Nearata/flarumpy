from typing import Optional


def authorization_header(token: str, user_id: Optional[int] = None) -> dict[str, str]:
    """
    Builds authorization header.
    """
    return {"Authorization": f"Token {token}; userId={user_id}"}
