"""应用配置：从 backend/.env 读取，密钥只存在于后端。"""
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent  # backend/


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"), env_file_encoding="utf-8", extra="ignore"
    )

    # AI 后端选择：ollama（本地）或 dashscope（云端）
    ai_provider: str = "ollama"

    # Ollama 本地服务（默认，免 API Key）
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen3.5:4b"

    # 云端 DashScope（仅当 ai_provider=dashscope 时使用）
    dashscope_api_key: str = ""
    dashscope_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    dashscope_model: str = "qwen-vl-plus"

    enable_image_moderation: bool = True

    # 鉴权
    jwt_secret: str = "dev-secret-change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 10080  # 7 天

    # 管理员
    admin_username: str = "admin"
    admin_password: str = "admin123"

    # 存储
    upload_dir: str = "uploads"


settings = Settings()
