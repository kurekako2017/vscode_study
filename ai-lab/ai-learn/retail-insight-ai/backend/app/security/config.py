"""JWT 配置值对象。

文件职责：把 Settings 中的部署参数收敛为 JWT 层唯一可见的配置。
谁调用它：应用组合根创建 JWTProvider / JWTService 时调用。
它调用谁：不调用业务 Service 或 Repository。
输入：密钥、算法、Access Token 有效期、时钟偏差容忍秒数。
输出：不可变 JWTConfig。
设计理由：认证参数集中管理，避免路由和 Provider 出现 magic number。
日本现场面试：配置层只描述 Token 策略，认证与未来授权保持分离。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class JWTConfig:
    """保存 JWT 签名与 Access Token 生命周期配置。

    leeway_seconds：仅用于吸收主机/WSL 时钟回拨导致的 iat/exp 边界抖动。
    不改变签名算法、密钥或 claims 合同；过期仍 fail-closed。
    """

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    # 诊断证据：PG 全量 suite 出现 max ~2s 时钟回拨 → iat 落在未来 → ImmatureSignatureError。
    # 30s 是行业常见 clock-skew 容忍，远小于默认 30min TTL。
    leeway_seconds: int = 30
