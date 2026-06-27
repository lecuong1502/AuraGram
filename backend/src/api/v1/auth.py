from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, RefreshRequest
from src.services import auth as auth_service
from src.core.dependencies import get_current_user
from src.models import User

router = APIRouter(prefix="/auth", tags=["Auth"])
bearer = HTTPBearer()

@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(data: RegisterRequest):
    return await auth_service.register(data)

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest):
    return await auth_service.login(data)

@router.post("/refresh", response_model=TokenResponse)
async def refresh(data: RefreshRequest):
    return await auth_service.refresh(data.refresh_token)

@router.post("/logout", status_code=204)
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    current_user: User = Depends(get_current_user),
):
    await auth_service.logout(current_user, credentials.credentials)