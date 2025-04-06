import logging

import aiohttp
from fastapi import APIRouter
from starlette.responses import Response

from src.config.telegram import telegram_settings
from src.utils.exceptions import http_exc

router = APIRouter(
    prefix="/avatars",
    tags=["Avatars"]
)
