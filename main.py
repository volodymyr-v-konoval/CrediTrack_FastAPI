from pathlib import Path

from fastapi import FastAPI

from src.common_services import healthchecker
from src.routers.credit_router import router as credit_router
from src.routers.plan_router import router as plan_router


BASE_DIR = Path(__file__).parent

app = FastAPI(title="Credit Manager API")


app.include_router(healthchecker.router,prefix="/api")
app.include_router(credit_router, prefix="/api")
app.include_router(plan_router, prefix="/api")
