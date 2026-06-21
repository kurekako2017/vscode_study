"""basics.py

最小的 Python 基础语法示例，包含注释：变量、数据类型、控制流、函数和列表推导式。
运行：`python3 basics.py`
"""

# 变量与基本类型：
# LLM 应用里也会经常处理字符串、数字、列表等基础数据。
# 先把这些基础类型看熟，后面读 prompt、JSON、chunk 时会轻松很多。
name = "Alice"  # 字符串
age = 30         # 整数
pi = 3.1415      # 浮点数


def greet(person: str) -> str:
    """返回问候语的函数，演示类型注解和简单逻辑。"""
    # f-string 用来把变量嵌入字符串；写 prompt 模板时也常用这种方式。
    return f"Hello, {person}!"


def factorial(n: int) -> int:
    """计算 n 的阶乘（示例：控制流与循环）。"""
    # result 用来累计乘法结果。
    result = 1
    # range(2, n + 1) 会依次产生 2 到 n。
    # 这里演示最基础的 for 循环。
    for i in range(2, n + 1):
        result *= i
    return result


if __name__ == "__main__":
    # 只有直接运行这个文件时，下面代码才会执行。
    # 如果这个文件被其他文件 import，下面代码不会自动跑。

    # 打印变量
    print(greet(name))
    print("age:", age)
    print("pi approx:", pi)

    # 使用列表推导式生成平方数
    # 列表推导式：把 0 到 5 逐个平方，生成一个新列表。
    # 后面处理 chunk、sources、tools 时也会常见这种写法。
    squares = [x * x for x in range(6)]
    print("squares:", squares)

    # 调用函数并打印结果
    print("5! =", factorial(5))
