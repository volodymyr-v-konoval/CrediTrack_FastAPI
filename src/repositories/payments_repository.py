from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.models.payment_model import Payment
from src.models.dictionary_model import Dictionary
from src.schemas.payments_schema import PaymentCreate

class PaymentRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_credit_id(self, credit_id: int) -> list[Payment]:
        result = await self.session.execute(select(Payment).where(Payment.credit_id == credit_id))
        return result.scalars().all()
    
    
    async def get_total_by_credit_id(self, credit_id: int) -> float:
        stmt = select(func.sum(Payment.sum)).where(Payment.credit_id == credit_id)
        result = await self.session.execute(stmt)
        return result.scalar() or 0.0
    
    async def get_sum_by_type(self, credit_id: int, type_name: str) -> float:
        subquery = select(Dictionary.id).where(Dictionary.name == type_name).scalar_subquery()
        stmt = select(func.sum(Payment.sum)).where(
            Payment.credit_id == credit_id,
            Payment.type_id == subquery
        )
        result = await self.session.execute(stmt)
        return result.scalar() or 0.0
    
    async def create(self, payment_create: PaymentCreate) -> Payment:
        # existing_payment = await self.session.execute(
        #     select(Payment).where(
        #         Payment.credit_id == payment_create.credit_id,
        #         Payment.payment_date == payment_create.payment_date,
        #         Payment.type_id == payment_create.type_id,
        #         Payment.sum == payment_create.sum
        #     )
        # )
        # existing_payment = existing_payment.scalar_one_or_none()

        # if existing_payment:
        #     raise ValueError(
        #         f"Payment for credit_id {payment_create.credit_id} for {payment_create.sum} with date {payment_create.payment_date} and type_id {payment_create.type_id} already exists."
        #     )

        payment = Payment(
            sum=payment_create.sum,
            payment_date=payment_create.payment_date,
            credit_id=payment_create.credit_id,
            type_id=payment_create.type_id
        )

        self.session.add(payment)

        try:
            await self.session.commit()
            await self.session.refresh(payment)
        except IntegrityError:
            await self.session.rollback()
            raise ValueError(
                f"Error creating payment for credit_id {payment_create.credit_id} with date {payment_create.payment_date}."
            )

        return payment
