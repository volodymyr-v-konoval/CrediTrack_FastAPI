from sqlalchemy import ForeignKey, Date, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from conf.config import Base
from datetime import date


class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(primary_key=True, 
                                    autoincrement=True)
    period: Mapped[date]
    sum: Mapped[float] = mapped_column(Numeric(10, 2))
    category_id: Mapped[int] = mapped_column(ForeignKey("dictionary.id"), 
                                             nullable=False)