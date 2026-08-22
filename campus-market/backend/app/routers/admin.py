"""管理员路由：全量管理、审核、下架、删除。"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..deps import require_admin
from ..models import Listing, User
from ..schemas import ListingOut
from .listings import to_listing_out

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/listings", response_model=list[ListingOut])
def admin_listings(
    status: str = "",
    user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    query = db.query(Listing).options(joinedload(Listing.seller))
    if status:
        query = query.filter(Listing.status == status)
    items = query.order_by(Listing.created_at.desc()).all()
    return [to_listing_out(x) for x in items]


@router.post("/listings/{listing_id}/approve")
def approve(
    listing_id: int,
    user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    listing = db.get(Listing, listing_id)
    if listing is None:
        raise HTTPException(404, "商品不存在")
    listing.status = "active"
    listing.is_flagged = False
    db.commit()
    return {"ok": True}


@router.post("/listings/{listing_id}/delist")
def delist(
    listing_id: int,
    user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    listing = db.get(Listing, listing_id)
    if listing is None:
        raise HTTPException(404, "商品不存在")
    listing.status = "delisted"
    db.commit()
    return {"ok": True}


@router.delete("/listings/{listing_id}")
def delete(
    listing_id: int,
    user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    listing = db.get(Listing, listing_id)
    if listing is None:
        raise HTTPException(404, "商品不存在")
    db.delete(listing)
    db.commit()
    return {"ok": True}
