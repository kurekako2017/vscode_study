# Deep Research 主线项目

真实 LangGraph 工作流：研究计划 → 多查询检索 → 证据去重 → 带引用写作 → 引用/证据审校 → 必要时再检索。`max_rounds` 和 `recursion_limit` 防止无界研究。

```bash
cd deep_research_demo
python3 main.py "LangGraph MCP Agent 如何保证安全"
```

验收：报告中的每条事实都有 `[Sx]` 引用；来源表与正文一致；至少两条独立证据；达到最大轮次后必须结束。默认语料固定且离线，接真实搜索 API 时还需增加域名 allowlist、抓取时间、原文 URL、发布日期、事实支持度和 token/金额预算。
