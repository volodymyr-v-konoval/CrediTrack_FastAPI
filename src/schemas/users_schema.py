from pydantic import BaseModel, ConfigDict, model_validator
from datetime import datetime


class UserBase(BaseModel):
    login: str

class UserCreate(UserBase):
    registration_date: datetime

    @model_validator(mode='before')
    def parse_dates(cls, values):
        if isinstance(values.get('registration_date'), str):
            values['registration_date'] = datetime.strptime(values['registration_date'], '%d.%m.%Y')
        return values
    
class UserInDB(UserBase):
    id: int
    registration_data: datetime
    model_config = ConfigDict(from_attributes=True)
