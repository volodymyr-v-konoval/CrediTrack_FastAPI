from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.plan_service import PlanService
from database.db import get_db
from conf import messages

router = APIRouter(prefix="/plans", tags=["Plans"])


@router.post("/")
async def insert_plans(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_db)
):
    plan_service = PlanService(session)
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, 
                            detail=messages.WRONG_EXCEL_FORMAT)
    try:
        await plan_service.insert_from_excel(file)
        return JSONResponse(content={"detail": "Plans inserted successfully"})
    except ValueError as e:
        raise HTTPException(status_code=400, datail=str(e))
    
