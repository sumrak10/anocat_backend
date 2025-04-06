from fastapi import APIRouter, Query
from starlette.requests import Request
from starlette.responses import HTMLResponse

from .users import router as users_router
from .mails import router as mails_router
from .stop_words import router as stop_words_router
from src.utils.templates import render_template


router = APIRouter()


router.include_router(users_router, prefix="/htmx/v1")
router.include_router(mails_router, prefix="/htmx/v1")
router.include_router(stop_words_router, prefix="/htmx/v1")


@router.get(
    path="/",
    response_class=HTMLResponse
)
async def index(
    request: Request,
    start_param: str | None = Query(None, alias="tgWebAppStartParam"),
):
    if start_param is not None:
        if start_param.startswith("mailto__"):
            try:
                mailto_user_id = int(start_param[8:])
            except ValueError:
                pass
            else:
                return render_template("pages/mailto.html", {
                    "request": request,
                    "mailto_user_id": mailto_user_id,
                    "max_mail_text_length": 512
                })
    return render_template("pages/index.html", {
        "request": request,
    })
