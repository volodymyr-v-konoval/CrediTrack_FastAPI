from sqlalchemy import ForeignKey, Date, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from conf.config import Base


class Credit(Base):
    __tablename__ = "credits"

    id: Mapped[int] = mapped_column(primary_key=True, 
                                    autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"),
                                         nullable=False)
    issuance_date: Mapped[date]
    return_date: Mapped[date]
    actual_return_date: Mapped[date | None]
    body: Mapped[float] = mapped_column(Numeric(10, 2))
    percent: Mapped[float] = mapped_column(Numeric(10, 2))
    