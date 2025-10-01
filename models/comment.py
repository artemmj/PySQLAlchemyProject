from sqlalchemy import ForeignKey, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dao.database import Base
from models.enums import RatingEnum


class Comment(Base):
    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))
    is_published: Mapped[bool] = mapped_column(default=True, server_default=text("'false'"))
    rating: Mapped[RatingEnum] = mapped_column(default=RatingEnum.ZERO, server_default=text("'ZERO'"))

    # Связь многие-к-одному с User
    user: Mapped["User"] = relationship(
        "User",
        back_populates="comments"
    )

    # Связь многие-к-одному с Post
    post: Mapped["Post"] = relationship(
        "Post",
        back_populates="comments"
    )
