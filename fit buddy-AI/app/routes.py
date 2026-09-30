from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(
    directory=str(Path(__file__).resolve().parent.parent / "templaters")
)
router = APIRouter()


@router.get("/", name="home")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )
