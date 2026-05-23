import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.infrastructure.postgress.database import Base


class Image(Base):
    __tablename__ = 'images'

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, nullable=False, default=uuid.uuid4
    )
    post_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey('posts.id', ondelete='CASCADE'),
        nullable=True,
    )
    comment_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey('comments.id', ondelete='CASCADE'),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    post: Mapped['Post'] = relationship(back_populates='images')
    comment: Mapped['Comment'] = relationship(back_populates='images')
