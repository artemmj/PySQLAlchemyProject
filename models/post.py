from sqlalchemy import ForeignKey, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, array_or_none_field
from models.enums import StatusPostEnum
# from .user import User


class Post(Base):
    title: Mapped[str]
    content: Mapped[str]
    main_photo_url: Mapped[str]
    photos_url: Mapped[array_or_none_field]
    status: Mapped[StatusPostEnum] = mapped_column(
        default=StatusPostEnum.PUBLISHED,
        server_default=text("'DRAFT'"),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    # Связь многие-к-одному с User
    user: Mapped["User"] = relationship(
        "User",
        back_populates="posts"
    )

    # Связь один-ко-многим с Comment
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan"
    )
