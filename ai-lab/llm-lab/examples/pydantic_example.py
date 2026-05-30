"""pydantic_example.py

示例：使用 pydantic 进行数据验证，适合结构化输出场景。
运行：`python3 pydantic_example.py`
"""

from pydantic import BaseModel, ValidationError, Field


class User(BaseModel):
    """定义一个用户模型，包含类型约束和默认值。"""
    # id 必须能被解析为 int。
    id: int
    # name 必须是字符串。
    name: str
    # email 可以是字符串，也可以是 None；默认就是 None。
    email: str | None = None
    # score 默认 0.0，并且要求大于等于 0。
    # 结构化输出里也常用 Field 给字段加约束和说明。
    score: float = Field(0.0, ge=0.0)  # 验证 score >= 0


def main() -> None:
    # 正确的数据会通过验证并被转换为模型实例
    # 注意：payload 是普通 dict，User(**payload) 会做类型校验。
    payload = {"id": 1, "name": "Bob", "score": 4.5}
    user = User(**payload)
    print("validated:", user)

    # 错误的数据会抛出 ValidationError
    # 这里 id 不是整数，Pydantic 会告诉我们哪个字段不合法。
    bad = {"id": "not-an-int", "name": "Bad"}
    try:
        User(**bad)
    except ValidationError as exc:
        # 在真实项目里，ValidationError 可以转成 API 错误响应或日志。
        print("validation error:\n", exc)


if __name__ == "__main__":
    # 直接运行文件时执行示例。
    main()
