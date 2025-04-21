from sqlalchemy import String, Integer, Date, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

from conf.config import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, 
                                    primary_key=True,
                                    autoincrement=True)
    login: Mapped[str] = mapped_column(String(100), 
                                       unique=True,
                                       nullable=False)
    registration_date: Mapped[Date] = mapped_column(nullable=False)
    credits: Mapped[list["Credit"]] = relationship("Credit",
                                                   back_populates="user")
    
class Credit(Base):
    __tablename__ = "credits"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"),
                                         nullable=False)
    issuance_date: Mapped[Date] = mapped_column(nullable=False)
    return_date: Mapped[Date] = mapped_column(nullable=False)
    actual_return_date: Mapped[Date | None] = mapped_column(nullable=True)
    body: Mapped[float] = mapped_column(nullable=False)
    percent: Mapped[float] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship("User", 
                                        back_populates="credits")
    payments: Mapped[list["Payment"]] = relationship("Payment",
                                                     bask_populates="credit")
    

class Dictionary(Base):
    