"""合规过滤：本地敏感词表 + 多模态违规图审核。"""
from .ai import moderate_images
from .config import settings

SENSITIVE_WORDS = [
    "赌博", "毒品", "枪支", "弹药", "色情", "代考", "替考", "作弊",
    "违禁品", "管制刀具", "诈骗", "洗钱", "发票代开",
]


def check_sensitive(text: str) -> list[str]:
    if not text:
        return []
    return [w for w in SENSITIVE_WORDS if w in text]


def moderate_listing(title: str, copy: str, image_paths: list[str]) -> tuple[bool, list[str]]:
    """返回 (是否违规, 原因列表)。图片审核异常时不判违规，仅跳过，避免阻塞发布。"""
    reasons = []
    for w in check_sensitive(f"{title} {copy}"):
        reasons.append(f"命中敏感词：{w}")
    if settings.enable_image_moderation and image_paths:
        try:
            safe, reason = moderate_images(image_paths)
            if not safe:
                reasons.append(f"图片违规：{reason}")
        except Exception as exc:
            print(f"[moderation] 图片审核跳过：{exc}")
    return bool(reasons), reasons
