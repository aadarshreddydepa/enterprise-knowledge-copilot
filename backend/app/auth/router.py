from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.dependencies import get_current_user
from app.db.session import AsyncSessionLocal
from app.auth.schemas import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
)
from app.db.models.user import User
from app.auth.service import register_user, authenticate_user

from app.auth.permissions import require_roles
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


@router.get("/me")
async def read_me(current_user: User = Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "full_name": current_user.full_name,
    }

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Enterprise Copilot API"}


@router.get("/admin/health")
async def admin_health(
    user = Depends(require_roles("admin"))
):
    return {
        "status": "ok",
        "user": user.email,
        "roles": user.roles,
    }


   
