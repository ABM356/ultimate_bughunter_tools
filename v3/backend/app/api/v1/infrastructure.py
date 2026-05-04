"""Infrastructure asset endpoints."""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import enforce_tenant, get_current_user
from app.models.asset import Asset
from app.models.user import User
from app.schemas.asset import AssetCreate, AssetRead, AssetUpdate
from app.schemas.common import MessageResponse

router = APIRouter()


@router.post("/assets", response_model=AssetRead, status_code=status.HTTP_201_CREATED)
async def create_asset(
    payload: AssetCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> AssetRead:
    asset = Asset(tenant_id=user.tenant_id, **payload.model_dump())
    db.add(asset)
    await db.commit()
    await db.refresh(asset)
    return AssetRead.model_validate(asset, from_attributes=True)


@router.get("/assets", response_model=list[AssetRead])
async def list_assets(
    asset_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[AssetRead]:
    stmt = select(Asset)
    if user.tenant_id is not None:
        stmt = stmt.where(Asset.tenant_id == user.tenant_id)
    if asset_type:
        stmt = stmt.where(Asset.asset_type == asset_type)
    rows = (await db.execute(stmt)).scalars().all()
    return [AssetRead.model_validate(a, from_attributes=True) for a in rows]


@router.get("/assets/{asset_id}", response_model=AssetRead)
async def get_asset(
    asset_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> AssetRead:
    asset = (
        await db.execute(select(Asset).where(Asset.id == asset_id))
    ).scalar_one_or_none()
    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    enforce_tenant(user, asset.tenant_id)
    return AssetRead.model_validate(asset, from_attributes=True)


@router.patch("/assets/{asset_id}", response_model=AssetRead)
async def update_asset(
    asset_id: UUID,
    payload: AssetUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> AssetRead:
    asset = (
        await db.execute(select(Asset).where(Asset.id == asset_id))
    ).scalar_one_or_none()
    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    enforce_tenant(user, asset.tenant_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(asset, field, value)
    await db.commit()
    await db.refresh(asset)
    return AssetRead.model_validate(asset, from_attributes=True)


@router.delete("/assets/{asset_id}", response_model=MessageResponse)
async def delete_asset(
    asset_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> MessageResponse:
    asset = (
        await db.execute(select(Asset).where(Asset.id == asset_id))
    ).scalar_one_or_none()
    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    enforce_tenant(user, asset.tenant_id)
    await db.delete(asset)
    await db.commit()
    return MessageResponse(message="Asset deleted")


@router.get("/iot")
async def iot_monitoring(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[AssetRead]:
    stmt = select(Asset).where(Asset.asset_type == "iot")
    if user.tenant_id is not None:
        stmt = stmt.where(Asset.tenant_id == user.tenant_id)
    rows = (await db.execute(stmt)).scalars().all()
    return [AssetRead.model_validate(a, from_attributes=True) for a in rows]


@router.get("/cctv")
async def cctv_monitoring(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[AssetRead]:
    stmt = select(Asset).where(Asset.asset_type == "cctv")
    if user.tenant_id is not None:
        stmt = stmt.where(Asset.tenant_id == user.tenant_id)
    rows = (await db.execute(stmt)).scalars().all()
    return [AssetRead.model_validate(a, from_attributes=True) for a in rows]


@router.get("/network-map")
async def network_map(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    stmt = select(Asset)
    if user.tenant_id is not None:
        stmt = stmt.where(Asset.tenant_id == user.tenant_id)
    assets = (await db.execute(stmt)).scalars().all()
    nodes = [
        {
            "id": str(a.id),
            "label": a.name,
            "type": a.asset_type,
            "criticality": a.criticality,
        }
        for a in assets
    ]
    return {"nodes": nodes, "edges": []}
