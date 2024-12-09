from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.exceptions.user import UserNotFoundException
from core.security import Encryptor
from lib.models.user import UserModel
from lib.schemas.user import UserCreateSchema, UserSchema


async def create_user(
    db: AsyncSession,
    *,
    schema: UserCreateSchema,
) -> UserSchema:
    hashed_password = Encryptor.hash_password(schema.password)
    user_model = UserModel(
        **schema.model_dump(exclude={"password"}),
        hashed_password=hashed_password,
    )
    db.add(user_model)
    await db.flush()
    return UserSchema.model_construct(**user_model.to_dict())


async def get_user_model_by_username(
    db: AsyncSession,
    *,
    username: str,
) -> UserModel:
    query = select(UserModel).where(UserModel.username == username)
    result = (await db.execute(query)).scalar_one_or_none()
    if result is None:
        raise UserNotFoundException
    return result


async def get_user_by_username(
    db: AsyncSession,
    *,
    username: str,
) -> UserSchema:
    user_model = await get_user_model_by_username(db, username=username)
    return UserSchema.model_construct(**user_model.to_dict())
