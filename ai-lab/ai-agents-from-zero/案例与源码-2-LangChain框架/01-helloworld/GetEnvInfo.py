"""
【案例】环境检查：LangChain 版本与安装路径

对应教程章节：第 10 章 - LangChain 快速上手与 HelloWorld → 3、安装依赖

知识点速览：
本脚本用于确认当前 Python 环境中 LangChain、langchain_community 的版本与安装路径，
便于排查「装错版本」「没进虚拟环境」或「解释器不是当前项目那一个」等问题。无需 API Key，可直接运行。
"""

import sys  # 获取 Python 解释器信息
import warnings  # 屏蔽第三方包的弃用提示

warnings.filterwarnings("ignore", category=DeprecationWarning)

import langchain  # 核心框架（Chain、Agent、Memory 等）
import langchain_community  # 社区扩展（部分集成、第三方工具等）

print("=== 环境信息 ===")
print(f"langchain version      : {langchain.__version__}")
print(f"langchain_community    : {langchain_community.__version__}")
print(f"langchain install path : {langchain.__file__}")
print(f"python version         : {sys.version.split()[0]}")
print(f"python executable      : {sys.executable}")

"""
【输出示例】
 langchainVersion:  1.2.9
 langchain_communityVersion:  0.4.1
 langchainfile:/Users/tools/PyCharmMiscProject/python100/.venv/lib/python3.10/site-packages/langchain/__init__.py
 3.10.19 (main, Oct  9 2025, 15:25:03) [Clang 17.0.0 (clang-1700.6.3.2)]
 pythonExecutable:/Users/tools/PyCharmMiscProject/python100/.venv/bin/python
"""
