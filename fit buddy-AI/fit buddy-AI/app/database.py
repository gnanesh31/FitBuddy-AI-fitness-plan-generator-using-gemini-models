import sqlite3
from pathlib import Path

from .config import get_settings


def _sqlite_path(database_url: str) -> str:
    prefix = "sqlite:///"
    if not database_url.startswith(prefix):
        raise ValueError("Only SQLite DATABASE_URL values are supported")

    database_path = database_url[len(prefix):]
    if database_path == ":memory:":
        return database_path

    path = Path(database_path)
    if not path.is_absolute():
        path = Path(__file__).resolve().parent.parent / path
    path.parent.mkdir(parents=True, exist_ok=True)
    return str(path)


def init_db() -> None:
    with sqlite3.connect(_sqlite_path(get_settings().database_url)) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS fitness_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                plan_json TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )