from datetime import date

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from conf.config import Base


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, 
                                    autoincrement=True)
    sum: Mapped[float] = mapped_column(Numeric(10, 2))
    payment_date: Mapped[date]
    credit_id: Mapped[int] = mapped_column(ForeignKey("credits.id"),
                                           nullable=False)
    type_id: Mapped[int] = mapped_column(ForeignKey("dictionary.id"),
                                         nullable=False)
    