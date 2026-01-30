from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.auth.schemas import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
)
from app.auth.service import register_user, authenticate_user


router = APIRouter(prefix="/auth", tags=["auth"])


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.post("/register", status_code=201)
async def register(
    payload: UserRegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    await register_user(
        session=db,
        email=payload.email,
        full_name=payload.full_name,
        password=payload.password,
    )
    return {"message": "User registered successfully"}


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: UserLoginRequest,
    db: AsyncSession = Depends(get_db),
):
    token = await authenticate_user(
        session=db,
        email=payload.email,
        password=payload.password,
    )
    return TokenResponse(access_token=token)
