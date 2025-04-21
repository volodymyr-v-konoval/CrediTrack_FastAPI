from pathlib import Path

from fastapi import FastAPI

from src.services import healthchecker


BASE_DIR = Path(__file__).parent

app = FastAPI()


app.include_router(healthchecker.router,prefix="/api")
