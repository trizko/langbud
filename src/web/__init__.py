from .api import setup_api_routes
from .discord import setup_discord_routes
from .routes import setup_web_routes


__all__ = [
    "setup_api_routes",
    "setup_discord_routes",
    "setup_web_routes",
]