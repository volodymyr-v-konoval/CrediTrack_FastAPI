from pydantic import BaseModel, ConfigDict


class DictionaryBase(BaseModel):
    name: str


class DictionaryCreate(DictionaryBase):
    pass


class DictionaryInDB(DictionaryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

