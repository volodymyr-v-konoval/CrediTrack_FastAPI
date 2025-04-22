from datetime import date
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from src.models.plan_model import Plan
from src.schemas.plans_schema import PlanCreate


class PlanRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_period_and_category(self, period: date, category_id: int) -> Optional[Plan]:
        result = await self.session.execute(
            select(Plan).where(and_(Plan.period == period, Plan.category_id == category_id))
        )
        return result.scalar_one_or_none()
    
    async def create_many(self, plans: list[Plan]) -> None:
        self.session.add_all(plans)
        await self.session.commit()

    async def exists(self, period, category_id) -> bool:
        stmt = select(Plan).where(
            and_(
                Plan.period == period,
                Plan.category_id == category_id
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None
    
    async def create(self, plan: PlanCreate) -> Plan:
        new_plan = Plan(**plan.dict())
        self.session.add(new_plan)
        await self.session.commit()
        await self.session.refresh(new_plan)
        return new_plan
        
