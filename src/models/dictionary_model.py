from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from conf.config import Base

class Dictionary(Base):
    __tablename__ = "dictionary"

    id: Mapped[int] = mapped_column(primary_key=True, 
                                    autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
