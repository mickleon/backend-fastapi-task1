import uuid
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.sqlite.database import Base


class Location(Base):
    __tablename__ = 'locations'

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, nullable=False, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(nullable=False)

    is_published: Mapped[bool] = mapped_column(nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now
    )
