"""FastAPI 应用入口。"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import BASE_DIR, settings
from .database import Base, SessionLocal, engine
from . import models  # noqa: F401  确保模型注册到 Base.metadata
from .routers import admin, auth, listings
from .security import hash_password

Base.metadata.create_all(bind=engine)

app = FastAPI(title="校园二手交易与智能估价平台")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = BASE_DIR / settings.upload_dir
UPLOAD_DIR.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

app.include_router(auth.router)
app.include_router(listings.router)
app.include_router(admin.router)


def seed_admin() -> None:
    """首次启动创建管理员账号。"""
    db = SessionLocal()
    try:
        admin = (
            db.query(models.User)
            .filter(models.User.username == settings.admin_username)
            .first()
        )
        if admin is None:
            db.add(
                models.User(
                    username=settings.admin_username,
                    password_hash=hash_password(settings.admin_password),
                    role="admin",
                )
            )
            db.commit()
    finally:
        db.close()


seed_admin()


@app.get("/")
def root():
    return {"message": "校园二手交易与智能估价平台 API", "docs": "/docs"}
