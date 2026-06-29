# Stock Agent：日本股票公开信息研究助手

这是一个适合初学者阅读的日本股票研究辅助 Demo。第一版只使用项目内置 Mock 数据，不连接真实行情 API，不调用 AI API，也不访问证券账户。

## 当前功能

- 输入四位日本股票代码。
- 获取固定的本地 Mock 数据。
- 生成规则化的 AI 风格总结和风险提示。
- 输出 Markdown 研究辅助报告。
- 支持的 Mock 代码：`7203`、`8306`、`9432`。

## 安全边界

- 无需 API Key，程序也不会读取 `.env`。
- 不访问网络或证券账户。
- 不提供登录和交易功能。
- 不输出买入、卖出、强烈推荐等投资指令。
- 所有价格、PER、PBR 和股息率均为模拟数据。
- 输出只用于编程学习和研究辅助，不构成投资建议。

## 环境要求

- Python 3.10 或更高版本。
- 第一版只使用 Python 标准库，不需要安装第三方依赖。

## 运行方法

在工作区根目录执行：

```bash
cd ai-lab/stock-agent
python3 src/main.py 7203
```

也可以尝试：

```bash
python3 src/main.py 8306
python3 src/main.py 9432
```

成功后会生成：

```text
reports/7203_report.md
```

## 项目结构

```text
stock-agent/
├── README.md
├── requirements.txt
├── src/
│   ├── main.py
│   ├── fetcher.py
│   ├── analyzer.py
│   └── report_writer.py
├── reports/
│   └── sample_report.md
└── docs/
    ├── 设计说明.md
    ├── 使用教程.md
    └── 风险说明.md
```

## 模块职责

| 模块 | 职责 |
| --- | --- |
| `src/main.py` | 接收股票代码并组织完整流程 |
| `src/fetcher.py` | 校验代码并返回本地 Mock 数据 |
| `src/analyzer.py` | 生成中性的总结和风险提示 |
| `src/report_writer.py` | 生成并保存 Markdown 报告 |

## 第一版限制

- 仅支持三只预设股票。
- 数据不是真实行情，也不会自动更新。
- “AI 总结”由本地规则生成，没有调用大语言模型。
- 不进行收益预测、组合建议或交易决策。

进一步说明请阅读 [设计说明](docs/设计说明.md)、[使用教程](docs/使用教程.md) 和 [风险说明](docs/风险说明.md)。
