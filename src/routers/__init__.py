from .api import setup_api_routes
from .discord import setup_discord_routes
from .static import setup_static_routes


__all__ = [
    "setup_api_routes",
    "setup_discord_routes",
    "setup_static_routes",
]