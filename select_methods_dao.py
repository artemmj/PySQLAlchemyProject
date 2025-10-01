from asyncio import run

from pydantic import EmailStr, create_model

from dao.dao import UserDAO
from dao.session_maker import db_connection
from schemas import UserSchema, UserIdAndUsernameSchema


@db_connection()
async def select_all_users(session):
    return await UserDAO.get_all_users(session)

# all_users = run(select_all_users())
# for user in all_users:
#     print(user.to_dict())
#     print(user.profile.to_dict() if user.profile else None)
#     print()

# all_users = run(select_all_users())
# for i in all_users:
#     user_pydantic = UserSchema.model_validate(i)
#     print(user_pydantic.model_dump())


@db_connection()
async def select_id_username(session):
    return await UserDAO.get_id_username(session)

# rez = run(select_id_username())
# for i in rez:
#     res = UserIdAndUsernameSchema.model_validate(i)
#     print(res.model_dump())


@db_connection()
async def select_full_user_info(session, user_id: int):
    rez = await UserDAO.get_user_info(session=session, user_id=user_id)
    if rez:
        return UserSchema.model_validate(rez).model_dump()
    return {'message': f'Пользователь с ID {user_id} не найден!'}

# info = run(select_full_user_info(user_id=1))
# print(info)
# info = run(select_full_user_info(user_id=3))
# print(info)
# info = run(select_full_user_info(user_id=1113))
# print(info)


@db_connection()
async def select_full_user_info(session, user_id: int):
    rez = await UserDAO.find_one_or_none_by_id(session=session, data_id=user_id)
    if rez:
        return UserSchema.model_validate(rez).model_dump()
    return {'message': f'Пользователь с ID {user_id} не найден!'}


@db_connection()
async def select_full_user_info_email(session, user_id: int, email: str):
    FilterModel = create_model(
        'FilterModel',
        id=(int, ...),
        email=(EmailStr, ...)
    )
    user = await UserDAO.find_one_or_none(session=session, filters=FilterModel(id=user_id, email=email))
    if user:
        # Преобразуем ORM-модель в Pydantic-модель и затем в словарь
        return UserSchema.model_validate(user).model_dump()
    return {'message': f'Пользователь с ID {user_id} не найден!'}

info = run(select_full_user_info_email(user_id=21, email='charlotte.scott@example.com'))
print(info)
