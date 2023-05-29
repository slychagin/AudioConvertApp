from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    CookieTransport,
    JWTStrategy,
    AuthenticationBackend
)

from src.auth.manager import get_user_manager
from src.auth.models import User
from src.config import JWT_SECRET

# Cookies configuration to store stateful information into the user browser.
cookie_transport = CookieTransport(cookie_name="audio", cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    """Creating access tokens based on JSON"""
    return JWTStrategy(secret=JWT_SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
