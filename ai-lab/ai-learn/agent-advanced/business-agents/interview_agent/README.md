# 面试 Agent

需求：对 STAR 回答做确定性 rubric 评分，指出缺项并生成下一轮追问；不把主观语言风格当成事实能力结论。

```bash
python3 main.py "situation task action result metric reflection"
```

验收：满要素为 10 分；缺失项出现在 `missing`；结果包含审计记录。简历表述：实现结构化面试训练、rubric 评分与可解释反馈。

## 图片式模板解释

输入：`python3 main.py "situation task action result metric reflection"`；处理前数据是一段面试回答和固定 Rubric。

```text
面试回答 -> main() -> coach()
│
├── 逐项匹配 Situation / Task / Action / Result / Metric / Reflection
├── 累计 score
└── 收集 missing
    │
    ▼
coach() -> 输出评分、缺项、追问和审计记录
```

节点对应：标准化统一文本，Rubric 提供确定性评分，追问针对缺项生成。最小完整输入输出 10 分；缺项输入会列出 `missing`。

## 业务场景（完整说明）

- **使用者**：求职者、面试教练和企业培训人员。
- **要解决的问题**：检查 STAR 回答是否包含情境、任务、行动、结果、指标和复盘。
- **输入与输出**：输入一段面试回答；输出评分、缺失要素和下一步追问。
- **生产环境差距**：需要多语言语义判断、岗位化评分表、历史训练记录和人工教练复核。

## 整体流程图

```mermaid
graph TD
    A[面试回答] --> B[标准化文本]
    B --> C[逐项匹配 STAR Rubric]
    C --> D[累计分数]
    C --> E[收集缺失要素]
    D --> F[生成反馈和追问]
    E --> F
    F --> G[输出审计结果]
```
