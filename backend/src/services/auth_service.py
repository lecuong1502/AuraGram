from fastapi import HTTPException, status
from src.models import User
from src.core.security import create_access_token, create_refresh_token, decode_token
from src.schemas.auth import RegisterRequest, LoginRequest, TokenResponse

async def register(data: RegisterRequest) -> TokenResponse:
    # Check for existing username / email
    if await User.find_one(User.username == data.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already taken")
    if await User.find_one(User.email == data.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = User(
        username=data.username,
        email=data.email,
        password_hash="",
        full_name=data.full_name,
    )
    user.set_password(data.password)

    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))
    user.refresh_tokens = [refresh_token]

    await user.insert()
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

async def login(data: LoginRequest) -> TokenResponse:
    user = await User.find_one(User.email == data.email).project(User)
    if not user or not user.verify_password(data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))

    # Rotate refresh tokens — keep max 5 active sessions
    user.refresh_tokens = ([refresh_token] + (user.refresh_tokens or []))[:5]
    await user.save()

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

async def refresh(token: str) -> TokenResponse:
    payload = decode_token(token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

    user = await User.get(payload["sub"])
    if not user or token not in (user.refresh_tokens or []):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked")

    access_token = create_access_token(str(user.id))
    new_refresh = create_refresh_token(str(user.id))

    # Rotate: replace old token with new one
    user.refresh_tokens = [new_refresh] + [t for t in user.refresh_tokens if t != token]
    await user.save()

    return TokenResponse(access_token=access_token, refresh_token=new_refresh)

async def logout(user: User, token: str) -> None:
    user.refresh_tokens = [t for t in (user.refresh_tokens or []) if t != token]
    await user.save()