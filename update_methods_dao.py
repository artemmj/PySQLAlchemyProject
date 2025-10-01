import asyncio
from pydantic import EmailStr, create_model
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from dao.dao import ProfileDAO, UserDAO
from dao.session_maker import db_connection
from models import Profile


@db_connection(commit=True)
async def update_username(session: AsyncSession, user_id: int, username: str):
    ValueModel = create_model('ValueModel', username=(str, ...))
    await UserDAO.update_one_by_id(session=session, data_id=user_id, values=ValueModel(username=username))

# asyncio.run(update_username(user_id=1, username='aaaabbbbcccc'))


@db_connection(commit=True)
async def update_user(session: AsyncSession, user_id: int, username: str, email: int):
    ValueModel = create_model('ValueModel', username=(str, ...), email=(EmailStr, ...))
    await UserDAO.update_one_by_id(session=session, data_id=user_id, values=ValueModel(username=username, email=email))

# asyncio.run(update_user(user_id=1, email='admin@admin.ru', username='admin'))


@db_connection(commit=True)
async def update_age_mass(session: AsyncSession, new_age: int, last_name: str):
    try:
        stmt = (
            update(Profile)
            .filter_by(last_name=last_name)
            .values(age=new_age)
        )
        result = await session.execute(stmt)
        updated_count = result.rowcount
        print(f'Обновлено {updated_count} записей')
        return updated_count
    except SQLAlchemyError as e:
        print(f"Error updating profiles: {e}")
        raise

# asyncio.run(update_age_mass(new_age=22, last_name='Smith'))


@db_connection(commit=True)
async def update_age_mass_dao(session: AsyncSession, new_age: int, last_name: str):
    filter_criteria = create_model('FilterModel', last_name=(str, ...))
    values = create_model('ValuesModel', age=(int, ...))
    await ProfileDAO.update_many(
        session=session,
        filter_criteria=filter_criteria(last_name=last_name),
        values=values(age=new_age),
    )

asyncio.run(update_age_mass_dao(new_age=33, last_name='Smith'))
