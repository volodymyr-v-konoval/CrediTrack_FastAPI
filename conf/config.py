from functools import cached_property
from pathlib import Path

from pydantic import ConfigDict, field_validator
from pydantic_settings import BaseSettings
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Settings(BaseSettings):
    # Database settings
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_HOST: str

    @cached_property
    def DB_URL(self) -> str:
        return (
            f"mysql+asyncmy://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}/{self.DATABASE_NAME}"
            )



    BASE_DIR: Path | None = Path(__file__).parent.parent

    model_config = ConfigDict(
        extra="ignore", 
        env_file=str(BASE_DIR / ".env"), 
        env_file_encoding="utf-8"
    )

app_config = Settings()
