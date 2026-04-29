import uuid
from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from application.infrastructure.postgress.database import Base


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, nullable=False, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    pub_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )
    location_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey('locations.id', ondelete='SET NULL'),
        nullable=True,
    )
    category_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey('categories.id', ondelete='SET NULL'),
        nullable=True,
    )
    image_url: Mapped[str | None] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    is_published: Mapped[bool] = mapped_column(nullable=False, default=True)
