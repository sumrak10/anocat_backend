from fastapi import APIRouter

from src.utils.exceptions import http_exc
from .avatars import router as avatars_router
from .mails import router as mails_router
from .users import router as users_router

router = APIRouter(
    prefix="/api/v1",
    responses={
        **http_exc.UnauthorizedHTTPException.docs(),
        **http_exc.ForbiddenHTTPException.docs(),
        **http_exc.NotFoundHTTPException.docs(),
    }
)

router.include_router(avatars_router)
router.include_router(users_router)
router.include_router(mails_router)
