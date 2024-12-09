from typing import Annotated, Any, AsyncGenerator

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from . import constructors as app_depends


def db_session_maker_stub() -> sessionmaker[Any]:
    raise NotImplementedError


async def db_session(
    request: Request,
    maker: Annotated[sessionmaker[Any], Depends(db_session_maker_stub)],
) -> AsyncGenerator[AsyncSession, None]:
    generator = app_depends.db_session_autocommit(maker)
    session = await anext(generator)
    request.state.db = session

    yield session

    try:
        await anext(generator)
    except StopAsyncIteration:
        pass
    else:
        raise RuntimeError("Database session not closed (db dependency generator is not closed).")


DatabaseDependency = Annotated[AsyncSession, Depends(db_session)]
