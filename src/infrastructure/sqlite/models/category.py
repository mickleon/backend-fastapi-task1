import uuid
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.sqlite.database import Base


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, nullable=False, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    is_published: Mapped[bool] = mapped_column(nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now
    )
