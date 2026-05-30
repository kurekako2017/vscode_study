"""basics.py

最小的 Python 基础语法示例，包含注释：变量、数据类型、控制流、函数和列表推导式。
运行：`python3 basics.py`
"""

# 变量与基本类型
name = "Alice"  # 字符串
age = 30         # 整数
pi = 3.1415      # 浮点数


def greet(person: str) -> str:
    """返回问候语的函数，演示类型注解和简单逻辑。"""
    return f"Hello, {person}!"


def factorial(n: int) -> int:
    """计算 n 的阶乘（示例：控制流与循环）。"""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


if __name__ == "__main__":
    # 打印变量
    print(greet(name))
    print("age:", age)
    print("pi approx:", pi)

    # 使用列表推导式生成平方数
    squares = [x * x for x in range(6)]  # 列表推导式示例
    print("squares:", squares)

    # 调用函数并打印结果
    print("5! =", factorial(5))
