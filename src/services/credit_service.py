from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from src.repositories.credits_repository import CreditRepository
from src.repositories.payments_repository import PaymentRepository
from src.schemas.credits_schema import CreditResponse


class CreditService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.credit_repo = CreditRepository(session)
        self.payment_repo = PaymentRepository(session)

    async def get_user_credits(self, user_id: int) -> CreditResponse:
        users_credits = await self.credit_repo.get_by_user_id(user_id)
        result = []

        for credit in users_credits:
            is_closed = credit.actual_return_date is not None
            credit_data = {
                "user_id": user_id,
                "issuance_date": credit.issuance_date,
                "is_closed": is_closed,
                "actual_return_date": credit.actual_return_date,
                "body": credit.body,
                "percent": credit.percent,
                "total_payment": credit.body + (credit.body * credit.percent / 100)
            }

            if is_closed:
                total_payments = await self.payment_repo.get_total_by_credit_id(credit.id)
                credit_data.update({
                    "total_payments": total_payments
                })
            else:
                today = date.today()
                overdue_days = max((today - credit.return_date).days, 0) if today > credit.return_date else 0
                body_payments = await self.payment_repo.get_sum_by_type(credit.id, "body")
                percent_payments = await self.payment_repo.get_sum_by_type(credit.id, "percents")

                credit_data.update({
                    "return_data": credit.return_date,
                    "overdue_days": overdue_days,
                    "body_payments": body_payments,
                    "percent_payments": percent_payments,
                })

            credit_data["credits"] = [credit_data]
            result.append(CreditResponse(**credit_data))



        return result
    
