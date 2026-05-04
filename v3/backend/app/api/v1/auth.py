"""Authentication endpoints."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import (
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
    hash_password,
    verify_password,
)
from app.models.tenant import Tenant
from app.models.user import User
from app.schemas.auth import (
    CurrentUser,
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenPair,
)
from app.schemas.common import MessageResponse

router = APIRouter()


@router.post("/register", response_model=CurrentUser, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)) -> CurrentUser:
    existing = await db.execute(select(User).where(User.email == payload.email))
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status_code=400, detail="Email already registered")

    tenant_id: UUID | None = None
    if payload.tenant_slug:
        tenant = (
            await db.execute(select(Tenant).where(Tenant.slug == payload.tenant_slug))
        ).scalar_one_or_none()
        if tenant is None:
            raise HTTPException(status_code=404, detail="Tenant not found")
        tenant_id = tenant.id

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        full_name=payload.full_name,
        role="client",
        tenant_id=tenant_id,
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return CurrentUser.model_validate(user, from_attributes=True)


@router.post("/login", response_model=TokenPair)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)) -> TokenPair:
    user = (
        await db.execute(select(User).where(User.email == payload.email))
    ).scalar_one_or_none()
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is inactive")

    user.last_login_at = datetime.now(timezone.utc)
    await db.commit()

    extra = {"role": user.role, "tenant_id": str(user.tenant_id) if user.tenant_id else None}
    return TokenPair(
        access_token=create_access_token(str(user.id), extra_claims=extra),
        refresh_token=create_refresh_token(str(user.id)),
    )


@router.post("/refresh", response_model=TokenPair)
async def refresh(payload: RefreshRequest, db: AsyncSession = Depends(get_db)) -> TokenPair:
    claims = decode_token(payload.refresh_token)
    if claims.get("type") != REFRESH_TOKEN_TYPE:
        raise HTTPException(status_code=401, detail="Wrong token type")
    sub = claims.get("sub")
    if not sub:
        raise HTTPException(status_code=401, detail="Invalid subject")
    user = (
        await db.execute(select(User).where(User.id == UUID(sub)))
    ).scalar_one_or_none()
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found")
    extra = {"role": user.role, "tenant_id": str(user.tenant_id) if user.tenant_id else None}
    return TokenPair(
        access_token=create_access_token(str(user.id), extra_claims=extra),
        refresh_token=create_refresh_token(str(user.id)),
    )


@router.post("/logout", response_model=MessageResponse)
async def logout(_user: User = Depends(get_current_user)) -> MessageResponse:
    # Stateless JWT: real revocation belongs in Redis blacklist; placeholder.
    return MessageResponse(message="Logged out")


@router.get("/me", response_model=CurrentUser)
async def me(user: User = Depends(get_current_user)) -> CurrentUser:
    return CurrentUser.model_validate(user, from_attributes=True)
