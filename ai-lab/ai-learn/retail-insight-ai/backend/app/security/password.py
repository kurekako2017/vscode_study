"""Password Verification Boundary。

文件职责：使用 passlib + bcrypt 校验密码，不保存明文、不自定义 hash。
谁调用它：AuthenticationService。
它调用谁：passlib CryptContext。
输入：登录请求密码与静态测试用户的 bcrypt hash。
输出：布尔校验结果。
设计理由：密码算法集中，未来替换用户数据库时认证服务无需改动。
日本现场面试：当前只有 deterministic test users，密码仍按真实 bcrypt 流程校验。
"""

from __future__ import annotations

from passlib.context import CryptContext


class PasswordService:
    """封装 passlib bcrypt 密码校验。"""

    def __init__(self) -> None:
        self._context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify(self, plain_password: str, password_hash: str) -> bool:
        """恒定走 bcrypt verifier；不记录输入密码或 hash。"""

        return self._context.verify(plain_password, password_hash)
