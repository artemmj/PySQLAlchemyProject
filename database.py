from datetime import datetime
from typing import Annotated, List

from sqlalchemy import ARRAY, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr, class_mapper
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from config import settings


DATABASE_URL = settings.get_db_url()

# Создаем асинхронный движок для работы с базой данных
engine = create_async_engine(url=DATABASE_URL)

# Создаем фабрику сессий для взаимодействия с базой данных
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


uniq_str_field = Annotated[str, mapped_column(unique=True)]
array_or_none_field = Annotated[List[str] | None, mapped_column(ARRAY(String))]


def db_connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                # Явно не открываем транзакции, так как они уже есть в контексте
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()  # Откатываем сессию при ошибке
                raise e                   # Поднимаем исключение дальше
            finally:
                await session.close()     # Закрываем сессию

    return wrapper


# Базовый класс для всех моделей
class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


    # Класс абстрактный, чтобы не создавать отдельную таблицу для него
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'

    def to_dict(self) -> dict:
        """Универсальный метод для конвертации объекта SQLAlchemy в словарь"""
        # Получаем маппер для текущей модели
        columns = class_mapper(self.__class__).columns
        # Возвращаем словарь всех колонок и их значений
        return {column.key: getattr(self, column.key) for column in columns}
