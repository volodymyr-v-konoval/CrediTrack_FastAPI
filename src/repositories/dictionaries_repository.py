from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.dictionary_model import Dictionary
from src.schemas.dictionary_schema import DictionaryCreate


class DictionaryRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, dict_id: int) -> Optional[Dictionary]:
        result = await self.session.execute(select(Dictionary).where(Dictionary.id == dict_id))
        return result.scalar_one_or_none
    
    async def get_by_name(self, name: str) -> Optional[Dictionary]:
        result = await self.session.execute(select(Dictionary).where(Dictionary.name == name))
        return result.scalar_one_or_none()
    
    async def get_all(self) -> list[Dictionary]:
        result = await self.session.execute(select(Dictionary))
        return result.scalars().all()
    
    async def create(self, dictionary_create: DictionaryCreate) -> Dictionary:
        result = await self.session.execute(select(Dictionary).where(Dictionary.name == dictionary_create.name))
        existing_dictionary = result.scalar_one_or_none() 
        
        if existing_dictionary:
            raise ValueError(f"Dictionary with name {dictionary_create.name} already exists.")
        
        dictionary = Dictionary(
            name=dictionary_create.name
        )
        self.session.add(dictionary)
        try:
            await self.session.commit()
            await self.session.refresh(dictionary)
        except IntegrityError:
            await self.session.rollback()
            raise ValueError(f"Error creating dictionary with name {dictionary_create.name}.")
        
        return dictionary