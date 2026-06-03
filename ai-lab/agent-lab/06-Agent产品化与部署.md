# Agent 产品化与部署

## 目录

- [1. 这一章解决什么问题](#sec-1)
- [2. Agent 做成产品的常见形态](#sec-2)
- [3. 一般公司怎么部署 Agent](#sec-3)
- [4. Python Agent 的部署方式](#sec-4)
- [5. 是否一定需要前台画面](#sec-5)
- [6. Python Agent 怎么和页面结合](#sec-6)
- [7. 模型是 API 调用还是自社部署](#sec-7)
- [8. 当前 ai-lab 的学习路线](#sec-8)
- [9. 面试回答模板](#sec-9)
- [10. 日本现场关键词](#sec-10)
- [11. 记忆用一句话](#sec-11)

---

<a id="sec-1"></a>

## 1. 这一章解决什么问题

这一章回答一个非常现实的问题：

```text
学习阶段写出来的 Python Agent，怎样变成公司里可以使用的产品？
```

核心结论：

```text
Python Agent 通常不会直接给最终用户使用，而是部署成后端 API 服务。
用户一般通过浏览器画面、既存业务系统、Teams / Slack Bot，或者后台自动任务来使用 Agent。
```

在当前 `ai-lab` 目录里，最接近企业产品形态的 demo 是：

- [projects/rag_api_demo/README.md](./projects/rag_api_demo/README.md)
- [projects/rag_api_demo/main.py](./projects/rag_api_demo/main.py)

它代表的方向是：

```text
Python 脚本
-> FastAPI API 服务
-> Docker / 云环境部署
-> 前端、Bot 或企业系统调用
```

<a id="sec-2"></a>

## 2. Agent 做成产品的常见形态

### 2.1 Python Agent 后端 API

最常见的方式是用 `FastAPI` 把 Agent 包装成 HTTP API。

典型接口：

```text
GET  /health
POST /ask
POST /chat
POST /agent/run
POST /reload
```

系统结构：

```text
调用方
  -> FastAPI API
  -> Agent / RAG / Tool Calling
  -> LLM API / Vector DB / DB / 文件 / 外部系统
  -> JSON 返回
```

这种方式适合：

- 社内検索 API
- ナレッジ検索 API
- 文書QA API
- 問い合わせ分類 API
- 要約 API
- 既存系统集成

### 2.2 浏览器画面 + Python 后端

如果 Agent 是给普通业务用户使用，一般会准备前台画面。

常见结构：

```text
React / Vue / Next.js 画面
  -> FastAPI
  -> Agent / RAG / Tool Calling
  -> LLM / Vector DB / 社内文档
```

用户看到的是：

- 聊天窗口
- 社内知识检索页面
- 资料问答页面
- FAQ 自动回答页面
- 管理画面里的 AI 辅助按钮

也就是说，Python 负责后端智能处理，前端负责让用户容易使用。

### 2.3 既存业务系统内嵌 Agent

很多公司不会单独做一个新的 AI 网站，而是把 Agent 嵌入已有系统。

常见入口：

- 社内ポータル
- CRM
- ERP
- FAQ システム
- 申請システム
- 管理画面
- コールセンターシステム

系统结构：

```text
既存业务系统
  -> 调用 Agent API
  -> Python Agent 后端
  -> 返回建议、答案、摘要、分类结果
```

用户感觉上还是在原来的系统里工作，只是多了 AI 问答、AI 生成、AI 检索、AI 辅助确认等功能。

### 2.4 聊天工具型 Agent

企业内部也常见把 Agent 做成聊天工具里的 Bot。

常见入口：

- Microsoft Teams Bot
- Slack Bot
- LINE WORKS Bot
- 社内チャット Bot

系统结构：

```text
Teams / Slack
  -> Bot 后端
  -> Python Agent API
  -> LLM / RAG / Tool Calling
  -> 聊天工具中返回答案
```

这种形态不一定需要传统 Web 前台画面，因为聊天工具本身就是 UI。

### 2.5 后台自动处理型 Agent

有些 Agent 不是给用户聊天用，而是在后台自动执行。

常见场景：

- 定期检查资料
- 自动总结邮件
- 自动分类問い合わせ
- 自动生成报告
- 自动抽取文件中的关键信息
- 自动调用外部 API
- 自动检测异常日志

这类场景不一定需要前台画面，可以部署成：

- batch
- AWS Lambda
- ECS Task
- Cloud Run Job
- Kubernetes CronJob

<a id="sec-3"></a>

## 3. 一般公司怎么部署 Agent

比较标准的企业架构如下：

```text
用户浏览器 / 既存系统 / Teams / Slack
        |
        v
前端 UI / Bot / 业务系统按钮
        |
        v
API Gateway / Load Balancer
        |
        v
Python FastAPI Agent 服务
        |
        v
LLM API / Vector DB / DB / S3 / 社内文档 / 外部系统
```

其中 Python Agent 通常作为后端服务存在。

<a id="sec-4"></a>

## 4. Python Agent 的部署方式

### 4.1 开发阶段

本地启动：

```bash
uvicorn main:app --reload --port 8000
```

适合：

- 本地开发
- API 联调
- PoC 初期验证
- mock 模式测试

当前 `rag_api_demo` 就是这个阶段的练习。

### 4.2 PoC 阶段

常见部署：

```text
Docker + VM
Docker + ECS
Docker + Cloud Run
Docker + Azure App Service
```

这一阶段重点是证明：

- API 能被调用
- 文档能检索
- 回答质量可接受
- 日志能看
- 失败时能调查
- 成本大致可控

### 4.3 正式服务阶段

正式上线时，通常会补齐：

- 认证和权限控制
- API Gateway
- Load Balancer
- Docker image 管理
- CI/CD
- 日志收集
- 监控告警
- 成本限制
- 访问审计
- 数据权限控制
- Prompt / RAG 评估

部署环境可能是：

- AWS ECS / Fargate
- Kubernetes
- Azure App Service
- Azure Container Apps
- Google Cloud Run
- VM + Docker

### 4.4 轻量事件处理

如果是短时间、事件驱动的处理，可以考虑 Lambda。

适合 Lambda 的 Agent 相关处理：

- S3 文件上传后自动摘要
- 定期轻量检查
- 小规模文本分类
- 通知生成
- 轻量数据抽取

不适合 Lambda 的情况：

- 长时间运行
- 大量文档检索
- 需要常驻大模型周边服务
- 内存占用较大
- 复杂状态管理

<a id="sec-5"></a>

## 5. 是否一定需要前台画面

不一定。

可以按用户入口判断：

| 使用者 | 常见入口 | 是否需要前台画面 |
| --- | --- | --- |
| 普通业务用户 | 浏览器页面 | 通常需要 |
| 既存系统用户 | 业务系统内按钮或画面 | 不一定新做，可能嵌入 |
| 内部员工 | Teams / Slack Bot | 不需要传统 Web 画面 |
| 其他系统 | API 调用 | 不需要 |
| 后台任务 | 定时 / 事件触发 | 不需要 |

判断标准：

```text
如果人要直接使用，通常需要 UI。
如果系统调用 Agent，只需要 API。
如果后台自动处理，可以没有 UI。
```

<a id="sec-6"></a>

## 6. Python Agent 怎么和页面结合

### 6.1 核心理解

Python 写的 Agent 本身不是“页面”，它通常作为后端 API 服务存在。

React / Vue 负责页面，Python FastAPI 负责 Agent 能力。

最简单结构：

```text
浏览器页面 React / Vue
  -> HTTP 请求
  -> Python FastAPI Agent API
  -> RAG / Tool Calling / LLM API
  -> JSON 返回
  -> React / Vue 把答案显示在页面上
```

也就是说，页面不是“套在 Python 上”，而是通过 HTTP API 调用 Python 后端。

### 6.2 最小页面调用流程

用户在页面输入问题：

```text
请输入问题: 这个设计书的重点是什么？
```

React / Vue 发送请求：

```http
POST /ask
Content-Type: application/json

{
  "question": "这个设计书的重点是什么？"
}
```

Python FastAPI 返回：

```json
{
  "answer": "这个设计书主要说明了...",
  "sources": [
    {
      "source_label": "基本设计.md#chunk1",
      "score": 3
    }
  ]
}
```

React / Vue 拿到 JSON 后，把 `answer` 显示在聊天窗口或问答区域里，把 `sources` 显示成参考来源。

### 6.3 典型画面需要什么功能

一个最小 Agent 页面通常包括：

- 问题输入框
- 发送按钮
- 回答显示区域
- loading 状态
- 错误消息显示
- 参考来源显示
- 历史对话列表

更接近企业系统时，会增加：

- 登录用户信息
- 权限控制
- 文档范围选择
- 部门 / 项目选择
- 回答评价按钮
- 操作日志
- 使用量统计

### 6.4 React 调用 FastAPI 的形象代码

前端只需要把用户输入通过 HTTP 发给 Python API。

```typescript
async function askAgent(question: string) {
  const response = await fetch("http://localhost:8000/ask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });

  if (!response.ok) {
    throw new Error("Agent API call failed");
  }

  return await response.json();
}
```

这段代码的意思：

```text
React 页面
  -> fetch()
  -> FastAPI /ask
  -> Python Agent 执行
  -> 返回 answer
  -> 页面显示 answer
```

### 6.5 FastAPI 后端要准备什么

Python 后端需要准备：

- `/health`：健康检查
- `/ask`：单次问答
- `/chat`：多轮对话
- `/reload`：重载文档索引
- request model：规定前端传什么
- response model：规定返回给前端什么
- CORS 设置：允许前端域名调用 API
- 认证：确认是谁在调用
- 日志：记录请求、错误、耗时、成本

最小结构：

```text
main.py
  -> FastAPI app
  -> AskRequest
  -> AskResponse
  -> /health
  -> /ask
  -> Agent / RAG 处理
```

当前 `rag_api_demo` 已经有 `/health`、`/ask`、`/reload`，所以它就是“页面可以调用的后端 API 雏形”。

### 6.6 必须通过 Java 吗

不必须。

新做一个 AI 应用时，可以直接：

```text
React / Vue
  -> Python FastAPI
  -> Agent / RAG / LLM API
```

这种结构完全成立。

Java 出现的原因，通常是因为公司已有 Java / Spring Boot 业务系统。

既存系统场景：

```text
React / Vue
  -> Java Spring Boot 既存系统
  -> Python Agent API
  -> LLM API / RAG
```

这里 Java 不是 Agent 必须依赖的东西，而是既存业务系统入口，负责：

- 登录认证
- 权限控制
- 业务数据管理
- 审批流程
- 既存 DB 访问
- 原有 API
- 审计日志

一句话：

```text
Java 不是必须的。
新做 AI 应用：React / Vue + Python FastAPI 就够。
既存 Java 系统加 AI：Java 调用 Python Agent API。
```

### 6.7 页面结合时的部署结构

开发阶段：

```text
React dev server: http://localhost:3000
FastAPI server:   http://localhost:8000
```

本地开发时，React 通过 API URL 调用 FastAPI。

PoC / 正式环境：

```text
浏览器
  -> 前端静态资源 React / Vue
  -> API Gateway / Load Balancer
  -> Python FastAPI Agent 服务
  -> LLM API / Vector DB / 社内文档
```

前端可以部署在：

- S3 + CloudFront
- Vercel
- Netlify
- Nginx
- 既存 Web 系统

Python API 可以部署在：

- ECS / Fargate
- Kubernetes
- Azure App Service
- Cloud Run
- VM + Docker

### 6.8 学习时先做什么

学习顺序建议：

```text
1. 先跑通 rag_api_demo 的 /ask
2. 用 curl 或 Postman 调用 /ask
3. 写一个最小 React 页面，输入 question，显示 answer
4. 增加 loading 和错误处理
5. 显示 sources
6. 再考虑登录、权限、历史记录
```

不要一开始就做复杂前端。先确认：

```text
页面能调用 Python Agent API，并把回答显示出来。
```

这就是前后端结合的核心。

<a id="sec-7"></a>

## 7. 模型是 API 调用还是自社部署

### 7.1 大部分日本会社的常见做法

大部分日本会社做 Agent / 生成 AI 应用时，优先采用：

```text
通过 API 调用托管模型
```

常见模型服务：

- OpenAI API
- Azure OpenAI Service
- Amazon Bedrock
- Google Gemini API
- Anthropic Claude API

常见系统结构：

```text
业务系统 / Web画面 / Bot
  -> 自社开发的后端 API
  -> 调用 OpenAI API / Azure OpenAI / Bedrock / Gemini / Claude
  -> 返回结果
```

也就是说，公司主要开发和维护的是：

- 业务画面
- Agent 后端
- Prompt 管理
- RAG 检索
- 权限控制
- 日志监控
- 成本控制
- 与社内系统集成

模型本身多数情况下使用云服务提供的托管模型，而不是自己从零部署和运维大模型。

### 7.2 为什么多数公司不自己部署大模型

主要原因：

- 大模型部署成本高，需要 GPU。
- 运维复杂，需要处理推理服务、扩容、监控、版本升级。
- 模型更新速度快，自社维护负担大。
- PoC 阶段使用 API 更容易快速落地。
- 企业项目更关注业务集成，而不是训练或运维模型本身。
- 安全、权限、日志、RAG、既存系统连接才是应用开发重点。

日本现场常见关键词：

```text
生成AI API連携
Azure OpenAI連携
ChatGPT API連携
RAG基盤構築
社内文書検索AI
AIチャットボット
```

### 7.3 什么情况下会自社部署模型

自社部署或闭域环境部署也存在，但相对少，通常出现在安全要求更高的场景。

常见情况：

- 金融、医疗、政府等对数据外发限制非常严格。
- 客户要求数据不能发送到外部 API。
- 公司已有 GPU 基盘或私有云环境。
- 想使用 OSS LLM，例如 Llama、Qwen、Mistral 等。
- 调用量非常大，自建推理服务在成本上可能更合适。
- 需要完全控制模型、数据和运行环境。

这种场景常见说法：

```text
オンプレLLM
プライベートLLM
ローカルLLM
OSS LLM
自社LLM基盤
閉域環境でのLLM利用
```

### 7.4 API 调用型和自社部署型的区别

| 项目 | API 调用托管模型 | 自社部署 / 闭域 LLM |
| --- | --- | --- |
| 初期成本 | 低 | 高 |
| 上线速度 | 快 | 慢 |
| 运维负担 | 小 | 大 |
| GPU 管理 | 不需要 | 需要 |
| 模型更新 | 服务商负责 | 自社负责 |
| 数据控制 | 需要确认服务条款和安全设置 | 控制力更高 |
| 适合阶段 | PoC、一般业务系统、快速导入 | 高安全要求、大规模、闭域环境 |

记忆方式：

```text
多数项目：API 调用托管模型
少数项目：本社 / 闭域环境部署 OSS LLM
公司重点：不是造模型，而是把模型接进业务系统
```

<a id="sec-8"></a>

## 8. 当前 ai-lab 的学习路线

结合本工作区，推荐顺序是：

```text
chat_cli
-> doc_qa_agent
-> rag_api_demo
-> FastAPI API 化
-> Docker 化
-> 简单前端或既存系统调用
```

对应理解：

| 阶段 | Demo | 学习目标 |
| --- | --- | --- |
| CLI | `chat_cli` | 理解模型调用和命令行交互 |
| 本地 RAG | `doc_qa_agent` | 理解文档读取、切分、检索 |
| API 化 | `rag_api_demo` | 把能力包装成后端服务 |
| Tool | `tool_agent_demo` | 让 Agent 调用本地工具 |
| Workflow | `workflow_agent` | 把任务拆成可控步骤 |

最重要的一步：

```text
先把 Python Agent 做成 FastAPI 后端服务。
```

因为公司项目里最常见的不是“直接运行 Python 脚本”，而是：

```text
前端 / 既存系统 / Bot -> API -> Python Agent
```

<a id="sec-9"></a>

## 9. 面试回答模板

### Q1. Agent 要怎么做成公司里可以使用的产品

> Agentを製品として利用する場合、Pythonの処理をそのままユーザーに使わせるのではなく、FastAPIなどでバックエンドAPIとしてサービス化する形が一般的だと理解しております。  
> ユーザー向けには、ReactやVueなどのWeb画面、既存業務システムへの組み込み、またはTeams / Slack BotのようなチャットUIから利用するケースがあります。  
> 一方で、定期処理や自動分類、文書要約のようなバックグラウンド処理であれば、前台画面なしでLambdaやECSのバッチとして動かすケースもあります。

### Q2. Python Agent はどこに配置されますか

> Python Agentは、多くの場合バックエンドサービスとして配置されます。  
> FastAPIでAPI化し、Docker化した上で、ECS、Kubernetes、Azure App Service、Cloud Runなどにデプロイする構成が一般的だと理解しております。  
> フロントエンドや既存システム、Botは、そのAPIを呼び出してAgentの機能を利用します。

### Q3. ユーザーはブラウザでAgentを使うのですか

> ユーザーが直接使う場合は、ブラウザ画面から利用するケースが多いと思います。  
> ただし、必ず新しい画面を作るとは限らず、既存の社内ポータルや業務システムにAI機能として組み込むこともあります。  
> また、TeamsやSlackのBotとして提供する場合は、ユーザーはチャットツール上でAgentを利用します。

### Q4. 前台画面は必ず必要ですか

> 必ず必要ではありません。  
> 人が直接利用する場合はWeb画面やチャットUIが必要になりますが、他システムから呼び出す場合はAPIだけで十分です。  
> また、定期実行やイベント駆動の自動処理であれば、LambdaやECS Taskとしてバックグラウンドで動かす構成もあります。

### Q5. 自分の学習では何を作っていますか

> 個人学習では、まずCLIでモデル呼び出しを確認し、その後、RAGによる文書検索、FastAPIによるAPI化まで学習しております。  
> 現在は、Python Agentを単なるスクリプトではなく、企業システムから呼び出せるAPIサービスとして整理することを意識して学習しています。  
> 今後はDocker化、認証、ログ、簡単なフロント画面との連携まで確認したいと考えております。

### Q6. 日本会社ではAgent用の大模型を自社部署しますか、それともAPIを使いますか

> 日本の現場では、現時点では自社で大規模モデルを一から構築・運用するよりも、OpenAI API、Azure OpenAI、Amazon Bedrock、Gemini APIなどのマネージドサービスを利用し、その上にRAG、Agent、業務システム連携を実装するケースが多いと理解しております。  
> 自社側では、モデルそのものよりも、認証、権限管理、プロンプト設計、社内文書検索、ログ管理、コスト管理、既存システムとのAPI連携を担当するイメージです。  
> 一方で、セキュリティ要件が非常に高い場合や閉域環境が必要な場合は、オンプレミスやプライベート環境でOSS LLMを運用するケースもあると理解しております。

短く答える場合：

> 多くの案件では、OpenAI APIやAzure OpenAIなどのマネージドモデルをAPI経由で利用し、自社側ではRAG、Agent、権限管理、既存システム連携を実装する形が多いと理解しております。  
> ただし、閉域環境や高いセキュリティ要件がある場合は、OSS LLMを自社環境にデプロイするケースもあります。

### Q7. Python Agent はどうやってReactやVueの画面と連携しますか

> Python AgentはFastAPIなどでバックエンドAPIとして公開し、ReactやVueの画面からHTTPで呼び出す構成になります。  
> 例えば、ユーザーが画面で質問を入力すると、フロントエンドが `/ask` APIにJSON形式で質問を送信し、Python側でRAGやLLM API連携を行って、回答と参照元をJSONで返します。  
> フロントエンド側では、その回答をチャット画面や検索結果画面に表示するイメージです。

### Q8. Agentを作るときJavaは必須ですか

> Javaは必須ではありません。  
> 新規でAIアプリを作る場合は、ReactやVueのフロントエンドからPython FastAPIのAgent APIを直接呼び出す構成で問題ありません。  
> ただし、既存の業務システムがJava / Spring Bootで作られている場合は、既存Javaシステムを残したまま、AI部分だけをPython Agent APIとして追加し、Java側から呼び出す構成もあります。  
> つまり、JavaはAgentのために必須というより、既存業務システム、認証、権限、業務データ連携を活かすために使われることが多いと理解しております。

<a id="sec-10"></a>

## 10. 日本现场关键词

| 中文 | 日本語 | 现场表达 |
| --- | --- | --- |
| 产品化 | 製品化 / サービス化 | Agentをサービス化します |
| 后端 API | バックエンドAPI | FastAPIでAPI化します |
| 托管模型 | マネージドモデル | Azure OpenAIなどのマネージドモデルを利用します |
| 模型 API 调用 | モデルAPI連携 | OpenAI APIと連携します |
| 自社部署模型 | 自社LLM基盤 / プライベートLLM | 閉域環境でOSS LLMを運用します |
| 前台画面 | フロント画面 / Web画面 | Reactの画面からAPIを呼び出します |
| 页面和后端结合 | フロントエンド連携 | ReactからFastAPIのAgent APIを呼び出します |
| API 请求 | APIリクエスト | `/ask` にJSONで質問を送信します |
| API 返回 | APIレスポンス | 回答と参照元をJSONで返します |
| 跨域设置 | CORS設定 | フロント画面からAPIを呼び出せるようにします |
| 既存系统嵌入 | 既存システムへの組み込み | 業務システムにAI機能を組み込みます |
| 聊天机器人 | チャットBot | Teams Botとして利用します |
| 后台处理 | バックグラウンド処理 | ECS TaskやLambdaで実行します |
| 容器化 | コンテナ化 | Docker化してデプロイします |
| 负载均衡 | ロードバランサー | LB経由でAPIを公開します |
| 健康检查 | ヘルスチェック | `/health` で稼働確認します |
| 监控 | 監視 | ログ、メトリクス、アラートを設定します |

<a id="sec-11"></a>

## 11. 记忆用一句话

```text
Agent 产品化 = Python Agent 后端 API 化 + 用户入口 UI / Bot / 既存系统 + 云上部署和运维。
```

日语一句话：

```text
AgentはPython処理をFastAPIでバックエンドAPI化し、Web画面、既存システム、またはBotから利用する形でサービス化するのが一般的です。
```

模型利用方式：

```text
多くの日本案件では、モデル自体はOpenAI APIやAzure OpenAIなどを利用し、自社側ではRAG、Agent、権限管理、既存システム連携を実装します。
```

页面结合方式：

```text
React / Vueの画面からPython FastAPIのAgent APIを呼び出し、回答をJSONで受け取って画面に表示します。
```
