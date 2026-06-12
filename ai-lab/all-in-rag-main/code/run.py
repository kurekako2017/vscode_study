#!/usr/bin/env python3
"""
文件功能概述：`code/run.py` 主要是 运行，这个文件里有 0 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 这个文件没有独立类或函数，主要靠模块级代码直接执行。
"""


from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from run import main


if __name__ == "__main__":
    raise SystemExit(main())
