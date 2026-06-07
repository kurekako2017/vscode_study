# 社内文件与 Wiki 混合检索 RAG

这个专题对应的现实场景是：

- 有些资料放在服务器目录里，比如制度、流程、申请表、SOP
- 有些资料放在社内 Wiki 里，比如操作手册、FAQ、发布指南、排障记录
- 用户问问题时，不想知道资料在哪里，只想快速拿到可信答案和出处

这类场景在社内 Agent / 知识库问答里非常常见，尤其适合日本现场、企业内部支持、运维和研发协作场景。

## 现在仓库里已经有的相关例子

- [agent-lab/projects/doc_qa_agent](../agent-lab/projects/doc_qa_agent/README.md)
- [agent-lab/projects/rag_api_demo](../agent-lab/projects/rag_api_demo/README.md)
- [agent-advanced/projects/advanced_rag_pipeline_demo](../agent-advanced/projects/advanced_rag_pipeline_demo/README.md)
- [agent-advanced/projects/internal_hybrid_rag_demo](../agent-advanced/projects/internal_hybrid_rag_demo/README.md)

## 这类系统通常怎么分层

### 1. 接入层

先把不同来源接进来。

常见来源包括：

- 文件服务器
- 共享目录
- 社内 Wiki
- Confluence / SharePoint / Notion / 内部 CMS
- FAQ 数据库
- 工单系统

这一层的目标不是马上回答问题，而是把数据统一成一个可处理的格式。

### 2. 文档统一层

把不同来源统一成类似 `Document` 的结构，并补足元数据。

建议至少保留：

- `source_type`：`server` / `wiki`
- `title`
- `path` 或 `url`
- `updated_at`
- `owner`
- `acl` / `visibility`

这样后面做权限过滤、引用展示、增量更新都会更顺。

### 3. 检索层

检索层通常不会只做一种方法。

真实项目里常见组合是：

- 关键词检索
- 向量检索
- hybrid search
- rerank
- query rewrite
- multi-query

如果场景偏企业内部，Wiki 和文件服务器往往都要搜，但不是所有问题都要把全库硬搜一遍，最好先做路由和过滤。

### 4. 权限层

这是企业场景里最容易被忽略、但最重要的一层。

因为社内资料通常不是全员可见：

- 员工能看制度，但看不到敏感事故报告
- 研发能看操作手册，但不一定能看所有审批材料
- 管理员能看更完整的资料

所以检索前或检索后都要做权限过滤，不能把无权文档直接喂给模型。

### 5. 引用层

最后输出答案时，最好带引用。

建议引用信息至少包含：

- 来源类型
- 文档标题
- 文件名或页面名
- 片段摘要

这样用户才能判断答案是不是可信，后面审计也更方便。

## 真实项目里要重点考虑什么

### 1. 权限

不是所有资料都能全员看。

### 2. 更新频率

Wiki 往往更新快，文件服务器可能更新慢，必须考虑增量同步和版本控制。

### 3. 来源可信度

同一个问题可能同时命中文档和 Wiki，要明确谁是主来源，谁是辅助来源。

### 4. 可追溯性

答案要能追到具体文档和片段，不能只给“模型说的”。

### 5. 检索路由

有些问题偏制度，有些问题偏操作，有些问题偏排障。
可以先做简单路由，再决定要查哪些来源。

### 6. 审计与日志

最好记录：

- 谁问了什么
- 命中了哪些文档
- 哪些文档因为权限被过滤
- 最终返回了哪些引用

## 这类例子为什么值得做成可运行 demo

只讲概念不够。

如果要真的落到社内 Agent，这种例子最好做成能跑的最小版本，因为你可以直接验证：

- 接入层是不是能把不同来源统一成文档
- 权限层有没有生效
- 检索是不是能同时命中文件和 Wiki
- 引用是不是清楚
- 结果是不是足够像真实场景

## 推荐学习路径

1. 先看 [agent-lab/projects/doc_qa_agent](../agent-lab/projects/doc_qa_agent/README.md)
2. 再看 [agent-lab/projects/rag_api_demo](../agent-lab/projects/rag_api_demo/README.md)
3. 然后看 [agent-advanced/projects/advanced_rag_pipeline_demo](../agent-advanced/projects/advanced_rag_pipeline_demo/README.md)
4. 最后跑 [agent-advanced/projects/internal_hybrid_rag_demo](../agent-advanced/projects/internal_hybrid_rag_demo/README.md)

## 结论

社内文件 + Wiki 混合检索，本质上是一个“多来源知识接入 + 权限过滤 + 检索 + 引用”的 RAG 问题。
最适合先做一个可运行的最小例子，把真实项目里最容易踩坑的部分先跑通。
