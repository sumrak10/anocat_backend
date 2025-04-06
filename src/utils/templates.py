import datetime
import random
from typing import Any

from urllib.parse import quote
from zoneinfo import ZoneInfo

from starlette.templating import Jinja2Templates

from src.config.app import app_settings


def static_url(path: str, add_hash: bool = False) -> str:
    # static_hash = "".join(random.choices("abcdef0123456789", k=8))
    link = f"/static{quote(path)}"
    if add_hash:
        link = f"{link}?v={app_settings.get_version_hash()}"
    return link


MONTHS_RU = {
        1: "Янв", 2: "Фев", 3: "Мар", 4: "Апр", 5: "Май", 6: "Июн",
        7: "Июл", 8: "Авг", 9: "Сен", 10: "Окт", 11: "Ноя", 12: "Дек"
    }


def humanize_datetime_ru(value: datetime.datetime, current_user_tz: str) -> str:
    if not value.tzinfo:
        value = value.replace(tzinfo=datetime.UTC)
    value = value.astimezone(ZoneInfo(current_user_tz))
    utcnow = datetime.datetime.now(datetime.UTC)

    year_str = ""
    if value.year != utcnow.year:
        year_str = f" {value.year} "
    return f"{value.day} {MONTHS_RU[value.month]}" + year_str + f" в {value.strftime('%H:%M')}"


templates = Jinja2Templates(directory="templates")
templates.env.globals["static_url"] = static_url
templates.env.globals["humanize_datetime_ru"] = humanize_datetime_ru


def render_template(
    template: str,
    context: dict[str, Any],
) -> templates.TemplateResponse:
    return templates.TemplateResponse(
        template,
        context,
    )

