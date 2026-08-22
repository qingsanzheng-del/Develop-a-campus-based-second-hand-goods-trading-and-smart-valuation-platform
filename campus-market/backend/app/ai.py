"""AI 能力：多模态模型（本地 Ollama / 云端 DashScope）估价与违规图审核。

两者都通过 OpenAI 兼容接口调用，仅 base_url 与模型名不同。
"""
import base64
import io
import json
import re

from openai import OpenAI
from PIL import Image

from .config import settings

CATEGORIES = ["数码", "书籍", "生活用品", "服饰鞋包", "运动户外", "其他"]

ANALYSIS_PROMPT = """你是校园二手交易平台的智能估价助手。请根据二手物品照片和补充说明，只输出一个JSON对象，不要输出其他内容。

字段要求：category选数码/书籍/生活用品/服饰鞋包/运动户外/其他；condition写成色如95新；title写15字内标题；price_min写底价元；price_max写期望价元；tags写2到4个卖点；valuation_note写一句估价依据；copy写60到120字带货文案。

估价规则：二手价约为全新市场价的3到7折，成色越新越接近7折，price_max大于price_min。

输出示例：{"category":"数码","condition":"95新","title":"标题","price_min":100,"price_max":130,"tags":["卖点"],"valuation_note":"依据","copy":"文案"}

补充说明：__DESCRIPTION__"""

MODERATION_PROMPT = """请判断这些图片是否包含违禁、色情、暴力、血腥或违法违规内容。只输出一个 JSON 对象：{"safe": true 或 false, "reason": "简短原因"}。"""


def _client() -> OpenAI:
    if settings.ai_provider == "dashscope":
        return OpenAI(
            api_key=settings.dashscope_api_key, base_url=settings.dashscope_base_url
        )
    return OpenAI(api_key="ollama", base_url=f"{settings.ollama_base_url}/v1")


def _model() -> str:
    if settings.ai_provider == "dashscope":
        return settings.dashscope_model
    return settings.ollama_model


def _encode_image(path: str, max_size: int = 1024) -> str:
    """读取图片 → 压缩到最长边 max_size → base64 data URL。

    压缩显著降低多模态推理的 tokens 与耗时；透明图合成白底避免黑边。
    """
    with Image.open(path) as img:
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGBA")
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[-1])
            img = bg
        else:
            img = img.convert("RGB")
        w, h = img.size
        scale = max_size / max(w, h)
        if scale < 1.0:
            img = img.resize(
                (max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS
            )
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=82)
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{b64}"


def _image_parts(paths: list[str], max_size: int = 1024) -> list[dict]:
    return [
        {"type": "image_url", "image_url": {"url": _encode_image(p, max_size)}}
        for p in paths
    ]


def _extract_json(text: str) -> dict:
    """从模型输出中稳健地提取 JSON 对象。"""
    text = (text or "").strip()
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.MULTILINE).strip()
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end > start:
        text = text[start : end + 1]
    # 去除数组/对象末尾的尾逗号（小模型常见的非严格 JSON）
    text = re.sub(r",\s*([}\]])", r"\1", text)
    try:
        return json.loads(text)
    except Exception:
        return {}


def _chat(content: list[dict]) -> str:
    """调用对话接口，依次尝试：关思考+JSON 约束 → JSON 约束 → 兜底。"""
    client = _client()
    base = dict(
        model=_model(),
        messages=[{"role": "user", "content": content}],
        temperature=0.1,
    )
    for attempt in (
        # 1) 关闭思考模式（本地 qwen 系列提速）+ 强制 JSON 约束解码
        {"response_format": {"type": "json_object"}, "extra_body": {"think": False}},
        # 2) 仅强制 JSON
        {"response_format": {"type": "json_object"}},
        # 3) 兜底
        {},
    ):
        try:
            resp = client.chat.completions.create(**base, **attempt)
            text = resp.choices[0].message.content or ""
            if text.strip():
                return text
            # 内容为空时继续回退（小模型偶发空输出）
        except Exception:
            continue
    return ""


def analyze_listing(image_paths: list[str], description: str = "") -> dict:
    """图片 → 分类 / 成色 / 价格区间 / 标签 / 文案 / 估价依据。

    小模型 JSON 输出不稳定，结果为空时最多重试 3 次。
    """
    content = [
        {"type": "text", "text": ANALYSIS_PROMPT.replace("__DESCRIPTION__", description or "无")}
    ]
    content += _image_parts(image_paths, max_size=1024)
    for _ in range(3):
        data = _extract_json(_chat(content))
        if data.get("title") or data.get("category") or data.get("copy"):
            return data
    return {}


def moderate_images(image_paths: list[str]) -> tuple[bool, str]:
    """违规图审核，返回 (是否安全, 原因)。用更小分辨率提速。"""
    content = [{"type": "text", "text": MODERATION_PROMPT}]
    content += _image_parts(image_paths, max_size=512)
    data = _extract_json(_chat(content))
    return bool(data.get("safe", True)), str(data.get("reason", ""))
