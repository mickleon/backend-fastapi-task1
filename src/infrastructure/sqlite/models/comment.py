import uuid
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.sqlite.database import Base


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )
    text: Mapped[str] = mapped_column(nullable=False)
    post_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('posts.id', ondelete='CASCADE'),
        nullable=False,
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='SET NULL'),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now
    )
