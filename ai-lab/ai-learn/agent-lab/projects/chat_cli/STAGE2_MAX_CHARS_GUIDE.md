# Stage 2: `--max-chars` 实战教程

本阶段目标：完整走一遍“参数 -> 业务逻辑 -> 输出”。

你将练到三件事：

1. 新增命令行参数
2. 把参数映射成业务规则
3. 在输出层看到行为变化

## 1. 本阶段改了什么

在 `main.py` 中新增了：

- `--max-chars` 参数：限制回答最大字符数
- `format_output()`：统一处理输出截断规则
- 主流程接线：一次性模式和交互模式都走同一套截断逻辑

## 2. 运行步骤（无 Key、零成本）

进入目录：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-learn/agent-lab/projects/chat_cli
```

先跑不截断：

```bash
python3 main.py --mock "请写一个稍长一点的学习建议"
```

再跑截断：

```bash
python3 main.py --mock --max-chars 60 "请写一个稍长一点的学习建议"
```

预期现象：

- 第二条命令输出更短
- 末尾出现 `...[truncated N chars]`

## 3. 交互模式练习

```bash
python3 main.py --mock --max-chars 80
```

然后连续输入 3 个问题，观察每次回答都经过同一个 `format_output()` 规则。

## 4. 注意点

1. `--max-chars` 必须大于 0
2. 不传 `--max-chars` 表示不截断
3. 这个参数是“输出层规则”，不是模型参数
4. Mock 模式也能练到 90% 的程序结构能力

## 5. 推荐练习法（30 分钟）

1. 10 分钟：只跑命令，观察行为差异
2. 10 分钟：把 `--max-chars` 改成默认 `120`，再运行对比
3. 10 分钟：给截断提示加上当前阈值，例如 `max=80`

## 6. 你现在学到的工程能力

1. 参数设计：`argparse` 如何定义新开关
2. 逻辑封装：为什么把截断放在单独函数中
3. 流程复用：一次性模式和交互模式共享业务规则
4. 可迁移性：未来接真实 API 时，这套结构无需重写

这就是后续做结构化输出、Tool Calling、RAG 时最核心的“骨架能力”。
