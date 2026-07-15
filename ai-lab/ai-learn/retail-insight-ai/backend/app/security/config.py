"""JWT 配置值对象。

文件职责：把 Settings 中的部署参数收敛为 JWT 层唯一可见的配置。
谁调用它：应用组合根创建 JWTProvider / JWTService 时调用。
它调用谁：不调用业务 Service 或 Repository。
输入：密钥、算法、Access Token 有效期。
输出：不可变 JWTConfig。
设计理由：认证参数集中管理，避免路由和 Provider 出现 magic number。
日本现场面试：配置层只描述 Token 策略，认证与未来授权保持分离。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class JWTConfig:
    """保存 JWT 签名与 Access Token 生命周期配置。"""

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
