"""
应用主配置

定义 conf/app_config.yaml 在程序中的结构化配置对象
项目启动后会在这里一次性完成配置文件加载和类型化转换，其他模块只需要导入 app_config
就可以按属性方式读取日志 MySQL Qdrant Embedding Elasticsearch 和 LLM 配置
"""

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
import yaml


@dataclass
class File:
    """文件日志配置"""

    enable: bool
    level: str
    path: str
    rotation: str
    retention: str


@dataclass
class Console:
    """控制台日志配置"""

    enable: bool
    level: str


@dataclass
class LoggingConfig:
    """日志总配置"""

    file: File
    console: Console


@dataclass
class DBConfig:
    """MySQL 连接配置"""

    host: str
    port: int
    user: str
    password: str
    database: str


@dataclass
class QdrantConfig:
    """Qdrant 连接与向量维度配置"""

    host: str
    port: int
    embedding_size: int


@dataclass
class EmbeddingConfig:
    """Embedding 服务配置"""

    host: str
    port: int
    model: str


@dataclass
class ESConfig:
    """Elasticsearch 配置"""

    host: str
    port: int
    index_name: str


@dataclass
class LLMConfig:
    """大模型调用配置"""

    provider_order: str
    model_name: str
    api_key: str
    base_url: str
    openrouter_model_name: str
    openrouter_api_key: str
    openrouter_base_url: str
    nvidia_model_name: str
    nvidia_api_key: str
    nvidia_base_url: str
    ollama_model_name: str
    ollama_api_key: str
    ollama_base_url: str


@dataclass
class RuntimeConfig:
    """运行时开关配置"""

    mock_mode: bool = False


@dataclass
class AppConfig:
    """项目级总配置入口"""

    logging: LoggingConfig
    db_meta: DBConfig
    db_dw: DBConfig
    qdrant: QdrantConfig
    embedding: EmbeddingConfig
    es: ESConfig
    llm: LLMConfig
    runtime: RuntimeConfig


_ENV_PATTERN = re.compile(r"^\$\{oc\.env:([^,}]+)(?:,([^}]*))?\}$")


def _coerce_value(value: Any) -> Any:
    """把 YAML 读出来的字符串环境占位符转换成更合适的 Python 类型。"""

    if isinstance(value, str):
        lowered = value.lower()
        if lowered == "true":
            return True
        if lowered == "false":
            return False
        if value.isdigit():
            return int(value)
    return value


def _resolve_env_placeholders(value: Any) -> Any:
    """递归展开 YAML 里的 ${oc.env:VAR,default} 占位符。"""

    if isinstance(value, dict):
        return {key: _resolve_env_placeholders(item) for key, item in value.items()}

    if isinstance(value, list):
        return [_resolve_env_placeholders(item) for item in value]

    if isinstance(value, str):
        match = _ENV_PATTERN.match(value)
        if match:
            env_name = match.group(1)
            default = match.group(2)
            resolved = os.getenv(env_name, default if default is not None else "")
            return _coerce_value(resolved)
        return value

    return value


def _build_dataclass(dataclass_type, data: dict[str, Any]):
    """用字典构造嵌套 dataclass 配置对象。"""

    return dataclass_type(
        **{
            field.name: _build_value(field.type, data[field.name])
            for field in dataclass_type.__dataclass_fields__.values()
        }
    )


def _build_value(field_type, value: Any):
    """根据字段类型把字典或标量转换成对应对象。"""

    if hasattr(field_type, "__dataclass_fields__") and isinstance(value, dict):
        return _build_dataclass(field_type, value)
    return value


# 从当前文件位置回到项目根目录，再定位到 conf/app_config.yaml
project_root = Path(__file__).parents[2]
config_file = project_root / "conf" / "app_config.yaml"

# 先读取本地 .env，让 YAML 中的 ${oc.env:...} 可以解析到敏感配置
load_dotenv(project_root / ".env")

# 兼容旧版 LLM_* 写法：没有单独配置 OpenRouter 时，沿用 LLM_*。
if not os.getenv("OPENROUTER_API_KEY") and os.getenv("LLM_API_KEY"):
    os.environ["OPENROUTER_API_KEY"] = os.environ["LLM_API_KEY"]
if not os.getenv("OPENROUTER_MODEL_NAME") and os.getenv("LLM_MODEL_NAME"):
    os.environ["OPENROUTER_MODEL_NAME"] = os.environ["LLM_MODEL_NAME"]
if not os.getenv("OPENROUTER_BASE_URL") and os.getenv("LLM_BASE_URL"):
    os.environ["OPENROUTER_BASE_URL"] = os.environ["LLM_BASE_URL"]

# NVIDIA NIM 有些环境会用 NGC_API_KEY，这里也兼容一下。
if not os.getenv("NVIDIA_API_KEY") and os.getenv("NGC_API_KEY"):
    os.environ["NVIDIA_API_KEY"] = os.environ["NGC_API_KEY"]

# 读取 YAML 配置内容
with config_file.open("r", encoding="utf-8") as file:
    context = yaml.safe_load(file)

context = _resolve_env_placeholders(context)

# 把配置字典转换成可以直接按属性访问的 dataclass 对象
app_config: AppConfig = _build_dataclass(AppConfig, context)

if __name__ == "__main__":
    # 简单测试：验证配置是否能正常读取
    print(app_config.es.host)
