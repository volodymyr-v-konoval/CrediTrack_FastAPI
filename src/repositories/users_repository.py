from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.user_model import User
from src.schemas.users_schema import UserCreate


class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    async def get_all(self) -> list[User]:
        result = await self.session.execute(select(User))
        return result.scalars().all()
    
    async def create(self, user_create: UserCreate) -> User:
        existing_user = await self.session.execute(select(User).where(User.login == user_create.login))
        existing_user = existing_user.scalar_one_or_none()
        
        if existing_user:
            raise ValueError(f"User with login {user_create.login} already exists.")
        
        user = User(
            login=user_create.login,
            registration_date=user_create.registration_date
        )
        self.session.add(user)
        try:
            await self.session.commit()
            await self.session.refresh(user)
        except IntegrityError:
            await self.session.rollback()
            raise ValueError(f"Error creating user with login {user_create.login}.")
        
        return user
    