from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.db.models.user import User
from app.core.security import hash_password, verify_password, create_access_token


async def register_user(
    session: AsyncSession,
    email: str,
    full_name: str,
    password: str,
) -> User:
    result = await session.execute(
        select(User).where(User.email == email)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user = User(
        email=email,
        full_name=full_name,
        password_hash=hash_password(password),
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


async def authenticate_user(
    session: AsyncSession,
    email: str,
    password: str,
) -> str:
    result = await session.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return create_access_token(subject=str(user.id))
