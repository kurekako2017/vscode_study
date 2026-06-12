"""
文件功能概述：`code/C3/visual_bge/setup.py` 主要是 setup，这个文件里有 0 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 这个文件没有独立类或函数，主要靠模块级代码直接执行。
"""

from setuptools import setup, find_packages

setup(
    name="visual_bge",
    version="0.1.0",
    description='visual_bge',
    long_description="./README.md",
    long_description_content_type="text/markdown",
    url='https://github.com/FlagOpen/FlagEmbedding/tree/master/research/visual_bge',
    packages=find_packages(),
    install_requires=[
        'torchvision',
        'timm',
        'einops',
        'ftfy'
    ],
    python_requires='>=3.6',
)
