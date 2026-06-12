"""
文件功能概述：`code/C9/main.py` 主要是 主函数，这个文件里有 1 个类、2 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 类 `RecipeNode`：功能概述：这个类是 `RecipeNode`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. 这个类没有单独的方法，通常用于保存配置或做简单占位。
2. 函数 `answer`：先接收输入参数 question，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 question.lower、join 等内部步骤完成主要工作，最后返回结果。
3. 函数 `main`：先进入当前步骤，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 print、sys.stdin.isatty、strip 等内部步骤完成主要工作，最后返回结果。
"""

from __future__ import annotations

import sys
from dataclasses import dataclass


@dataclass
class RecipeNode:
    """
    功能概述：这个类是 `RecipeNode`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. 这个类没有单独的方法，通常用于保存配置或做简单占位。
    """
    name: str
    category: str
    ingredients: list[str]
    steps: list[str]


RECIPES = [
    RecipeNode(
        name="番茄炒蛋",
        category="素菜",
        ingredients=["番茄", "鸡蛋", "盐", "糖"],
        steps=["打散鸡蛋并炒熟", "番茄切块翻炒", "加入鸡蛋和调味料"],
    ),
    RecipeNode(
        name="玉米排骨汤",
        category="汤品",
        ingredients=["排骨", "玉米", "姜片", "盐"],
        steps=["排骨焯水", "与玉米姜片炖煮", "出锅前加盐调味"],
    ),
    RecipeNode(
        name="麻婆豆腐",
        category="川菜",
        ingredients=["豆腐", "牛肉末", "豆瓣酱", "花椒", "辣椒"],
        steps=["炒香调料", "下豆腐轻推", "收汁后撒花椒"],
    ),
]


def answer(question: str) -> str:  # 中文名称：answer
    lower = question.lower()
    if "食材" in question or "需要什么" in question:
        for recipe in RECIPES:
            if recipe.name in question:
                return f"{recipe.name}的食材包括：{'、'.join(recipe.ingredients)}。"
    if "步骤" in question or "怎么做" in question or "做法" in question:
        for recipe in RECIPES:
            if recipe.name in question:
                return f"{recipe.name}的步骤：{'；'.join(recipe.steps)}。"
    if "汤" in question:
        soup_names = [recipe.name for recipe in RECIPES if recipe.category == "汤品"]
        return f"可以尝试这些汤品：{'、'.join(soup_names)}。"
    if "川菜" in question:
        names = [recipe.name for recipe in RECIPES if recipe.category == "川菜"]
        return f"川菜示例：{'、'.join(names)}。"
    return f"这是一个离线图式问答示例。你可以询问：{RECIPES[0].name} 需要什么食材？"


def main():  # 中文名称：主函数
    print("基于图RAG的智能烹饪助手 - 离线演示")
    print("可用示例：番茄炒蛋需要什么食材？、玉米排骨汤怎么做？")

    if not sys.stdin.isatty():
        question = "番茄炒蛋需要什么食材？"
        print(f"\n示例问题: {question}")
        print(f"回答: {answer(question)}")
        return

    while True:
        question = input("\n请输入问题（回车退出）: ").strip()
        if not question:
            break
        print(answer(question))


if __name__ == "__main__":
    main()
