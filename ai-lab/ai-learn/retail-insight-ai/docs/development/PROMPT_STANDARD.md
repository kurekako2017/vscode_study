# Prompt Standard / Prompt 规范 / プロンプト標準

## 1. Purpose / 目的 / 目的

Prompts must be classified, templated, and externalized.
Prompt 必须分类、模板化、外置化。
プロンプトは分類、テンプレート化、外部化される必要があります。

Rule:
Do not hardcode production prompts directly inside workflow logic.
规则：禁止在工作流逻辑中直接硬编码生产 Prompt。
ルール：ワークフローロジックへ本番 Prompt を直接ハードコードしてはいけません。

## 2. Prompt Categories / Prompt 分类 / プロンプト分類

- Analysis
- Research
- Approval
- Report
- Retrieval
- Internal RAG
- LLM Provider Seam
- Evaluation
- Guardrails

## 3. Standard Prompt Shape / 标准结构 / 標準構造

Each prompt definition must declare:

- `role`
- `goal`
- `input`
- `output`
- `variables`
- `constraints`
- `fallback`
- `version`

## 4. Category Rules / 分类规则 / 分類ルール

### 分析（Analysis）

- Role: domain analyst
- Input: structured business facts and relevant research
- Output: grounded analysis points
- Variables: `question`, `mode`, `kpi_summary`, `research_summary`

### 调研（Research）

- Role: evidence collector
- Input: question, scope, source constraints
- Output: source-backed findings
- Variables: `question`, `research_scope`, `allowed_sources`

### 审批（Approval）

- Role: approval assistant
- Input: report draft, approval rules, reviewer notes
- Output: approval summary or revision guidance
- Variables: `report_content`, `approval_status`, `review_comment`

### 报告（Report）

- Role: report writer
- Input: facts, citations, risk notes
- Output: structured markdown report
- Variables: `task_id`, `findings`, `citations`, `risk_notes`

### 检索（Retrieval）

- Role: retrieval orchestrator
- Input: query, data scope, top-k, filters
- Output: ranked context candidates
- Variables: `query`, `retrieval_scope`, `top_k`, `filters`

### Internal RAG

- Role: grounded answer synthesizer
- Input: question, ranked retrieval results, citation policy, answer mode
- Output: answer with citations and confidence notes
- Variables: `question`, `retrieval_results`, `answer_mode`, `require_citations`, `confidence_floor`
- Constraints: every factual claim must be grounded in citations; do not invent unsupported facts; return an insufficiency signal when context is too thin; keep answers schema-bound.
- Fallback: `insufficient_context`

### LLM Provider 接缝

- Role: model-backed answer assembly boundary
- Input: question, retrieval results, citations, answer mode, provider policy, usage limits
- Output: grounded answer draft, citations, usage metadata, confidence notes
- Variables: `question`, `retrieval_results`, `citations`, `answer_mode`, `provider_name`, `model_name`, `max_output_tokens`, `temperature`, `token_budget`, `cost_budget`, `latency_budget`
- Constraints: provider output must be schema-bound; missing or invalid citations must not be passed through; provider errors must not change the frozen retrieval API response; token, cost, and latency accounting placeholders must be documented even when not enforced.
- Fallback: `deterministic_extractive_mode`

### 评估（Evaluation）

- Role: evaluator
- Input: expected answer, actual answer, sources
- Output: scored evaluation
- Variables: `expected`, `actual`, `sources`, `criteria`

### 护栏（Guardrails）

- Role: safety and policy checker
- Input: draft action or response
- Output: allow, block, or revise
- Variables: `candidate_output`, `policy_rules`, `risk_level`

## 5. Storage Rules / 存储规则 / 保存ルール

- Prompts must live in prompt registries, config files, or dedicated prompt modules.
- Version each prompt family.
- Business rules belong in contracts or code, not only inside prompts.

## 6. Variable Rules / 变量规则 / 変数ルール

- Variables must be named, typed, and documented.
- Missing variables must fail fast.
- Variables that carry confidential data must be minimized and redacted from logs.

## 7. Output Rules / 输出规则 / 出力ルール

- Prompt outputs must map to a schema or typed contract when used by workflow logic.
- Free-form prose is acceptable only at user-facing report edges.
- Prompt output must not be the only source of state transitions.

## 8. Trilingual Key Terms / 三语术语 / 三言語用語

| English | 中文（简体） | 日本語 |
|---|---|---|
| Prompt | 提示词 | プロンプト |
| Variables | 变量 | 変数 |
| Guardrails | 护栏规则 | ガードレール |
| Evaluation | 评估 | 評価 |
| Grounded Output | 有依据输出 | 根拠付き出力 |
| Version | 版本 | バージョン |

## 9. Text Flow / 纯文本流程 / テキストフロー

```text
Prompt category selected
│
▼
Load prompt template and version
│
▼
Bind variables
├── missing variable -> fail fast
└── complete
    │
    ▼
    Execute model or provider
    │
    ▼
    Validate output schema
    ├── invalid -> fallback / retry / error
    └── valid -> workflow / report / approval step
```

## 10. Review Checklist / 审查清单 / レビューチェックリスト

1. Is the prompt category declared?
2. Is the prompt version declared?
3. Are variables documented?
4. Is output typed or schema-bound?
5. Is hardcoded prompt logic avoided?
