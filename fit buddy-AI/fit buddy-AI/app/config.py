import os
from dataclasses import dataclass
from pathlib import Path


def _load_dotenv() -> None:
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.is_file():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"\''))


@dataclass(frozen=True)
class Settings:
    app_name: str
    database_url: str
    gemini_api_key: str
    workout_model: str
    fast_model: str
    admin_key: str
    app_env: str


def get_settings() -> Settings:
    _load_dotenv()
    return Settings(
        app_name=os.getenv("APP_NAME", "FitBuddy"),
        database_url=os.getenv("DATABASE_URL", "sqlite:///./fitbuddy.db"),
        gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
        workout_model=os.getenv("WORKOUT_MODEL", "gemini-3.1-pro"),
        fast_model=os.getenv("FAST_MODEL", "gemini-3-flash"),
        admin_key=os.getenv("ADMIN_KEY", ""),
        app_env=os.getenv("APP_ENV", "development"),
    )