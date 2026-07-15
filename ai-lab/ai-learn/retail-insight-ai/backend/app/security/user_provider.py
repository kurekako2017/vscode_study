"""Deterministic Test User Provider。

文件职责：提供 admin / manager / employee 三个本地认证账号。
谁调用它：AuthenticationService。
它调用谁：不连接数据库，不调用 RBAC。
输入：username。
输出：带 bcrypt hash 的认证用户记录。
设计理由：本轮只验证认证框架，避免提前进入用户管理和 RBAC。
日本现场面试：这是可替换 Identity Provider seam，生产环境应换成用户库或 IdP。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AuthenticationUser:
    """认证所需的最小用户记录；不包含 permissions。"""

    user_id: str
    username: str
    role: str
    password_hash: str


class DeterministicTestUserProvider:
    """只保存预先生成的 bcrypt hash，不保存明文密码。"""

    # Hash 对应的测试密码只存在于测试代码/受控验收输入，应用代码不保存明文。
    _USERS = {
        "admin": AuthenticationUser(
            user_id="user-admin",
            username="admin",
            role="admin",
            password_hash="$2b$12$5KLWAEueTRWrGLNtN/hoFuG6aM7g1Ra9AO5OUAo/xRrHTAmRllQ4e",
        ),
        "manager": AuthenticationUser(
            user_id="user-manager",
            username="manager",
            role="manager",
            password_hash="$2b$12$1xhgXWN3c5hfgci7KUsczOeDgdzxxnGIveme17Gj2KxGkyVyy.r8C",
        ),
        "employee": AuthenticationUser(
            user_id="user-employee",
            username="employee",
            role="employee",
            password_hash="$2b$12$b.LlhGz4lOgStDtOxgJ.i.yTV0yBx/hFXJBRghSJoL68DNUz500Xi",
        ),
    }
    _DUMMY_PASSWORD_HASH = (
        "$2b$12$5KLWAEueTRWrGLNtN/hoFuG6aM7g1Ra9AO5OUAo/xRrHTAmRllQ4e"
    )

    def get_by_username(self, username: str) -> AuthenticationUser | None:
        """按规范化用户名读取测试身份；未知用户返回 None。"""

        return self._USERS.get(username.strip().lower())

    def get_dummy_password_hash(self) -> str:
        """未知用户也执行一次 bcrypt，降低用户名枚举的时序差异。"""

        return self._DUMMY_PASSWORD_HASH
