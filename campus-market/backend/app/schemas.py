"""Pydantic 请求 / 响应模型。"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# ---------- 鉴权 ----------
class RegisterIn(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=6, max_length=100)


class LoginIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    role: str

    model_config = {"from_attributes": True}


class TokenOut(BaseModel):
    token: str
    user: UserOut


# ---------- 商品 ----------
class ListingCreate(BaseModel):
    title: str
    category: str
    description: str = ""
    images: List[str] = []
    ai_condition: str = ""
    ai_tags: List[str] = []
    ai_copy: str = ""
    price_min: float = 0.0
    price_max: float = 0.0
    contact: str = ""


class ListingOut(BaseModel):
    id: int
    title: str
    category: str
    description: str
    images: List[str]
    ai_condition: str
    ai_tags: List[str]
    ai_copy: str
    price_min: float
    price_max: float
    contact: str
    status: str
    is_flagged: bool
    seller_id: int
    seller_name: Optional[str] = None
    created_at: datetime


class ListingPage(BaseModel):
    items: List[ListingOut]
    total: int
    page: int
    page_size: int


class StatusIn(BaseModel):
    status: str


# ---------- AI 发品草稿 ----------
class AnalyzeOut(BaseModel):
    images: List[str]
    title: str
    category: str
    condition: str
    price_min: float
    price_max: float
    tags: List[str]
    valuation_note: str = ""
    copy: str
