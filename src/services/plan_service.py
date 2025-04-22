import pandas as pd
from io import BytesIO
from fastapi import HTTPException, UploadFile
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from conf import messages
from src.repositories.dictionaries_repository import DictionaryRepository
from src.repositories.plans_repository import PlanRepository
from src.schemas.plans_schema import PlanCreate



class PlanService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.plan_repo = PlanRepository(session)
        self.dict_repo = DictionaryRepository(session)

    async def insert_from_excel(self, file: UploadFile):
        file_bytes = await file.read()
        
        df = pd.read_excel(BytesIO(file_bytes))

        df['period'] = pd.to_datetime(df['period'], format='%d.%m.%Y')

        required_columns = ["period", "name", "sum"]
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(status_code=400, detail=messages.MUST_CONTAIN_COLUMNS)
        
        inserted = 0

        for _, row in df.iterrows():
            try:
                period = pd.to_datetime(row["period"])
            except Exception:
                raise HTTPException(status_code=400, datail=messages.WRONG_DATE_FORMAT)
            
            if df['period'].iloc[0].day != 1:
                raise HTTPException(status_code=400, detail=messages.MONTHS_FIRST_DATE)
            
            if pd.isnull(row["sum"]):
                raise HTTPException(status_code=400, detail=messages.SUM_CAN_NOT_BE_NULL)
            
            name = row["name"]
            category = await self.dict_repo.get_by_name(name)

            if not category:
                raise HTTPException(status_code=400, detail=f"Category '{name}' did not found in Dictionary!")
            
            exists = await self.plan_repo.exists(period, category.id)
            if exists:
                raise HTTPException(status_code=400, detail=f"Plan for {period.strftime('%Y-%m')} and '{name}' category already exists!")
            
            plan = PlanCreate(
                period=period,
                sum=float(row["sum"]),
                category_id=category.id
            )
            await self.plan_repo.create(plan)
            inserted += 1

        return {"message": f"Successfully added {inserted} entries."}
    
