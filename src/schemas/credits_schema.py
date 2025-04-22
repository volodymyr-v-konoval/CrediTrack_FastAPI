import math
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Optional, List, Union


class CreditBase(BaseModel):
    user_id: int
    issuance_date: date
    return_date: date
    actual_return_date: Optional[date]
    body: float
    percent: float


class CreditCreate(BaseModel):
    user_id: int
    issuance_date: date
    return_date: date
    actual_return_date: Optional[date]
    body: float
    percent: float

    @model_validator(mode='before')
    def parse_dates(cls, values):
        for date_field in ['issuance_date', 'return_date', 'actual_return_date']:
            field_value = values.get(date_field)

            if field_value is None or (isinstance(field_value, float) and math.isnan(field_value)):  
                values[date_field] = None  
                continue

            if isinstance(field_value, str):
                try:
                    values[date_field] = datetime.strptime(field_value, '%d.%m.%Y').date()
                except ValueError:
                    raise ValueError(f"Invalid date format for {date_field}. Expected format: dd.mm.yyyy.")
            elif isinstance(field_value, date):
                values[date_field] = field_value.strftime('%d.%m.%Y')

        return values
        
    
class CreditInDB(CreditBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ClosedCreditInfo(BaseModel):
    user_id: int
    issuance_date: date
    is_closed: bool = Field(default=True)
    actual_return_date: Optional[date] = None
    body: float
    percent: float
    total_payment: float


class OpenCreditInfo(BaseModel):
    user_id: int
    issuance_date: date
    is_closed: bool = Field(default=False)
    return_date: date
    overdue_days: int
    body: float
    percent: float
    principal_payment: float
    interest_payment: float


class CreditResponse(BaseModel):
    user_id: int
    credits: List[Union[ClosedCreditInfo, OpenCreditInfo]]
    