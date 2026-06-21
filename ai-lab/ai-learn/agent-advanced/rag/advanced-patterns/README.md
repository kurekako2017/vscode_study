# 高级 RAG 标准模式

一个离线脚本覆盖四条标准链路：小块召回后返回完整父文档（Parent Document）、按问题压缩上下文（Contextual Compression）、生成假设答案扩展检索（HyDE）、低相关时回退（Corrective RAG）。

```bash
python3 main.py "新干线超过三万日元怎么审批"
python3 main.py "数据库密码是什么"
python3 main.py "远程办公规定" --baseline
```

验收：制度问题返回父文档来源；无关问题走 `fallback`；`--baseline` 可与 HyDE 路径对比。这里的词法检索用于稳定离线演示，生产环境应替换为向量召回和 cross-encoder reranker。
