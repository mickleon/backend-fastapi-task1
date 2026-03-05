from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.sqlite.database import Base


class User(Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(primary_key=True, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(nullable=False)

    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)

    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)
