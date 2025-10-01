from sqlalchemy import JSON, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dao.database import Base, array_or_none_field
from models.enums import GenderEnum, ProfessionEnum


class Profile(Base):
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    age: Mapped[int | None]
    gender: Mapped[GenderEnum]
    profession: Mapped[ProfessionEnum] = mapped_column(
        default=ProfessionEnum.UNEMPLOYED,
        server_default=text("'UNEMPLOYED'")
    )
    interests: Mapped[array_or_none_field]
    contacts: Mapped[dict | None] = mapped_column(JSON)

    # Внешний ключ на таблицу users
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)

    # Обратная связь один-к-одному с User
    user: Mapped["User"] = relationship(
        "User",
        back_populates="profile",
        uselist=False
    )
