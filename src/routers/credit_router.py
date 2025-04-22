from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.credit_service import CreditService
from src.schemas.credits_schema import CreditResponse
from database.db import get_db
from conf import messages

router = APIRouter(prefix="/credits", tags=["Credits"])


@router.get("/{user_id}", response_model=list[CreditResponse])
async def get_user_credits(user_id: int, 
                       session: AsyncSession = Depends(get_db)):
    credit_service = CreditService(session)
    result = await credit_service.get_user_credits(user_id)
    if not result:
        raise HTTPException(status_code=404, detail=messages.CREDITS_WARNING_NOT_FOUND)
    return result
