"""pydantic_example.py

示例：使用 pydantic 进行数据验证，适合结构化输出场景。
运行：`python pydantic_example.py`
"""

from pydantic import BaseModel, ValidationError, Field


class User(BaseModel):
    """定义一个用户模型，包含类型约束和默认值。"""
    id: int
    name: str
    email: str | None = None
    score: float = Field(0.0, ge=0.0)  # 验证 score >= 0


def main() -> None:
    # 正确的数据会通过验证并被转换为模型实例
    payload = {"id": 1, "name": "Bob", "score": 4.5}
    user = User(**payload)
    print("validated:", user)

    # 错误的数据会抛出 ValidationError
    bad = {"id": "not-an-int", "name": "Bad"}
    try:
        User(**bad)
    except ValidationError as exc:
        print("validation error:\n", exc)


if __name__ == "__main__":
    main()
