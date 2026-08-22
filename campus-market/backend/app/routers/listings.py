"""商品路由：AI 分析、发布、列表、详情、状态、我的。"""
import re
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from ..ai import CATEGORIES, analyze_listing
from ..config import BASE_DIR, settings
from ..database import get_db
from ..deps import get_current_user
from ..models import Listing, User
from ..moderation import moderate_listing
from ..schemas import AnalyzeOut, ListingCreate, ListingOut, ListingPage, StatusIn

router = APIRouter(prefix="/api", tags=["listings"])

UPLOAD_DIR = BASE_DIR / settings.upload_dir
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def save_upload(file: UploadFile) -> str:
    UPLOAD_DIR.mkdir(exist_ok=True)
    ext = Path(file.filename or "img.jpg").suffix.lower()
    if ext not in ALLOWED_EXT:
        ext = ".jpg"
    name = f"{uuid.uuid4().hex}{ext}"
    (UPLOAD_DIR / name).write_bytes(file.file.read())
    return f"/uploads/{name}"


def abs_image_path(url_path: str) -> str:
    return str(UPLOAD_DIR / url_path.lstrip("/uploads/"))


def _num(v, default: float = 0.0) -> float:
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        m = re.search(r"\d+(\.\d+)?", v)
        if m:
            return float(m.group())
    return default


def _normalize_draft(d: dict) -> dict:
    tags = d.get("tags")
    if not isinstance(tags, list):
        tags = []
    tags = [str(t) for t in tags][:4]

    price_min = _num(d.get("price_min"))
    price_max = _num(d.get("price_max"))
    if price_max <= price_min:
        price_max = price_min + 1.0

    category = d.get("category")
    if category not in CATEGORIES:
        category = "其他"

    return {
        "title": str(d.get("title") or "二手好物").strip()[:120],
        "category": category,
        "condition": str(d.get("condition") or "成色未知"),
        "price_min": price_min,
        "price_max": price_max,
        "tags": tags,
        "valuation_note": str(d.get("valuation_note") or "").strip()[:200],
        "copy": str(d.get("copy") or "").strip(),
    }


def to_listing_out(x: Listing) -> ListingOut:
    return ListingOut(
        id=x.id,
        title=x.title,
        category=x.category,
        description=x.description,
        images=x.images or [],
        ai_condition=x.ai_condition,
        ai_tags=x.ai_tags or [],
        ai_copy=x.ai_copy,
        price_min=x.price_min,
        price_max=x.price_max,
        contact=x.contact,
        status=x.status,
        is_flagged=x.is_flagged,
        seller_id=x.seller_id,
        seller_name=x.seller.username if x.seller else None,
        created_at=x.created_at,
    )


@router.post("/ai/analyze", response_model=AnalyzeOut)
def analyze(files: list[UploadFile] = File(...), description: str = Form("")):
    if not 1 <= len(files) <= 3:
        raise HTTPException(400, "请上传 1-3 张图片")
    paths = [save_upload(f) for f in files]
    try:
        draft = _normalize_draft(
            analyze_listing([abs_image_path(p) for p in paths], description)
        )
    except Exception as exc:
        raise HTTPException(502, f"AI 分析失败：{exc}")
    return AnalyzeOut(images=paths, **draft)


@router.post("/listings", response_model=ListingOut)
def create_listing(
    data: ListingCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not data.images:
        raise HTTPException(400, "至少需要一张图片")
    images = data.images[:3]
    flagged, _ = moderate_listing(
        data.title, data.ai_copy, [abs_image_path(i) for i in images]
    )
    listing = Listing(
        title=data.title,
        category=data.category,
        description=data.description,
        images=images,
        ai_condition=data.ai_condition,
        ai_tags=data.ai_tags,
        ai_copy=data.ai_copy,
        price_min=data.price_min,
        price_max=data.price_max,
        contact=data.contact,
        status="pending" if flagged else "active",
        is_flagged=flagged,
        seller_id=user.id,
    )
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return to_listing_out(listing)


@router.get("/listings", response_model=ListingPage)
def list_listings(
    category: str = "",
    q: str = "",
    page: int = 1,
    page_size: int = 12,
    db: Session = Depends(get_db),
):
    query = (
        db.query(Listing)
        .options(joinedload(Listing.seller))
        .filter(Listing.status.in_(["active", "sold"]))
    )
    if category:
        query = query.filter(Listing.category == category)
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Listing.title.like(like), Listing.ai_copy.like(like)))
    total = query.count()
    items = (
        query.order_by(Listing.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return ListingPage(
        items=[to_listing_out(x) for x in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/listings/mine", response_model=list[ListingOut])
def my_listings(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    items = (
        db.query(Listing)
        .options(joinedload(Listing.seller))
        .filter(Listing.seller_id == user.id)
        .order_by(Listing.created_at.desc())
        .all()
    )
    return [to_listing_out(x) for x in items]


@router.get("/listings/{listing_id}", response_model=ListingOut)
def get_listing(listing_id: int, db: Session = Depends(get_db)):
    listing = db.get(Listing, listing_id)
    if listing is None:
        raise HTTPException(404, "商品不存在")
    return to_listing_out(listing)


@router.patch("/listings/{listing_id}/status", response_model=ListingOut)
def update_status(
    listing_id: int,
    data: StatusIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    listing = db.get(Listing, listing_id)
    if listing is None:
        raise HTTPException(404, "商品不存在")
    if user.role != "admin" and listing.seller_id != user.id:
        raise HTTPException(403, "无权操作该商品")
    if data.status not in ("sold", "delisted"):
        raise HTTPException(400, "无效状态")
    listing.status = data.status
    db.commit()
    db.refresh(listing)
    return to_listing_out(listing)
