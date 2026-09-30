from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "FitBuddy")


def get_settings() -> Settings:
    return Settings()
