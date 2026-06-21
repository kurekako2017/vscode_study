# MCP Office Agent

需求：Office 场景只能使用 allowlist 中的“检索文档”和“创建草稿”；发送、删除和覆盖等动作默认拒绝。项目内的本地 adapter 用于离线验收，真实 MCP transport 见 `../../mcp/`。

```bash
python3 main.py search_documents "费用"
python3 main.py create_draft "会议纪要"
```

验收：查询直接完成；创建内容只返回 `draft` 且要求审批；allowlist 外工具无法进入执行函数。简历表述：实现 MCP 工具权限、草稿审批和调用审计。
