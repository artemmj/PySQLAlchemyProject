import asyncio

from pydantic import create_model
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from dao.dao import UserDAO
from dao.session_maker import connection
from models import User


@connection(commit=True)
async def delete_user_by_id(session: AsyncSession, user_id: int):
    user = await session.get(User, user_id)
    if user:
        await session.delete(user)

# asyncio.run(delete_user_by_id(user_id=5))


@connection(commit=True)
async def delete_user_by_id_dao(session: AsyncSession, user_id: int):
    await UserDAO.delete_one_by_id(session=session, data_id=user_id)

# asyncio.run(delete_user_by_id_dao(user_id=10))


@connection(commit=True)
async def delete_user_username_ja(session: AsyncSession, start_letter: str = 'ja'):
    stmt = delete(User).where(User.username.like(f"{start_letter}%"))
    await session.execute(stmt)

# asyncio.run(delete_user_username_ja())


@connection(commit=True)
async def delete_user_by_password(session: AsyncSession, password: str):
    filter_criteria = create_model('FilterModel', password=(str, ...))
    await UserDAO.delete_many(session=session, filters=filter_criteria(password=password))

asyncio.run(delete_user_by_password(password='asdasd'))
