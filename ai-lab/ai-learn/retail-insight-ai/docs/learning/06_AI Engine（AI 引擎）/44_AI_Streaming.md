
# Retail Insight AI 企业源码架构手册

# Volume 06：AI Engine（AI 引擎）

# Chapter 44

# AI Streaming（AI 流式输出）

> Deliver AI Responses in Real Time

---

# 文档信息

| 项目     | 内容                                                                          |
| -------- | ----------------------------------------------------------------------------- |
| Volume   | 06                                                                            |
| Chapter  | 44                                                                            |
| 技术主题 | AI Streaming                                                                  |
| 难度     | ⭐⭐⭐⭐⭐                                                                    |
| 推荐程度 | ⭐⭐⭐⭐⭐                                                                    |
| 对应源码 | backend/app/api/tasks.py / backend/app/events/ / backend/app/sse/（未来扩展） |

---

# 学习目标

阅读本章后，你应该能够回答：

- 什么是 AI Streaming？
- 为什么 AI Agent 需要 Streaming？
- SSE 与 Streaming 有什么关系？
- Retail Insight AI 如何实现实时输出？
- 企业 AI 为什么几乎都会采用 Streaming？

---

# 一、为什么需要 Streaming？

假设：

LLM：

需要：

30 秒。

如果：

30 秒以后：

浏览器：

才看到：

第一句话。

用户会认为：

系统：

已经：

卡住。

因此：

现代 AI：

几乎：

全部：

Streaming。

---

# 二、什么是 Streaming？

传统：

```text
Question

↓

LLM

↓

等待

↓

完整 Answer
```

Streaming：

```text
Question

↓

LLM

↓

Token1

↓

Token2

↓

Token3

↓

Finished
```

用户：

马上：

看到：

输出。

---

# 三、Retail Insight AI 当前实现（Current）

当前：

Workflow：

完成：

以后：

通过：

EventPublisher：

发送：

事件。

SSE：

持续：

推送：

状态。

整体：

```text
Browser

↓

SSE

↓

EventPublisher

↓

Workflow
```

虽然：

目前：

主要：

Streaming：

Workflow 状态。

未来：

可以：

Streaming：

LLM Token。

---

# 四、源码目录结构 ⭐

建议阅读：

```text
backend/app/events/

↓

publisher.py
```

继续：

```text
backend/app/api/tasks.py
```

观察：

SSE：

如何：

建立。

---

# 五、关键源码文件 ⭐

重点：

```text
publisher.py

↓

publish()

↓

SSE Endpoint

↓

Browser
```

未来：

Provider：

也可以：

Streaming：

Token。

---

# 六、Streaming 执行流程 ⭐

```text
Question

↓

Workflow

↓

LLM

↓

Token Stream

↓

Publisher

↓

SSE

↓

Browser
```

不是：

最后：

一起：

返回。

而是：

边生成：

边发送。

---

# 七、Workflow Streaming ⭐

Workflow：

除了：

Token。

还可以：

Streaming：

状态。

例如：

```text
Workflow Started

↓

Research Running

↓

Research Completed

↓

Report Running

↓

Completed
```

用户：

知道：

系统：

正在：

执行。

---

# 八、Token Streaming ⭐

未来：

Provider：

建议：

支持：

```text
Token

↓

Publisher

↓

SSE

↓

Browser
```

浏览器：

实时：

显示：

AI：

回答。

---

# 九、SSE 与 Streaming

很多人：

认为：

SSE：

就是：

Streaming。

实际上：

不是。

Streaming：

表示：

持续输出。

SSE：

只是：

实现：

Streaming：

的一种：

协议。

除此之外：

还有：

- WebSocket
- HTTP Chunked
- gRPC Streaming

---

# 十、Architecture Thinking ⭐

为什么：

企业：

喜欢：

Streaming？

因为：

等待：

30 秒。

体验：

很差。

Streaming：

100ms：

看到：

第一句话。

用户：

认为：

系统：

很快。

---

# 十一、Retail Insight AI 实施方案 ⭐

建议：

未来：

Workflow：

增加：

```text
LLM Token

↓

Publisher.publish()

↓

SSE

↓

Browser
```

形成：

完整：

Streaming AI。

---

# 十二、Learning Trace 对应 ⭐

建议：

增加：

```text
Workflow Started

↓

Token Streaming

↓

Workflow Running

↓

Completed
```

方便：

观察：

Streaming。

---

# 十三、Debug Guide ⭐

建议：

断点：

```text
① Workflow Start

↓

② Provider Stream

↓

③ Publisher

↓

④ SSE

↓

⑤ Browser
```

观察：

Token：

是否：

实时：

发送。

---

# 十四、Performance & Cost ⭐

Streaming：

不会：

减少：

Token。

但是：

能够：

降低：

用户：

等待：

感知。

企业：

建议：

统计：

- First Token Time
- Tokens / Second
- Streaming Duration
- Network Delay

---

# 十五、Current vs Enterprise

Current：

```text
Workflow

↓

Publisher

↓

SSE
```

Enterprise：

```text
Workflow

↓

LLM Streaming

↓

Publisher

↓

SSE

↓

Browser
```

真正：

实现：

实时：

AI。

---

# 十六、Java / Spring 对照 ⭐

| Retail Insight AI | Spring                    |
| ----------------- | ------------------------- |
| SSE               | SseEmitter                |
| Publisher         | ApplicationEventPublisher |
| Token Stream      | Flux<String></string>     |
| Streaming         | Spring WebFlux            |

---

# 十七、VS Code 阅读路线 ⭐

建议：

```text
tasks.py

↓

publisher.py

↓

SSE

↓

Frontend
```

观察：

Streaming：

整个：

调用链。

---

# 十八、企业扩展（Enterprise）

未来：

建议：

支持：

```text
Streaming

↓

WebSocket

↓

Multi Client

↓

Backpressure

↓

Realtime Dashboard
```

形成：

企业：

实时：

AI 平台。

---

# 十九、面试回答（中文）

为什么 AI 系统要采用 Streaming？

Streaming 可以让模型生成内容时立即返回给用户，而不是等待全部完成。这不仅提升用户体验，也便于展示 Workflow 执行状态，是 ChatGPT、Gemini、Claude 等现代 AI 产品的标准能力。

---

# 二十、面试回答（日文）

なぜ AI Streaming が必要ですか。

Streaming を利用すると、LLM が生成した Token をリアルタイムで画面へ表示できます。ユーザーは待ち時間を短く感じられ、AI システムの応答性も向上します。

---

# 二十一、日本 SES 常见追问

### Q：SSE 和 WebSocket 有什么区别？

| SSE               | WebSocket      |
| ----------------- | -------------- |
| 单向              | 双向           |
| 简单              | 功能更多       |
| AI Streaming 常用 | Chat、游戏常用 |
| HTTP              | 独立协议       |

---

# 二十二、本章练习 ⭐

完成下面练习：

① 阅读：

```text
backend/app/events/publisher.py
```

↓

② 找到：

SSE：

发送：

位置。

↓

③ 思考：

如果：

Streaming：

LLM Token。

Workflow：

需要：

修改：

哪些：

地方？

---

# 二十三、本章核心记忆图 ⭐

```text
Question

↓

Workflow

↓

LLM

↓

Token

↓

Publisher

↓

SSE

↓

Browser
```

---

# 二十四、本章总结

一句话：

```text
Streaming

负责：

实时输出

↓

SSE

负责：

持续传输

↓

Browser

负责：

实时显示
```

AI Streaming 的核心价值在于：

**让用户在模型生成过程中持续获得反馈，而不是等待最终结果。**

对于 Retail Insight AI 来说，未来结合 **LLM Token Streaming + EventPublisher + SSE**，可以构建接近 ChatGPT 的实时交互体验。

---

# 下一章

**Chapter 45：MCP Architecture（Model Context Protocol）**

学习：

- MCP
- Tool Calling
- Filesystem
- Database
- GitHub
- Enterprise Tool Integration
