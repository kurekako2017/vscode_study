# RAG 文档读取路径、Top K、Chunk 切分补足学习资料

> 适用对象：正在学习本地 RAG / 文档问答 / LangChain 或 Agent 检索流程的初学者。  
> 对应示例：`main.py` 本地 RAG 文档问答最小示例。

---

## 1. 这个例子整体在做什么？

这个 `main.py` 是一个最小版的本地 RAG 文档问答程序。

它的核心流程是：

```text
用户问题
   ↓
指定文档目录 --docs
   ↓
扫描目录中的 .md / .txt 文件
   ↓
读取文件内容
   ↓
把长文档切成多个 chunk
   ↓
根据问题检索最相关的 Top K 个 chunk
   ↓
把这些 chunk 拼成上下文 context
   ↓
交给大模型回答
   ↓
输出答案和 sources 来源
```

也就是说，RAG 不是直接把整个文档全部塞给模型，而是先从文档中找出最相关的几个片段，再让模型基于这些片段回答。

---

## 2. 文档路径是怎么指定的？

在这个例子中，文档路径通过命令行参数 `--docs` 指定。

示例：

```bash
python3 main.py "交通费怎么报销？" --docs ./docs
```

意思是：

```text
问题：交通费怎么报销？
文档目录：./docs
```

如果不写 `--docs`，默认读取当前目录：

```bash
python3 main.py "交通费怎么报销？"
```

等同于：

```bash
python3 main.py "交通费怎么报销？" --docs .
```

代码中对应的位置：

```python
parser.add_argument(
    "--docs",
    default=".",
    help="Directory containing local markdown or text files. Default: current directory.",
)
```

在 `main()` 中会把路径转换成绝对路径：

```python
base_dir = Path(args.docs).resolve()
```

例如：

```bash
--docs ./docs
```

可能会被转换成：

```text
/home/victor/project/docs
```

这样后续程序就知道应该去哪个目录里读取资料。

---

## 3. 实际运行命令怎么写？

### 3.1 读取当前目录

```bash
python3 main.py "请总结这个目录中的 RAG 思路"
```

默认读取：

```text
当前目录 .
```

---

### 3.2 读取指定 docs 目录

```bash
python3 main.py "会社的请假制度是什么？" --docs ./docs
```

读取：

```text
./docs
```

---

### 3.3 读取上级目录

```bash
python3 main.py "请总结这个项目的学习内容" --docs ../../..
```

读取：

```text
当前目录往上三级的目录
```

这个命令适合在某个子目录里运行，但想检索整个大项目资料时使用。

---

## 4. 程序会读取哪些文件？

这个例子只读取两种文件：

```python
SUPPORTED_EXTENSIONS = {".md", ".txt"}
```

也就是：

```text
.md  Markdown 文件
.txt 纯文本文件
```

不会读取：

```text
.pdf
.docx
.xlsx
.html
.py
.json
```

如果你想让它读取 PDF、Word、Excel，需要额外增加解析逻辑。

---

## 5. 程序是怎么扫描文件的？

代码中有一个函数：

```python
def iter_text_files(base_dir: Path) -> list[Path]:
    files = []
    for path in base_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(path)
    return sorted(files)
```

重点是：

```python
base_dir.rglob("*")
```

这表示：

```text
递归扫描 base_dir 目录下的所有文件和子目录
```

例如目录结构：

```text
docs/
├── company.md
├── rules/
│   ├── vacation.md
│   └── traffic.md
└── faq/
    └── common.txt
```

程序会读到：

```text
docs/company.md
docs/rules/vacation.md
docs/rules/traffic.md
docs/faq/common.txt
```

因为它是递归扫描，所以子目录里的 `.md` 和 `.txt` 也会被读取。

---

## 6. 文档是怎么被读取的？

读取文件的代码在 `build_chunks()` 中：

```python
text = file_path.read_text(encoding="utf-8")
```

也就是说，它按 UTF-8 编码读取文本。

如果文件不是 UTF-8 编码，可能会出现 `UnicodeDecodeError`，这个例子会直接跳过这个文件：

```python
except UnicodeDecodeError:
    continue
```

所以实际项目中，文档编码最好统一成 UTF-8。

---

## 7. Chunk 是什么？

Chunk 可以理解成：

```text
把一篇长文档切成很多小片段
```

为什么要切？

因为实际文档可能很长，例如：

```text
就业规则.md：5万字
系统操作手册.md：10万字
公司 FAQ.md：2万字
```

大模型不能每次都读取全部内容，而且全部塞进去也会：

```text
成本高
速度慢
上下文太长
答案容易混乱
```

所以 RAG 会先把文档切成小块，再根据问题找最相关的小块。

---

## 8. 这个例子怎么切 Chunk？

当前设置是：

```python
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200
```

意思是：

```text
每个 chunk 大约 1200 个字符
相邻 chunk 之间重叠 200 个字符
```

示意：

```text
原文：0 ------------------------------------------------ 3000

chunk1：0 ---------------- 1200
chunk2：1000 ------------- 2200
chunk3：2000 ------------- 3000
```

可以看到：

```text
chunk1 和 chunk2 重叠 200 字符
chunk2 和 chunk3 重叠 200 字符
```

---

## 9. 为什么需要 Chunk Overlap？

如果没有重叠，可能会发生这种情况：

```text
chunk1 结尾：交通费报销需要在每月
chunk2 开头：25日之前提交申请
```

如果用户问：

```text
交通费什么时候提交？
```

单独看 chunk1，不完整。

单独看 chunk2，也缺少主语。

所以加入 overlap 后，chunk2 可能会包含上一段结尾内容：

```text
交通费报销需要在每月 25 日之前提交申请
```

这样检索效果会更好。

---

## 10. Chunk 切分代码解释

代码：

```python
def chunk_text(text: str) -> list[str]:
    normalized = text.replace("\r\n", "\n").strip()
    if not normalized:
        return []

    chunks = []
    start = 0
    while start < len(normalized):
        end = min(len(normalized), start + CHUNK_SIZE)
        chunks.append(normalized[start:end])
        if end >= len(normalized):
            break
        start = end - CHUNK_OVERLAP
    return chunks
```

逐步理解：

```python
normalized = text.replace("\r\n", "\n").strip()
```

统一换行符，并去掉前后空白。

```python
start = 0
```

从第 0 个字符开始切。

```python
end = min(len(normalized), start + CHUNK_SIZE)
```

每次最多切 1200 个字符。

```python
chunks.append(normalized[start:end])
```

把这一段加入 chunks。

```python
start = end - CHUNK_OVERLAP
```

下一块不是从 `end` 开始，而是往回退 200 个字符。

这就是重叠切分。

---

## 11. Chunk 的标签 source_label 是什么？

每个 chunk 都会带一个来源标签：

```python
label = f"{relative}#chunk{index}"
```

例如：

```text
rules/traffic.md#chunk1
rules/traffic.md#chunk2
faq/common.txt#chunk1
```

这个标签很重要，因为最终回答会输出 Sources：

```text
=== Sources ===
- rules/traffic.md#chunk1 (score=3)
- faq/common.txt#chunk2 (score=1)
```

这样你可以知道：

```text
模型回答是参考了哪个文件、哪个 chunk
```

这就是 RAG 中的“可追溯来源”。

---

## 12. Top K 是什么意思？

Top K 的意思是：

```text
从所有 chunk 中，取最相关的前 K 个
```

这个例子中：

```python
TOP_K = 4
```

意思是：

```text
最多取前 4 个最相关的 chunk
```

---

## 13. Top K 举例说明

假设有 100 个 chunk。

用户问：

```text
交通费怎么报销？
```

系统给每个 chunk 打分：

```text
chunk1：公司介绍，score=0
chunk2：请假制度，score=0
chunk3：交通费报销流程，score=3
chunk4：报销截止日，score=2
chunk5：发票提交规则，score=1
chunk6：工资制度，score=0
```

如果：

```python
TOP_K = 4
```

最终会取：

```text
chunk3
chunk4
chunk5
再取一个分数靠前的 chunk
```

然后把这些 chunk 拼接成 context 给模型。

---

## 14. 这个例子的检索方式是什么？

这个例子不是向量检索。

它用的是简单的关键词重合度。

代码中：

```python
question_tokens = tokenize(question)
chunk_tokens = tokenize(chunk.content)
overlap = question_tokens & chunk_tokens
score = len(overlap)
```

意思是：

```text
问题中的词 和 chunk 中的词 重合越多，分数越高
```

例如问题：

```text
交通费怎么报销？
```

问题 tokens 可能是：

```text
交通费 / 怎么 / 报销
```

某个 chunk 内容：

```text
交通费报销需要在每月 25 日之前提交。
```

chunk tokens 可能有：

```text
交通费 / 报销 / 每月 / 25 / 提交
```

重合词：

```text
交通费 / 报销
```

所以：

```text
score = 2
```

---

## 15. 这个检索方式有什么问题？

关键词检索容易理解，但有明显缺点。

例如用户问：

```text
电车费用如何申请？
```

文档写的是：

```text
交通费报销流程
```

虽然意思接近，但关键词不完全一样。

关键词检索可能匹配不到。

而向量检索可以理解语义：

```text
电车费用 ≈ 交通费
申请 ≈ 报销
```

所以生产环境一般会使用：

```text
embedding + 向量数据库
```

例如：

```text
OpenAI embeddings
Qwen embeddings
nomic-embed-text
FAISS
Chroma
Milvus
Qdrant
pgvector
```

---

## 16. 当前例子和生产级 RAG 的区别

当前教学版：

```text
读取 .md / .txt
按字符切 chunk
关键词重合度检索
Top K 固定为 4
每次运行都重新读取和切分
```

生产级 RAG：

```text
支持 PDF / Word / Excel / HTML / Markdown
按标题、段落、语义切 chunk
用 embedding 做向量检索
Top K 可配置
文档向量化后存入数据库
支持增量更新
支持权限控制
支持来源引用
支持缓存
支持日志和监控
```

---

## 17. 实际会社资料路径一般怎么设计？

实际项目中，会社资料通常会放在固定目录。

例如：

```text
company-rag/
├── main.py
├── data/
│   ├── rules/
│   │   ├── 就业规则.md
│   │   ├── 请假制度.md
│   │   └── 交通费报销.md
│   ├── manuals/
│   │   ├── 系统操作手册.md
│   │   └── 新人培训资料.md
│   ├── faq/
│   │   └── 常见问题.md
│   └── project_docs/
│       ├── 要件定義書.md
│       ├── 基本設計書.md
│       └── 詳細設計書.md
```

运行时：

```bash
python3 main.py "交通费怎么报销？" --docs ./data
```

这样程序会读取 `data` 下面所有支持的资料。

---

## 18. 实际项目中路径会不会每次手动输入？

学习阶段可以手动输入：

```bash
--docs ./data
```

但实际项目中，一般不会每次手动写。

通常会放进配置文件。

例如 `.env`：

```env
DOCS_DIR=./data
TOP_K=5
CHUNK_SIZE=1000
CHUNK_OVERLAP=150
```

或者 `config.yaml`：

```yaml
docs_dir: ./data
top_k: 5
chunk_size: 1000
chunk_overlap: 150
```

然后程序启动时自动读取配置。

这样更适合实际会社项目。

---

## 19. 会社资料是否一定是固定路径？

一般来说，实际项目会采用固定路径，但不一定只有一种来源。

常见资料来源包括：

```text
本地固定目录
共享文件夹
Google Drive
SharePoint
GitHub 仓库
Confluence
Notion
数据库
S3 对象存储
社内文件服务器
```

学习阶段建议先用：

```text
本地固定目录 ./data
```

因为最容易理解。

之后再升级到：

```text
Google Drive / SharePoint / S3 / GitHub
```

---

## 20. 推荐的学习目录结构

你现在学习 RAG，可以这样整理：

```text
ai-learn/
├── rag-demo/
│   ├── main.py
│   ├── data/
│   │   ├── company_rule.md
│   │   ├── vacation_rule.md
│   │   ├── traffic_expense.md
│   │   └── faq.md
│   └── README.md
```

然后运行：

```bash
cd ai-learn/rag-demo
python3 main.py "交通费怎么报销？" --docs ./data --mock
```

如果要使用真实模型：

```bash
python3 main.py "交通费怎么报销？" --docs ./data --real
```

---

## 21. 建议你给这个例子追加的学习功能

这个例子适合作为第一步，但建议继续改造：

### 21.1 把 TOP_K 改成命令行参数

当前是固定：

```python
TOP_K = 4
```

可以改成：

```bash
python3 main.py "问题" --docs ./data --top-k 5
```

这样你可以测试不同 Top K 的效果。

---

### 21.2 在 Sources 中显示 chunk 摘要

当前只显示：

```text
rules/traffic.md#chunk1 (score=3)
```

可以改成显示部分内容：

```text
rules/traffic.md#chunk1 (score=3)
交通费报销需要在每月25日之前提交……
```

这样更容易学习检索结果是否正确。

---

### 21.3 支持更多文件类型

可以逐步追加：

```text
PDF
Word
Excel
HTML
CSV
```

不过建议先把 `.md` 和 `.txt` 理解透。

---

### 21.4 替换成向量检索

后续可以升级为：

```text
文本读取
   ↓
chunk 切分
   ↓
embedding
   ↓
FAISS / Chroma
   ↓
similarity search Top K
   ↓
LLM 回答
```

---

## 22. 一句话总结

这个例子中：

```text
--docs 决定从哪里读取资料
iter_text_files() 负责扫描 .md / .txt 文件
read_text() 负责读取文件内容
chunk_text() 负责把长文档切成 chunk
retrieve() 负责根据问题找最相关的 chunk
TOP_K 决定最多取几个 chunk
build_context() 负责把检索结果拼成模型上下文
answer_question() 负责调用模型回答
```

最核心的一句话：

> RAG 的关键不是让模型直接读全部资料，而是先把资料切成 chunk，再从中检索 Top K 个最相关片段，让模型只基于这些片段回答。

---

## 23. 当前 main.py 的流程图

```text
main()
  ↓
parse_args()
  ↓
取得 question / --docs / --model / --mock / --real
  ↓
base_dir = Path(args.docs).resolve()
  ↓
检查目录是否存在
  ↓
build_chunks(base_dir)
  ↓
iter_text_files(base_dir)
  ↓
读取 .md / .txt
  ↓
chunk_text(text)
  ↓
生成 Chunk(source_label, content)
  ↓
retrieve(question, chunks)
  ↓
关键词重合度打分
  ↓
排序后取 TOP_K
  ↓
build_context(top_chunks)
  ↓
answer_question(...)
  ↓
打印 Answer
  ↓
打印 Sources
```

---

## 24. 最适合你的下一步练习

建议你下一步做 3 个小练习：

### 练习 1：准备测试资料

创建目录：

```text
data/
├── traffic_expense.md
├── vacation_rule.md
└── company_faq.md
```

每个文件写一点会社规则。

---

### 练习 2：观察 Sources

运行：

```bash
python3 main.py "交通费什么时候提交？" --docs ./data --mock
```

重点看：

```text
=== Sources ===
```

判断它是否检索到了正确的 chunk。

---

### 练习 3：修改 TOP_K

把：

```python
TOP_K = 4
```

改成：

```python
TOP_K = 2
```

再运行同样的问题，比较 Sources 数量变化。

这样你就能真正理解 Top K 的作用。
