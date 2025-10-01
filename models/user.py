from sqlalchemy.orm import Mapped, relationship

from database import Base, uniq_str_field


class User(Base):
    username: Mapped[uniq_str_field]
    email: Mapped[uniq_str_field]
    password: Mapped[str]

    # Связь один-к-одному с Profile
    profile: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="user",
        uselist=False,  # Обеспечивает связь один-к-одному
        lazy="joined"   # Автоматически загружает связанные данные из Profile при запросе User
    )

    # Связь один-ко-многим с Post
    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="user",
        cascade="all, delete-orphan"  # При удалении User удаляются и связанные Post
    )

    # Связь один-ко-многим с Comment
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="user",
        cascade="all, delete-orphan"  # При удалении User удаляются и связанные Comment
    )

