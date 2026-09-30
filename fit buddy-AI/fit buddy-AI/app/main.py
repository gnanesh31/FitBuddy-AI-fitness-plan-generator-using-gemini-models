from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import get_settings
from .database import init_db
from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown lifecycle.

    The SQLite database tables are created when
    the application starts.
    """

    init_db()

    yield


settings = get_settings()


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description=(
        "FitBuddy is an AI-powered fitness plan generator "
        "built with FastAPI, SQLite, SQLAlchemy, Jinja2, "
        "and Google Gemini."
    ),
    lifespan=lifespan,
)


# ---------------------------------------------------------
# STATIC FILES
# ---------------------------------------------------------
#
# This makes files inside:
#
# static/
#
# available through:
#
# /static/...
#
# For example:
#
# /static/styles.css
#

static_directory = Path(__file__).resolve().parent.parent / "static"
if static_directory.is_dir():
    app.mount(
        "/static",
        StaticFiles(directory=str(static_directory)),
        name="static",
    )


# ---------------------------------------------------------
# APPLICATION ROUTES
# ---------------------------------------------------------
#
# All application routes are defined in routes.py.
#

app.include_router(router)


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get("/health")
def health_check():
    """
    Simple endpoint used to verify that
    the FastAPI application is running.
    """

    return {
        "status": "ok",
        "service": settings.app_name,
        "version": "1.0.0",
    }