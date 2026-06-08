# 社内文件 + Wiki 混合检索 RAG Demo

这个 demo 用本地文件模拟两类社内资料源：

- `server_docs/`：服务器上的制度类、流程类资料
- `wiki_docs/`：社内 Wiki 上的操作类、FAQ 类资料

它重点演示四层：

1. 接入层：把不同来源统一加载成文档
2. 检索层：对可访问文档做关键词检索和 rerank
3. 权限层：按角色过滤不可见文档
4. 引用层：输出带来源的答案

## 安装

这个 demo 只用 Python 标准库，不需要额外安装第三方包。

如果你想先看统一环境说明，可以参考 [项目依赖总表](../DEPENDENCIES.md)。

## 你会学到什么

- 怎么把文件服务器和 Wiki 当成两个资料源接入
- 怎么在检索前做权限过滤
- 怎么让答案带来源引用
- 怎么把“社内搜索”拆成可测试的小步骤

## 运行方式

```bash
/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/internal_hybrid_rag_demo/main.py "远程办公和发布流程有什么要求？" --role employee
```

可选角色：

- `employee`
- `manager`
- `it_admin`

例如：

```bash
/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/internal_hybrid_rag_demo/main.py "事故处理流程和访问控制怎么查？" --role it_admin
```

## 常见报错

- `FileNotFoundError`：通常是 `assets/` 或 `catalog.json` 路径不对，先确认在 demo 目录内运行。
- `Permission denied` 风格的问题：先检查 `--role` 是否选对，很多文档默认只对部分角色可见。

## 目录结构

```text
internal_hybrid_rag_demo/
├── main.py
└── assets/
    ├── catalog.json
    ├── server_docs/
    └── wiki_docs/
```

## 设计重点

- `server_docs/` 更像制度、流程、审批、规范
- `wiki_docs/` 更像 FAQ、操作说明、排障指南、发布手册
- `catalog.json` 保存来源、标题、路径、ACL 等元数据
- `main.py` 负责统一接入、权限过滤、检索、引用生成

## 学习建议

先看 `main.py` 的四个分层函数，再看 `assets/` 里的资料样本。  
如果你要做成真实企业系统，下一步通常就是：

1. 把本地目录换成真正的文件服务器
2. 把 Wiki 读取器换成 Confluence / SharePoint / Notion API
3. 把 ACL 接到公司权限系统
4. 把检索层升级成向量检索 + rerank
