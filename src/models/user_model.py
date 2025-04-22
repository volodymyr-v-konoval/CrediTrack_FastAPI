from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from conf.config import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String(50), unique=True,
                                       nullable=False)
    registration_date: Mapped[datetime] = mapped_column(DateTime,
                                                        nullable=False,
                                                        default=datetime.utcnow)
    
    