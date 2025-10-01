from typing import List
from pydantic import BaseModel, ConfigDict
from models.enums import GenderEnum, ProfessionEnum


class ProfileSchema(BaseModel):
    first_name: str
    last_name: str | None
    age: int | None
    gender: GenderEnum
    profession: ProfessionEnum
    interests: List[str] | None
    contacts: dict | None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class UserSchema(BaseModel):
    username: str
    email: str
    profile: ProfileSchema | None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class UserIdAndUsernameSchema(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)
