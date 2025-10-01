from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dao.base import BaseDAO
from models import User, Profile, Post, Comment


class UserDAO(BaseDAO[User]):
    model = User

    @classmethod
    async def add_user_with_profile(cls, session: AsyncSession, user_data: dict) -> User:
        """
        Добавляет пользователя и привязанный к нему профиль.

        Аргументы:
        - session: AsyncSession - асинхронная сессия базы данных
        - user_data: dict - словарь с данными пользователя и профиля

        Возвращает:
        - User - объект пользователя
        """
        # Создаем пользователя из переданных данных
        user = cls.model(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
        session.add(user)
        await session.flush()  # Чтобы получить user.id для профиля

        # Создаем профиль, привязанный к пользователю
        profile = Profile(
            user_id=user.id,
            first_name=user_data['first_name'],
            last_name=user_data.get('last_name'),
            age=user_data.get('age'),
            gender=user_data['gender'],
            profession=user_data.get('profession'),
            interests=user_data.get('interests'),
            contacts=user_data.get('contacts')
        )
        session.add(profile)

        # Один коммит для обеих операций
        await session.commit()

        return user  # Возвращаем объект пользователя

    @classmethod
    async def get_all_users(cls, session: AsyncSession):
        # Создаем запрос для выборки всех пользователей
        query = select(cls.model)

        # Выполняем запрос и получаем результат
        result = await session.execute(query)

        # scalars() используется, когда мы ожидаем получить одну колонку результата
        # scalar() используется, когда мы ожидаем одну запись и одно поле
        # all() возвращает список всех записей, которые удовлетворяют нашему запросу
        # first() возвращает только первую запись из результатов запроса
        # scalar_one() — возвращает одно значение. Если запрос вернет более одной строки, произойдет ошибка
        # scalar_one_or_none() — вернет либо одно значение, либо None, если записей не найдено

        # Извлекаем записи как объекты модели
        records = result.scalars().all()

        # Возвращаем список всех пользователей
        return records

    @classmethod
    async def get_id_username(cls, session: AsyncSession):
        # Создаем запрос для выборки id и username всех пользователей
        query = select(cls.model.id, cls.model.username)  # Указываем конкретные колонки
        print(query)                                      # Выводим запрос для отладки
        result = await session.execute(query)             # Выполняем асинхронный запрос
        records = result.all()                            # Получаем все результаты
        return records                                    # Возвращаем список записей

    @classmethod
    async def get_user_info(cls, session: AsyncSession, user_id: int):
        query = select(cls.model).filter_by(id=user_id)
        # query = select(cls.model).filter(cls.model.id == user_id)
        result = await session.execute(query)
        user_info = result.scalar_one_or_none()
        return user_info

    @classmethod
    async def update_username_age_by_id(cls, session: AsyncSession, data_id: int, username: str, age: int):
        user = await session.get(cls.model, data_id)
        user.username = username
        user.profile.age = age
        await session.flush()


class ProfileDAO(BaseDAO[Profile]):
    model = Profile


class PostDAO(BaseDAO[Post]):
    model = Post


class CommentDAO(BaseDAO[Comment]):
    model = Comment
