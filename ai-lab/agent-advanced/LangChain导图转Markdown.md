# LangChain从入门到实战（导图转Markdown）

# LangChain从入门到实战- author：宋红康
## 01-LangChain的概述
### 基本理解
#### 什么是LangChain
#### 使用LangChain能开发什么？
##### RAG
##### Agent
#### 有哪些开发大模型的框架
##### LangChain
##### LlamaIndex
##### LangChain4J
##### SpringAI/SpringAI Alibaba
##### SemanticKernel
#### 核心模块
##### Model I/O
##### Chains
##### Memory
##### Agents
##### Retrieval
##### Callbacks
### 大模型应用1：RAG
### 大模型应用2：Agent
## 02-模块1：Model IO之大模型调用
### 大模型分类
### 获取大模型的标准代码
#### 非对话模型
#### 对话模型
#### .env配置文件
### 模型的调用方法
#### invoke()
#### stream()
#### batch()
### 私有模型的调用
#### Ollama的下载与安装
#### 调用私有模型
## 02-模块1：Model IO之提示词模板
### Prompt Template
#### 两种实例化方式
##### 构造方法
##### from_template()
#### 部分提示词赋值
#### format() 与 invoke()
#### 结合LLM调用
### ChatPromptTemplate
#### 两种实例化方式
##### 构造方法
##### from_messages()
#### 模板调用的几种方式
##### format()
##### invoke()
##### format_messages()
##### format_prompt()
#### 更丰富的参数类型
##### 了解：字符串类型
##### 了解：字典类型
##### 消息类型
##### ChatPromptTemplate类型
##### BaseMessagePromptTemplate类型
#### 结合LLM调用
##### 举例1
##### 举例2
#### MessagesPlaceholder
### 少量样本示例的提示词模板
#### FewShotPromptTemplate
#### FewShotChatMessagePromptTemplate
### 了解：其它
## 02-模块1：Model IO之输出解析器
### StrOutputParser
### JsonOutputParser (重点)
#### 举例1
#### 举例2
### XMLOutputParser（了解）
### CommaSeparatedListOutputParser (了解)
### DatetimeOutputParser (了解)
## 03-模块2：Chains
### 传统的Chain
#### LLMChain
##### 举例1
##### 举例2
#### 顺序链之SimpleSequentialChain
##### 举例1
##### 举例2
#### 顺序链之 SequentialChain
##### 举例
##### 实际应用举例
#### 数学链 LLMMathChain (了解)
#### StuffDocumentsChain(了解)
### LCEL语法的使用
#### 基本概念
#### 举例1
##### 不使用Chain
##### 使用Chain
### 基于LCEL的Chain
#### create_sql_query_chain
#### create_stuff_documents_chain(了解)
## 04-模块3：Memory
### 理论
### ChatMessageHistory(基础)
### ConversationBufferMemory
#### 基础举例
#### 结合Chain
#### 使用ChatPromptTemplate
### ConversationChain
#### 理解
#### 举例
### ConversationBufferWindowMemory
#### 入门举例
#### 结合chain
### ConversationTokenBufferMemory(了解）
#### 举例
### ConversationSummaryMemory(了解)
#### 举例
### ConversationSummaryBufferMemory(了解)
#### 举例
## 05-模块4：Tools
### 理论
### 自定义工具方式1
#### 举例1
#### 举例2
#### 举例3
### 自定义工具方式2
#### 举例1
### 工具的调用
## 06-模块5：Agents
### Agent的核心能力/组件
### Agent、AgentExecutor的创建
### 工具的调用
#### 传统方式举例
##### React模式
##### FUNCTION_CALL模式
#### 通用方式举例
##### FUNCTION_CALL模式
##### React模式
#### 自定义工具举例
### 记忆组件的使用
#### 传统方式举例
#### 通用方式举例
## 07-模块6：Retrieval
### 理论
### 环节1：文档加载器 Document Loaders
#### 加载Txt
#### 加载pdf
#### 加载CSV
#### 加载JSON
### 环节2：文档拆分器 Text Splitters
#### Chunking拆分的策略
#### CharacterTextSplitter：Split by character
#### RecursiveCharacterTextSplitter：最常用
#### CharacterTextSplitter：Split by tokens(了解)
#### SemanticChunker：语义分块
### 环节3：文档嵌入模型 Text Embedding Models
#### 句子的向量化（embed_query）
#### 文档的向量化（embed_documents）
### 环节4：向量存储(Vector Stores)
#### 数据的存储
#### 数据的检索
##### 相似性检索（similarity_search）
##### 支持直接对问题向量查询（similarity_search_by_vector）
##### 相似性检索，支持过滤元数据（filter）
##### 通过L2距离分数进行搜索（similarity_search_with_score）
##### 通过余弦相似度分数进行搜索（_similarity_search_with_relevance_scores）
##### MMR（最大边际相关性，max_marginal_relevance_search）
### 环节5：检索器(召回器) Retrievers
#### 默认检索器使用相似性搜索
#### 分数阈值查询
#### MMR搜索
#### 结合LLM
### 项目：智能对话助手
#### 定义工具
#### Retriever
#### 创建工具、工具集
#### 语言模型调用工具
#### 创建Agent程序(使用通用方式)
#### 运行Agent
#### 添加记忆