
# Retail Insight AI 企业源码架构手册

# Volume 06：AI Engine（AI 引擎）

# Chapter 41

# Prompt Engineering（Prompt 工程）

> Design Prompts for Enterprise AI Systems

---

# 文档信息

| 项目     | 内容                                                   |
| -------- | ------------------------------------------------------ |
| Volume   | 06                                                     |
| Chapter  | 41                                                     |
| 技术主题 | Prompt Engineering                                     |
| 难度     | ⭐⭐⭐⭐⭐                                             |
| 推荐程度 | ⭐⭐⭐⭐⭐                                             |
| 对应源码 | backend/app/workflow/graph.py / backend/app/providers/ |

---

# 学习目标

阅读本章后，你应该能够回答：

- Prompt 在 AI Engine 中的作用是什么？
- System Prompt 与 User Prompt 有什么区别？
- 为什么企业需要 Prompt Template？
- 如何设计可维护的 Prompt？
- Prompt 如何结合 Workflow 与 RAG？

---

# 一、什么是 Prompt？

Prompt 并不是一句简单的话。

在企业 AI 系统中：

Prompt 是：

> **AI 的业务规则（Business Rule）。**

AI 是否输出正确结果，

很大程度取决于 Prompt 的设计。

---

# 二、ERIP 当前实现（Current）

当前 AI 调用流程：

```text
Workflow

↓

Prepare Context

↓

Generate Prompt

↓

LLM

↓

Structured Result
```

Workflow：

负责组织流程。

Prompt：

负责告诉模型：

要完成什么任务。

---

# 三、源码目录结构 ⭐

建议阅读：

```text
backend/app/workflow/

↓

graph.py
```

继续阅读：

```text
backend/app/providers/
```

重点关注：

Prompt 是在哪里构造，

Provider 如何发送给模型。

---

# 四、关键源码文件 ⭐

建议重点阅读：

```text
graph.py

↓

AnalysisWorkflow

↓

Provider

↓

LLM Request
```

阅读时：

重点观察：

- Prompt 来源
- Context 来源
- Model 输入

---

# 五、Prompt 生命周期 ⭐

一个 Prompt 的形成过程：

```text
User Request

↓

Workflow

↓

Business Context

↓

Prompt Template

↓

Final Prompt

↓

LLM
```

企业 Prompt 很少直接拼接字符串。

通常会经过统一模板。

---

# 六、Prompt 的组成 ⭐

企业 Prompt 一般包含：

```text
Role

↓

Instruction

↓

Context

↓

Constraints

↓

Output Format
```

例如：

```text
Role：

Retail Analyst

Instruction：

Analyze KPI

Context：

Sales Data

Output：

JSON
```

这样模型输出更加稳定。

---

# 七、Prompt Template ⭐

企业项目通常不会：

```python
prompt = "...字符串..."
```

而是：

```text
Prompt Template

+

Variables

↓

Final Prompt
```

例如：

```text
{company}

{period}

{kpi}

{language}
```

统一模板，

方便维护。

---

# 八、Structured Output

企业 AI：

通常要求：

固定输出。

例如：

```json
{
  "summary":"",
  "risk":"",
  "recommendation":""
}
```

而不是：

一大段自由文本。

这样：

方便：

Workflow

继续处理。

---

# 九、Prompt Versioning

企业项目：

Prompt：

也需要版本管理。

例如：

```text
Prompt v1.0

↓

Prompt v1.1

↓

Prompt v2.0
```

出现问题：

可以快速回滚。

---

# 十、Architecture Thinking ⭐

为什么 Prompt 不直接写在代码里？

因为：

Prompt：

会不断优化。

如果：

直接修改源码：

维护成本很高。

企业通常：

Prompt 独立管理。

Workflow：

负责调用。

---

# 十一、Current vs Enterprise

Current：

```text
Workflow

↓

Prompt

↓

LLM
```

Enterprise：

```text
Workflow

↓

Prompt Library

↓

Prompt Version

↓

Prompt Validation

↓

LLM
```

形成完整 Prompt 管理体系。

---

# 十二、Java / Spring 对照 ⭐

| Retail Insight AI | Java AI        |
| ----------------- | -------------- |
| Prompt            | PromptTemplate |
| Workflow          | AI Flow        |
| Context           | Context Object |
| Structured Output | DTO            |

---

# 十三、VS Code 阅读路线 ⭐

建议：

```text
graph.py

↓

Provider

↓

Prompt Build

↓

LLM Request
```

观察：

Prompt：

如何生成。

---

# 十四、Debug Guide ⭐

建议断点：

```text
① Workflow Start

↓

② Prompt Generate

↓

③ Provider Send

↓

④ LLM Response

↓

⑤ Result Parse
```

调试时：

重点查看：

最终 Prompt 内容。

---

# 十五、Learning Trace 对应 ⭐

建议增加：

```text
Workflow Started

↓

Prompt Generated

↓

LLM Request

↓

LLM Response

↓

Workflow Continue
```

这样：

可以快速定位 Prompt 问题。

---

# 十六、Prompt Design Checklist ⭐

企业 Prompt 建议检查：

- 是否明确角色（Role）
- 是否限定任务范围
- 是否提供 Context
- 是否定义输出格式
- 是否避免歧义
- 是否支持版本管理

每次修改 Prompt，

建议重新验证。

---

# 十七、企业扩展（Enterprise）

未来建议增加：

```text
Prompt Library

↓

Prompt Version

↓

Prompt Evaluation

↓

A/B Testing

↓

Prompt Audit
```

形成完整 Prompt 管理平台。

---

# 十八、面试回答（中文）

为什么企业需要 Prompt Template？

Prompt Template 可以把固定规则与业务变量分离，提高 Prompt 的可维护性和复用性。当业务变化时，只需要修改变量或模板，而不用修改 Workflow 代码。

---

# 十九、面试回答（日文）

なぜ Prompt Template を利用するのですか。

Prompt Template を利用することで、固定部分と変数部分を分離できます。保守性・再利用性が向上し、業務変更にも柔軟に対応できます。

---

# 二十、日本 SES 常见追问

### Q：Prompt 越长越好吗？

回答：

不是。

好的 Prompt：

应该：

- 清晰
- 明确
- 可维护
- 可复用

而不是：

越长越好。

---

# 二十一、本章练习 ⭐

完成下面练习：

① 阅读：

```text
backend/app/workflow/graph.py
```

↓

② 找出：

Prompt 是在哪里生成？

↓

③ 设计：

一个 KPI 分析 Prompt Template。

↓

④ 思考：

哪些内容应该作为变量？

---

# 二十二、本章核心记忆图 ⭐

```text
Workflow

↓

Context

↓

Prompt Template

↓

Final Prompt

↓

LLM

↓

Structured Result
```

---

# 本章总结

一句话：

```text
Workflow

组织流程

↓

Prompt

定义任务

↓

LLM

完成推理
```

Prompt Engineering 的核心目标是：

**将 AI 指令标准化、模板化、可维护化。**

企业 AI 系统不会把 Prompt 当作普通字符串，而是将其作为一种可管理、可版本化、可持续优化的重要资产。

---

# 下一章

**Chapter 42：RAG Architecture（检索增强生成）**

学习：

- Retriever
- Embedding
- Chunk
- Hybrid Search
- Knowledge Base
- 企业知识库架构
