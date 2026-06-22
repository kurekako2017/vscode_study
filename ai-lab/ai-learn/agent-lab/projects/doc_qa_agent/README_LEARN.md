# doc_qa_agent 学习导读

本文件只保留学习顺序和阅读重点，避免和主文档重复。完整说明请先看 [README.md](/home/victorkure/workspace/vscode_study/ai-lab/ai-learn/agent-lab/projects/doc_qa_agent/README.md)。

所有执行命令都默认在 `ai-lab/` 根目录运行。
`--docs` 需要传入 `doc_qa_agent` 项目的目录，而不是 `ai-lab/` 根目录。

## 1. 推荐阅读顺序

1. 先看 `README.md` 里的“chunk 是什么，chunk 前后分别是什么”
2. 再看 `main.py` 的 `chunk_text()`、`build_chunks()`、`retrieve()`、`build_context()`、`answer_question()`
3. 最后看 `[简单测试用例表.md](/home/victorkure/workspace/vscode_study/ai-lab/ai-learn/agent-lab/projects/doc_qa_agent/简单测试用例表.md)`，把 chunk 规则和输出结果对应起来

## 2. 这个项目里 chunk 的关键点

- chunk 前是原始文件内容
- chunk 方式是按字符切片，不是按段落，也不是按 token
- 默认参数是 `CHUNK_SIZE = 1200`、`CHUNK_OVERLAP = 200`
- chunk 后会得到 `list[str]`，再包装成 `Chunk` 对象
- 每个片段的来源格式是 `相对路径#chunkN`

## 3. 命令写法

- Mock 执行：

```bash
python3 ai-learn/agent-lab/projects/doc_qa_agent/main.py --mock --docs ai-learn/agent-lab/projects/doc_qa_agent "项目简介是什么"
```

- 真实模型执行：

```bash
python3 ai-learn/agent-lab/projects/doc_qa_agent/main.py --real --docs ai-learn/agent-lab/projects/doc_qa_agent "项目简介是什么"
```

- 真实模式回退顺序：`OpenRouter -> NVIDIA -> Ollama(qwen2.5-coder:1.5b) -> mock`

## 4. 学习建议

- 先用小文档验证 `CHUNK_SIZE` 和 `CHUNK_OVERLAP`
- 再看 `TOP_K = 4` 对最终 `Sources` 的影响
- 如果要做扩展练习，优先把 `TOP_K` 参数化，再考虑向量检索

## 5. 这份导读不重复的内容

- 不重复介绍业务场景
- 不重复展开流程图
- 不重复解释安装和运行命令
- 不重复列完整设计说明
