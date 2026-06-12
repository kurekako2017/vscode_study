from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, List, Sequence

import numpy as np


DEFAULT_EMBED_DIM = 384


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[\w\u4e00-\u9fff]+", text.lower())


def hash_embed(text: str, dim: int = DEFAULT_EMBED_DIM) -> np.ndarray:
    vector = np.zeros(dim, dtype=np.float32)
    for token in _tokenize(text):
        digest = hashlib.md5(token.encode("utf-8")).hexdigest()
        idx = int(digest[:8], 16) % dim
        sign = -1.0 if int(digest[8:9], 16) % 2 else 1.0
        vector[idx] += sign

    norm = float(np.linalg.norm(vector))
    if norm:
        vector /= norm
    return vector


def normalize_vectors(vectors: np.ndarray) -> np.ndarray:
    if vectors.size == 0:
        return vectors
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return vectors / norms


def cosine_similarity(query: Sequence[float], candidates: Sequence[Sequence[float]]) -> np.ndarray:
    q = np.asarray(query, dtype=np.float32)
    docs = np.asarray(candidates, dtype=np.float32)
    if q.ndim == 1:
        q = q[None, :]
    if docs.ndim == 1:
        docs = docs[None, :]
    q = normalize_vectors(q)
    docs = normalize_vectors(docs)
    return q @ docs.T


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def prompt_to_text(prompt: Any) -> str:
    if prompt is None:
        return ""
    if isinstance(prompt, str):
        return prompt
    if isinstance(prompt, (list, tuple)):
        parts: list[str] = []
        for item in prompt:
            parts.append(prompt_to_text(item))
        return "\n".join(p for p in parts if p)
    if hasattr(prompt, "to_string"):
        try:
            return prompt.to_string()
        except Exception:
            pass
    if hasattr(prompt, "content"):
        return str(getattr(prompt, "content"))
    if hasattr(prompt, "messages"):
        return prompt_to_text(getattr(prompt, "messages"))
    return str(prompt)


def extract_question(text: str) -> str:
    patterns = [
        r"用户问题[:：]\s*(.+)",
        r"问题[:：]\s*(.+)",
        r"Question[:：]\s*(.+)",
        r"query[:：]\s*(.+)",
    ]
    for pattern in patterns:
        m = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if m:
            return m.group(1).strip()
    return text.strip()


def summarize_context(text: str, max_lines: int = 6) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ""
    return "\n".join(lines[:max_lines])


def classify_topic(text: str) -> str:
    lowered = text.lower()
    if any(keyword in lowered for keyword in ["川菜", "麻辣", "水煮鱼", "麻婆豆腐", "宫保鸡丁", "鱼香"]):
        return "川菜"
    if any(keyword in lowered for keyword in ["粤菜", "白切鸡", "老火靓汤", "虾饺", "云吞面"]):
        return "粤菜"
    if any(keyword in lowered for keyword in ["list", "列表", "推荐", "几个", "多个", "哪些菜"]):
        return "list"
    if any(keyword in lowered for keyword in ["怎么做", "制作", "步骤", "食材", "做法"]):
        return "detail"
    return "general"


def render_answer(prompt: str) -> str:
    text = prompt_to_text(prompt)
    question = extract_question(text)
    topic = classify_topic(text)

    if "只返回SQL语句" in text or "SQL语句" in text:
        if any(word in question for word in ["年龄", "age"]):
            return "SELECT * FROM users WHERE age > 30;"
        if any(word in question for word in ["库存", "stock"]):
            return "SELECT * FROM products WHERE stock < 50;"
        if "订单" in question:
            return "SELECT * FROM orders;"
        return "SELECT 1;"

    if "菜谱Markdown" in text and "返回标准JSON" in text:
        return json.dumps(
            {
                "name": "示例菜",
                "difficulty": 3,
                "category": "素菜",
                "cuisine_type": "",
                "prep_time": "10分钟",
                "cook_time": "15分钟",
                "servings": "2人",
                "ingredients": [
                    {"name": "示例食材", "amount": "1", "unit": "份", "category": "蔬菜", "is_main": True}
                ],
                "steps": [
                    {"step_number": 1, "description": "准备食材", "methods": ["切"], "tools": ["刀"], "time_estimate": "5分钟"}
                ],
                "tags": ["离线占位"],
                "nutrition_info": {"calories": "", "protein": "", "carbs": "", "fat": ""},
            },
            ensure_ascii=False,
        )

    if "人物姓名" in text and "技能列表" in text:
        name = "张三"
        age = 30
        skills = ["Python", "Go"]
        return json.dumps({"name": name, "age": age, "skills": skills}, ensure_ascii=False)

    if "list" == topic:
        return "川菜示例：麻婆豆腐、宫保鸡丁、鱼香肉丝。"
    if "detail" == topic:
        return f"基于提供的上下文，{question} 的做法通常包括准备食材、处理主料、按步骤烹饪并调味。"
    if topic in {"川菜", "粤菜"}:
        return f"这是一个关于{topic}的回答。你可以根据常见做法准备食材并分步完成。"

    context = summarize_context(text)
    if context:
        return f"根据上下文，可以回答为：{context}"
    return f"这是一个离线占位回答：{question}"


@dataclass
class SimpleMessage:
    content: str
