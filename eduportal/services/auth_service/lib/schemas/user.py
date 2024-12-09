from datetime import datetime

from .abc import BaseSchema


class BaseUserSchema(BaseSchema):
    username: str
    email: str


class UserCreateSchema(BaseUserSchema):
    password: str


class UserLoginSchema(BaseSchema):
    username: str
    password: str


class UserSchema(BaseUserSchema):
    id: int
    is_active: bool
    created_at: datetime
