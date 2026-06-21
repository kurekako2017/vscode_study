# 面试 Agent

需求：对 STAR 回答做确定性 rubric 评分，指出缺项并生成下一轮追问；不把主观语言风格当成事实能力结论。

```bash
python3 main.py "situation task action result metric reflection"
```

验收：满要素为 10 分；缺失项出现在 `missing`；结果包含审计记录。简历表述：实现结构化面试训练、rubric 评分与可解释反馈。
