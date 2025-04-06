import time
from contextlib import asynccontextmanager
from typing import AsyncIterator

import sentry_sdk
from fastapi import FastAPI
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.staticfiles import StaticFiles

from src.config.app import app_settings
from src.config.sentry import sentry_settings
from src.config.telegram import telegram_settings
from src.infrastructure.aiogram.tg_bot import AiogramManager
from src.ui.htmx import router as htmx_router
from src.ui.rest_api import router as rest_api_router
from src.ui.tg_api import router as tg_api_router


@asynccontextmanager
async def lifespan(app_: FastAPI) -> AsyncIterator[None]:  # noqa: ARG001
    # Database healthcheck
    from src.infrastructure.database.base import engine
    from src.infrastructure.database.healthcheck import healthcheck as db_healthcheck
    await db_healthcheck()

    # Create the bot and dispatcher
    aiogram_manager = AiogramManager()
    await aiogram_manager.init(app_, app_settings.URL + telegram_settings.WEBHOOK_PATH)
    aiogram_manager.dp.include_router(tg_api_router)

    try:
        yield
    finally:
        # Shutdown events
        await engine.dispose()  # Clean up the connection pool
        await aiogram_manager.shutdown()  # Close the aiohttp session


def create_app() -> FastAPI:
    sentry_sdk.init(
        dsn=sentry_settings.DSN,
        # Add data like request headers and IP for users,
        # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
        send_default_pii=True,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=sentry_settings.TRACES_SAMPLE_RATE,
    )

    app_ = FastAPI(
        title="AnoCat",
        version=app_settings.get_version(),
        lifespan=lifespan,
        docs_url=None if app_settings.ENVIRONMENT == 'production' else "/docs",
        redoc_url=None if app_settings.ENVIRONMENT == 'production' else "/redoc",
        openapi_url=None if app_settings.ENVIRONMENT == 'production' else "/openapi.json",
    )

    app_.mount("/static", StaticFiles(directory="static"), name="static")

    app_.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=[],
    )

    @app_.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        response.headers["X-Process-Time"] = str(int((time.perf_counter() - start) * 1000))
        return response

    app_.get("/metrics")(lambda _: Response(status_code=status.HTTP_204_NO_CONTENT))

    app_.include_router(htmx_router)
    app_.include_router(rest_api_router)

    return app_
