from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, field_validator


class PlanBase(BaseModel):
    period: date
    sum: float
    category_id: int

    @field_validator("period", mode="before")
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%d.%m.%Y").date()
        return value

    model_config = ConfigDict(str_strip_whitespace=True)


class PlanCreate(PlanBase):
    pass


class PlanInBD(PlanBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
