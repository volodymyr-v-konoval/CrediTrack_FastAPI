from pydantic import BaseModel, ConfigDict, field_validator
from datetime import date
from decimal import Decimal


class PaymentBase(BaseModel):
    sum: float
    payment_date: date
    credit_id: int
    type_id: int


class PaymentCreate(BaseModel):
    sum: Decimal
    payment_date: date
    credit_id: int
    type_id: int

    @field_validator("payment_date", mode="before")
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, str):
            from datetime import datetime
            return datetime.strptime(value, "%d.%m.%Y").date()
        return value

    model_config = {
        "str_strip_whitespace": True
    }

class PaymentInDB(PaymentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
        