from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.credit_model import Credit
from src.schemas.credits_schema import CreditCreate


class CreditRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_user_id(self, user_id: int) -> list[Credit]:
        result = await self.session.execute(select(Credit).where(Credit.user_id == user_id))
        return result.scalars().all()
    
    async def get_by_id(self, credit_id: int) -> Optional[Credit]:
        result = await self.session.execute(select(Credit).where(Credit.id == credit_id))
        return result.scalar_one_or_none()
    
    async def create(self, credit_create: CreditCreate) -> Credit: 
        existing_credit = await self.session.execute(
                select(Credit).where(Credit.user_id == credit_create.user_id, Credit.return_date == credit_create.return_date)
            )
        existing_credit = existing_credit.scalar_one_or_none()

        if existing_credit:
            raise ValueError(f"Credit for user_id {credit_create.user_id} with return_date {credit_create.return_date} already exists.")
            
        credit = Credit(
            user_id=credit_create.user_id,
            issuance_date=credit_create.issuance_date,
            return_date=credit_create.return_date,
            actual_return_date=credit_create.actual_return_date,
            body=credit_create.body,
            percent=credit_create.percent
        )

        self.session.add(credit)

        try:
            await self.session.commit()
            await self.session.refresh(credit)
        except IntegrityError:
            await self.session.rollback()
            raise ValueError(f"Error creating credit for user_id {credit_create.user_id} with return_date {credit_create.return_date}.")
        
        return credit    

    