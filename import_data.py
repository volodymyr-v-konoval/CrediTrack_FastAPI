import csv
import asyncio
from contextlib import asynccontextmanager
import pandas as pd
from database.db import get_db
from src.schemas.users_schema import UserCreate
from src.schemas.credits_schema import CreditCreate
from src.schemas.dictionary_schema import DictionaryCreate
from src.schemas.payments_schema import PaymentCreate
from src.schemas.plans_schema import PlanCreate
from src.repositories.users_repository import UserRepository
from src.repositories.credits_repository import CreditRepository
from src.repositories.dictionaries_repository import DictionaryRepository
from src.repositories.payments_repository import PaymentRepository
from src.repositories.plans_repository import PlanRepository


@asynccontextmanager
async def get_async_session():
    async for session in get_db():
        yield session

        
async def import_credits(session):
    df = pd.read_csv("data/credits.csv", sep='\t')
    service = CreditRepository(session)
    for _, row in df.iterrows():
        data = CreditCreate(**row.to_dict())
        try:
            await service.create(data)
        except ValueError as e:
            print(f"Error: {e}. Skipping credit for user_id {data.user_id} with return_date {data.return_date} already exists.")
        except Exception as e:
            print(f"Unexpected error: {e}. Skipping credit for user_id {data.user_id} with return_date {data.return_date}.")


async def import_users(session):
    df = pd.read_csv("data/users.csv", sep='\t')
    service = UserRepository(session)
    for _, row in df.iterrows():
        data = UserCreate(**row.to_dict())
        try:
            await service.create(data)
        except ValueError as e:
            print(f"Error: {e}. Skipping user with login {data.login}.")
        except Exception as e:
            print(f"Unexpected error: {e}. Skipping user with login {data.login}.")


async def import_dictionary(session):
    df = pd.read_csv("data/dictionary.csv", sep='\t')
    service = DictionaryRepository(session)
    for _, row in df.iterrows():
        data = DictionaryCreate(**row.to_dict())
        await service.create(data)


async def import_payments(session):
    df = pd.read_csv("data/payments.csv", sep='\t')
    service = PaymentRepository(session)
    
    for index, row in df.iterrows():
        try:
            data = PaymentCreate(**row.to_dict())
            await service.create(data)
        except ValueError as e:
            print(f"[{index}] Skipped: {e}")
        except Exception as e:
            print(f"[{index}] Unexpected error: {e}")


async def import_plans(session):
    df = pd.read_csv("data/plans.csv", sep='\t')
    service = PlanRepository(session)
    for _, row in df.iterrows():
        data = PlanCreate(**row.to_dict())
        await service.create(data)


async def main():
    async with get_async_session() as session:
        await import_users(session)
        await import_credits(session)
        await import_dictionary(session)
        await import_payments(session)
        await import_plans(session)
        print("All data imported seccessfully to the database!")


if __name__ == "__main__":
    asyncio.run(main())
