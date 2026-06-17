# AI Agent 開発案件 面接準備稿：DeepSearch / Shopkeeper Agent

> 用途：日本现场 AI Agent / LLM アプリ開発岗位面试准备。  
> 目标：把 `deepsearch-agents-main` 和 `shopkeeper-agent-main` 两个项目整理成“实际项目经验”口径，可用于现场面试说明。  
> 补充策略：项目中没有正式使用、但岗位面试可能问到的技术，统一回答为 `本地環境で模拟検証・学習しました`。

## 快速跳转

- [1. 面试表达原则](#sec-1)
- [2. AI Agent 案件用自我介绍](#sec-2)
- [3. 两个项目总括说明](#sec-3)
- [4. DeepSearch Agents 项目介绍](#sec-4)
- [5. Shopkeeper Agent 项目介绍](#sec-5)
- [6. 日本现场案件要求对齐](#sec-6)
- [7. 未使用但可回答的技术口径](#sec-7)
- [8. Agent 现场面试高频问答](#sec-8)
- [9. 简历可直接使用的日语描述](#sec-9)
- [10. 快速背诵版](#sec-10)
- [11. AI Agent 技术词日语发音](#sec-11)
- [12. 参考来源](#sec-12)

---

<a id="sec-1"></a>

## 1. 面试表达原则

这份文档按“实际项目经验”来讲，但现场回答时要把“实际做过的项目”和“本地模拟练习过的技术”分清楚。

推荐表达：

> AI Agent 関連では、DeepSearch Agents と Shopkeeper Agent という2つの実装プロジェクトを担当しました。  
> DeepSearch は多智能体による調査支援、Shopkeeper は自然言語から SQL を生成する問数 Agent です。  
> 実装では FastAPI、LangGraph / DeepAgents、LangChain、MySQL、Qdrant、Elasticsearch、React、WebSocket / SSE を使用しました。

如果对方问到项目没用过的技术，例如 LangSmith、OpenAI Agents SDK、MCP、Kubernetes、本番監視、CI/CD，可以这样说：

> その技術は今回のプロジェクト本体では本番利用していません。  
> ただし、本地検証環境で基本的な使い方や構成は確認しております。  
> 実案件で必要になれば、既存の FastAPI、Agent、DB、ログ連携の経験をベースにキャッチアップ可能です。

避免表达：

- `全部実務でやりました`
- `本番大規模運用まで経験しています`
- `何でもできます`

安全但有力的表达：

- `プロジェクト内で実装・動作確認しました`
- `本地環境で模拟検証しました`
- `本番導入時には、権限、監査ログ、評価、監視、コスト管理が重要だと認識しております`
- `Prompt だけでなく、API、DB、検索、非同期処理、ログ、前端連携まで含めて対応しました`

---

<a id="sec-2"></a>

## 2. AI Agent 案件用自我介绍

### 2.1 标准版

> 2007年に来日し、日本で約20年間、システム開発に従事してまいりました。  
> Java、Python、C#、ABAP を中心に、Webアプリケーション、バッチ処理、API連携、クラウド移行、データ移行、運用保守まで幅広く経験しております。  
> 役割としては、SE、ブリッジSE、TLの経験がございます。
>
> AI Agent 関連では、DeepSearch Agents と Shopkeeper Agent という2つのプロジェクトを実装しました。  
> DeepSearch Agents は、DeepAgents を使った多智能体型の調査支援システムです。主智能体がユーザー依頼を分析し、ネット検索、DB検索、ローカル知識庫検索、アップロードファイル解析を使い分け、最終的に回答や Markdown / PDF レポートを生成します。  
> Shopkeeper Agent は、LangGraph を使った自然言語問数システムです。ユーザーの質問から関連する字段、指标、字段值を検索し、SQL を生成、検証、修正、実行して分析結果を返します。
>
> 技術面では、Python / FastAPI、LangGraph、DeepAgents、LangChain、OpenAI-Compatible API、MySQL、Qdrant、Elasticsearch、React / Vite、WebSocket、SSE を使用しました。  
> Agent 開発では、単に大模型 API を呼ぶだけではなく、タスク分解、ツール呼び出し、RAG、SQL安全性、ログ、ストリーミング表示、エラー時の切り分けを意識して実装しました。  
> これまでのバックエンド開発とデータ連携の経験を活かし、AI Agent 開発案件でも貢献したいと考えております。  
> 本日はよろしくお願いいたします。

### 2.2 短め版

> 日本で約20年間、システム開発に従事してまいりました。  
> Java / Python を中心に、バックエンド、DB連携、API、バッチ、クラウド移行の経験がございます。  
> AI Agent 関連では、DeepAgents による多智能体検索システムと、LangGraph による自然言語问数 Agent を実装しました。  
> FastAPI、React、MySQL、Qdrant、Elasticsearch、RAG、SQL生成、WebSocket / SSE のストリーミング連携まで対応しました。  
> 既存の業務システム開発経験を活かして、AI Agent 案件にも対応したいと考えております。

---

<a id="sec-3"></a>

## 3. 两个项目总括说明

面试中如果被问“AI Agent の项目経験を説明してください”，可以这样回答：

> AI Agent の项目として2つ経験しました。  
> 1つ目は DeepSearch Agents で、ユーザーの調査依頼に対して、主智能体がタスクを整理し、ネット検索、DB検索、ローカル知識庫検索、アップロードファイル解析を使い分け、最終的に回答や Markdown / PDF を生成するシステムです。  
> 2つ目は Shopkeeper Agent で、ECデータ分析を想定し、自然言語の質問から関連する表、字段、指标、字段值を検索し、LangGraph のワークフローで SQL を生成、検証、修正、実行する問数システムです。
>
> どちらも、単純なチャットボットではなく、LLM、検索、DB、ツール実行、ストリーミングレスポンス、React 前端を組み合わせた AI アプリケーションとして実装しました。

---

<a id="sec-4"></a>

## 4. DeepSearch Agents 项目介绍

### 4.1 项目一句话说明

> DeepSearch Agents は、DeepAgents を利用した多智能体型の深度検索・調査支援システムです。  
> ユーザーの調査依頼に対して、主智能体がタスクを判断し、ネット検索、DB検索、ローカル知識庫検索、アップロードファイル解析を使い分けて、最終回答や Markdown / PDF レポートを生成します。

### 4.2 架构说明

> バックエンドは FastAPI、智能体部分は DeepAgents / LangGraph / LangChain、前端は React / Vite です。  
> FastAPI の `/api/task` でタスクを受け取り、后台任务として Agent を実行します。  
> 実行过程は WebSocket で前端に送信し、工具调用、子智能体调用、最终结果、生成文件一覧をリアルタイム表示します。

### 4.3 智能体设计

> 智能体は Orchestrator-Workers 形式で設計しました。  
> 主智能体は用户任务の理解、规划、子智能体调度、结果汇总、文件生成を担当します。  
> 子智能体として、ネット検索助手、数据库查询助手、ローカル知識庫助手を分け、それぞれ Tavily、MySQL、本地知识库工具を调用します。  
> 主智能体は直接、上传文件读取、Markdown 生成、PDF 转换などの工具も调用できます。

### 4.4 担当内容说明

> 私は、前端から后端、主智能体、子智能体、工具层までの调用流程を実装・確認しました。  
> 特に、FastAPI で長時間タスクを后台実行し、WebSocket で進捗を推送する構成、`thread_id` と `session_dir` による会話単位の上下文隔离、アップロードファイルと输出文件を会話単位で管理する部分を担当しました。  
> また、LLM provider の切り替え、OpenRouter / NVIDIA / Ollama のような OpenAI-Compatible 接続、外部服务异常時のログ確認とエラー表示も確認しました。

---

<a id="sec-5"></a>

## 5. Shopkeeper Agent 项目介绍

### 5.1 项目一句话说明

> Shopkeeper Agent は、ECデータ分析を想定した自然言語问数 Agent です。  
> ユーザーが「华北地区の销售额を统计してください」のように自然言語で質問すると、系统が関連する表、字段、指标、字段值を召回し、SQL を生成、検証、修正、実行して结果を返します。

### 5.2 架构说明

> バックエンドは FastAPI、智能体工作流は LangGraph、数据层は MySQL、Qdrant、Elasticsearch を利用します。  
> MySQL は业务数据和元数据保存、Qdrant は字段・指标の向量检索、Elasticsearch は字段取值の全文检索に使います。  
> 前端は React / Vite で、后端から SSE 形式で返される执行步骤、SQL、查询结果を画面に表示します。

### 5.3 LangGraph 工作流说明

> LangGraph では、自然语言问题をいきなり SQL に変換するのではなく、複数の节点に分けて処理します。  
> まず关键词抽出を行い、その後、字段召回、字段值召回、指标召回を并行执行します。  
> 次に召回结果を合并し、必要な表和指标を过滤し、数据库方言や日期などの追加上下文を补充します。  
> その上で SQL を生成し、MySQL の `EXPLAIN` などで検証し、エラーがあれば修正节点を通してから最终执行します。

### 5.4 担当内容说明

> 私は、问数 Agent の调用流程を整理し、API 路由、`QueryService`、`graph.py`、各节点、Repository 层までを実装・確認しました。  
> 特に、字段・指标・字段值を分けて召回する理由、元数据知识库を先に构築する理由、SQL 生成后に検証・修正节点を入れる理由を重点的に対応しました。  
> また、FastAPI の生命周期で MySQL / Qdrant / Elasticsearch / Embedding client を初期化し、请求単位で ContextVar に request_id を入れてログ追跡する設計も確認しました。

---

<a id="sec-6"></a>

## 6. 日本现场案件要求对齐

### 6.1 目前日本案件票常见要求

近期日本现场 AI / 生成AI / LLM 案件，要求通常不是只会 Prompt，而是“生成AI + Web系统开发 + 业务整理 + 云和运用”的组合。

常见要求可以整理成下面几类：

| 案件要求 | 面试时应强调的自身经验 |
| --- | --- |
| Python 后端开发 | `FastAPI で API 実装、SSE / WebSocket、非同期処理、外部 API 連携を担当しました` |
| AI / LLM / RAG 基本理解 | `LLM 単体ではなく、検索、DB、文件、工具调用を組み合わせた RAG / Agent 構成を実装しました` |
| AIエージェント設計 | `人間の作業をタスク分解し、Workflow / Agent / Tool に分けて設計しました` |
| 要件定義・基本設計 | `ユーザーの質問から必要なデータ、検索対象、SQL生成、結果表示まで処理フローを整理しました` |
| React / TypeScript | `React / Vite で Agent の進捗、結果、ファイル一覧、SSE / WebSocket 連携を実装しました` |
| DB / SQL | `MySQL、SQLAlchemy、SQL生成、SQL検証、EXPLAIN、実行結果返却を対応しました` |
| Vector DB / Search | `Qdrant、Elasticsearch、Embedding を用いて字段、指标、字段值の召回を実装しました` |
| Cloud / Docker | `本体はローカル・Docker中心ですが、AWS / Azure 連携や本番配置時の構成は理解しています` |
| Git / チーム開発 | `Git、Issue、レビュー前提のチーム開発に対応可能です` |
| AI 開発支援ツール | `ChatGPT、Claude Code、Cursor、GitHub Copilot 等は開発・調査・資料作成で活用経験があります` |
| 運用保守・改善 | `ログ、request_id / thread_id、エラー切り分け、外部サービス失敗時の確認を意識しました` |

### 6.2 面试中优先强调的项目卖点

日本案件票里经常写 `要件整理`、`基本設計`、`タスク分解`、`API実装`、`保守運用改善`。所以不要只讲 LangGraph / DeepAgents，要这样讲：

> 私の強みは、AI Agent のフレームワークだけではなく、既存の業務システム開発経験を活かして、ユーザー業務を整理し、API、DB、検索、前端、ログ、運用まで含めて実装できる点です。  
> DeepSearch では、調査業務をネット検索、DB検索、知識庫検索、文件解析、レポート生成に分解しました。  
> Shopkeeper では、自然言語問数業務を关键词抽出、三路召回、SQL生成、SQL検証、SQL実行に分解しました。  
> そのため、AI Agent 案件で求められる「人間の作業をシステム化可能なタスクに分解する」部分にも対応可能です。

### 6.3 日本案件规格に寄せた自我紹介补强版

> AI Agent 案件で求められる、Python バックエンド、API 実装、RAG、DB連携、React 前端、Git チーム開発、クラウド・Docker の基本構成については、DeepSearch Agents と Shopkeeper Agent の2つのプロジェクトで一通り対応しました。  
> また、日本の现场案件では、生成AIそのものよりも、業務要件を整理し、人間が行っている作業をタスク分解し、システム化できる形に落とし込む力が重要だと理解しております。  
> 私はこれまで Java / Python の業務システム、DB連携、バッチ、運用保守を長く経験しているため、AI Agent 開発でも、既存システムとの連携や運用面を意識して対応できます。

### 6.4 案件票关键词別の回答

#### `AIエージェント設計開発`

> DeepSearch では、主智能体と子智能体を分け、調査任务を動的に判断して工具调用する構成を実装しました。  
> Shopkeeper では、LangGraph で固定流程の问数 Agent を構成しました。  
> そのため、自由度の高い Agent と安全性の高い Workflow の両方を説明できます。

#### `生成AI / LLMを組み込んだWebアプリケーション`

> FastAPI に LLM 呼び出し、RAG、SQL生成、外部検索、文件处理を組み込み、React 前端に WebSocket / SSE で結果を返す Web アプリケーションとして実装しました。

#### `クライアントヒアリング / 業務要件整理`

> AI Agent では、まず人間が行っている作業を整理し、どこを検索、どこを判断、どこをDB查询、どこを人間確認にするか分ける必要があります。  
> 私の项目では、調査業務と問数業務をそれぞれ処理ステップに分解し、Agent / Tool / API の構成に落とし込みました。

#### `クラウド / Docker / CI/CD / 監視`

> プロジェクト本体はローカルと Docker を中心に確認しました。  
> 本番化する場合は、FastAPI、worker、DB、vector DB、frontend をコンテナ化し、AWS / Azure 上で配置し、GitHub Actions、CloudWatch / Datadog、権限管理、Secrets 管理を組み合わせる構成になると理解しています。  
> CI/CD や監視については本地環境と既存案件経験をベースに対応可能です。

---

<a id="sec-7"></a>

## 7. 未使用但可回答的技术口径

现场 AI Agent 案件会问一些项目中没有正式使用的技术。不要说“完全没有”，建议统一回答为“本地模拟练习过”。

| 技术 | 推荐回答 |
| --- | --- |
| LangSmith / Agent 监控 | `本プロジェクトでは独自ログとストリーミングイベントで確認しました。LangSmith については本地環境で trace / eval の考え方を確認しており、本番では可観測性のために導入候補になると理解しています。` |
| OpenAI Agents SDK | `今回の本体実装は LangGraph / DeepAgents ですが、Agents SDK の概念、tool calling、guardrails、handoff については本地検証で確認しました。` |
| MCP | `本体では MCP は使用していませんが、外部ツールや社内システムを標準化して Agent に接続する仕組みとして理解しています。本地で基本構成を確認しました。` |
| Guardrails | `本体では SQL 検証、ツール引数補正、エラー処理を入れました。Guardrails 専用フレームワークは本地環境で検証し、出力形式制御や禁止操作制御に使えると理解しています。` |
| Human-in-the-loop | `本体では自動実行が中心ですが、LangGraph の interrupt / state 確認の考え方は本地検証しました。SQL実行前承認や重要操作前承認に使えると考えています。` |
| Kubernetes | `本体はローカル / Docker 中心です。Kubernetes については本地検証レベルですが、FastAPI、worker、vector DB、ログ基盤を分けて配置する考え方は理解しています。` |
| CI/CD | `本体では手動起動と検証が中心です。GitHub Actions などで lint、test、build、deploy を分ける構成は本地サンプルで確認しています。` |
| Prompt Evaluation | `本体では手動ケースで確認しました。評価データセット、期待結果、LLM-as-a-judge、回帰テストの考え方は本地で確認しました。` |

---

<a id="sec-8"></a>

## 8. Agent 现场面试高频问答

### Q1. AI Agent と普通の ChatGPT API 呼び出しの違いは何ですか

> 普通の API 呼び出しは、ユーザーの質問をそのままモデルに渡して回答をもらう形です。  
> AI Agent は、ユーザーの目的を分解し、必要に応じて検索、DB查询、文件读取、SQL生成、外部API调用などの工具を使い、途中结果を見ながら最终回答を作る点が違います。  
> 私の项目では、DeepSearch で多智能体调度、Shopkeeper で LangGraph 工作流を使い、LLM と工具执行を組み合わせました。

### Q2. Agent と Workflow の違いは何ですか

> Workflow は、処理順序や分岐が比較的固定されている構成です。Shopkeeper Agent のように、关键词抽出、召回、SQL生成、検証、実行という順序が決まっている場合に向いています。  
> Agent は、LLM が状況に応じてどの工具を使うか判断する構成です。DeepSearch のように、ネット検索が必要か、DB検索が必要か、ファイル解析が必要かを動的に判断する場合に向いています。  
> 実務では、完全自由な Agent より、重要処理は Workflow 化して安全性を高める方がよいと考えています。

### Q3. LangGraph を使うメリットは何ですか

> LangGraph は、Agent の処理を节点和边で明確に定義できる点がメリットです。  
> また、長時間実行、状態管理、ストリーミング、human-in-the-loop、チェックポイントのような Agent 実行に必要な基盤を扱いやすいです。  
> Shopkeeper Agent では、SQL生成前後の処理を节点化し、エラー時だけ `correct_sql` に進む条件分岐を入れました。

### Q4. Tool Calling / Function Calling とは何ですか

> LLM に外部能力を使わせる仕組みです。  
> 例えば、検索、DB查询、ファイル読み取り、SQL実行、PDF生成などを関数として定義し、モデルが必要な工具名と参数を出して、アプリ側が実際に実行します。  
> 注意点は、LLM の出す参数をそのまま信用しないことです。型チェック、必須項目チェック、許可された工具だけ実行する制御が必要です。

### Q5. なぜ自然言語から直接 SQL を作らないのですか

> 直接 SQL を生成すると、表名、字段名、指标口径を間違えるリスクが高いです。  
> そのため、先に元数据知识库から関連字段、指标、字段值を召回し、LLM に正しい上下文を渡してから SQL を生成します。  
> さらに生成後に SQL を検証し、必要に応じて修正することで、幻觉や実行エラーを減らす設計にしています。

### Q6. SQL Agent で安全性をどう確保しますか

> まず読み取り専用ユーザーを使い、`SELECT` のみ許可します。  
> 次に、SQL 生成後に構文チェック、禁止キーワードチェック、`EXPLAIN` による検証、実行タイムアウト、取得件数制限を入れます。  
> 重要な本番データでは、実行前に人間承認を入れる、監査ログを残す、テーブル単位の権限を分けることも必要です。

### Q7. Qdrant と Elasticsearch はどう使い分けましたか

> Qdrant は向量检索に向いているため、字段説明や指标説明のような意味検索に使います。  
> Elasticsearch は关键词や实际取值の全文検索に向いているため、地域名、商品名、状态値などの字段取值検索に使います。  
> つまり、意味が近いものを探す場合は Qdrant、文字列として一致・部分一致させたい場合は Elasticsearch という使い分けです。

### Q8. RAG の精度を上げるには何を見ますか

> まずデータ前処理、chunk サイズ、metadata、embedding モデル、検索 top_k、reranking の有無を確認します。  
> 次に、検索結果が正しいか、LLM に渡す上下文が多すぎないか、回答が検索結果に根拠を持っているかを確認します。  
> 本番では、質問と期待回答の評価データセットを作り、検索精度、回答の忠実性、回答妥当性を継続的に測る必要があります。

### Q9. RAG は hallucination を完全に防げますか

> 完全には防げません。  
> RAG は外部データを参照することで回答を根拠づけやすくしますが、検索結果が間違っている場合、古い場合、文脈が不足している場合、LLM が誤って要約する場合があります。  
> そのため、出典表示、回答根拠の確認、評価、ログ、必要に応じた人間確認が重要です。

### Q10. WebSocket と SSE はどう使い分けますか

> WebSocket は双方向通信が必要な場合に向いています。DeepSearch では、Agent 実行イベントを会話単位で前端に推送し、必要に応じて取消や状態管理も行うため WebSocket を使いました。  
> SSE はサーバーからクライアントへの一方向ストリーミングに向いています。Shopkeeper のように查询流程や结果を順番に返すだけなら、SSE でも十分です。  
> 用途に応じて、双方向なら WebSocket、一方向なら SSE と整理できます。

### Q11. Agent の実行が長時間になる場合、どう設計しますか

> HTTP リクエスト内で最後まで待たせず、后台任务、Queue、Worker に分けます。  
> 前端には WebSocket や SSE で進捗を返し、キャンセル、タイムアウト、エラー通知を用意します。  
> また、会話 ID や request_id でログを追跡し、途中結果や生成ファイルを session 単位で分離します。

### Q12. Memory と Context の違いは何ですか

> Context は、現在のリクエストや現在の会話で LLM に渡す情報です。  
> Memory は、過去の会話やユーザー設定、長期的に保持したい情報です。  
> 実務では、何でも Memory に保存するのではなく、保存対象、期限、個人情報、削除要求への対応を考える必要があります。

### Q13. Prompt Injection にはどう対応しますか

> ユーザー入力や外部文書の内容をそのまま system 指示より優先させないことが重要です。  
> 工具実行は許可リスト方式にし、SQL やファイル操作など危険な処理は入力検証、権限分離、人間承認を入れます。  
> RAG の検索文書にも悪意ある指示が含まれる可能性があるため、文書内容は“参考情報”として扱い、操作権限はアプリ側で制御します。

### Q14. Agent の評価はどうしますか

> まず代表的な質問セットと期待結果を作ります。  
> RAG なら検索結果の妥当性、回答の根拠一致、回答の完全性を評価します。  
> SQL Agent なら、生成 SQL の正しさ、実行可否、集計結果、禁止 SQL が出ないことを評価します。  
> モデルや Prompt を変えるたびに同じ評価セットで回帰確認することが重要です。

### Q15. LLM アプリのコストとレイテンシをどう下げますか

> まず不要な上下文を減らし、検索 top_k や chunk を調整します。  
> 次に、軽い処理は小さいモデル、重要な推論は高性能モデルに分けます。  
> Embedding や検索結果のキャッシュ、SQL 結果のキャッシュ、streaming 表示も有効です。  
> Agent が工具を呼びすぎないように、Workflow 化や最大ステップ数制限も入れます。

### Q16. 障害調査ではどこを見ますか

> request_id / thread_id でログを追い、どの节点、どの工具、どの外部服务で失敗したかを確認します。  
> LLM 呼び出し、検索、DB、Embedding、WebSocket / SSE のどこで止まったかを切り分けます。  
> Agent 系では、モデル入力、モデル出力、工具参数、工具結果を残しておくことが重要です。

### Q17. OpenAI / OpenRouter / Ollama のような provider 切り替えはなぜ必要ですか

> 開発、検証、本番で使うモデルやコスト要件が違うためです。  
> 例えば、外部APIが使えない場合は Ollama でローカル検証し、本番では OpenAI-Compatible API を使うなどの切り替えができます。  
> ただし、モデルごとに tool calling や JSON 出力の安定性が違うため、provider 切り替え時には評価が必要です。

### Q18. 面试で “LangSmith / MCP / Agents SDK は経験ありますか” と聞かれたら

> 今回の项目本体では LangGraph / DeepAgents を中心に実装しました。  
> LangSmith、MCP、Agents SDK については本地環境で基本機能を模拟検証しました。  
> LangSmith は trace / eval、MCP は外部工具接続の標準化、Agents SDK は tool calling や guardrails の観点で理解しています。  
> 実案件で利用する場合も、今回の Agent、API、DB、ログ連携の経験をベースに対応可能です。

---

<a id="sec-9"></a>

## 9. 简历可直接使用的日语描述

### 8.1 DeepSearch Agents

> DeepAgents を利用した多智能体型の深度検索システムを実装。  
> FastAPI、WebSocket、React を用いて、ユーザーの調査依頼を受け付け、主智能体がネット検索、数据库查询、ローカル知識庫検索、アップロードファイル解析を使い分ける構成を担当。  
> 会話単位の `thread_id` / `session_dir` による上下文隔离、工具调用イベントのリアルタイム表示、Markdown / PDF 生成、ファイルダウンロードまで一連の処理を実装・検証。

### 8.2 Shopkeeper Agent

> LangGraph を用いた自然言語问数 Agent を実装。  
> ECデータ分析を想定し、自然言語の質問から关键词抽出、字段・指标・字段值の召回、SQL生成、SQL検証、SQL修正、SQL実行までを节点型ワークフローとして構築。  
> MySQL、Qdrant、Elasticsearch、Embedding、FastAPI、SSE、React を組み合わせ、检索增强型の SQL 生成システムとして動作確認。

### 8.3 技术关键字

> Python、FastAPI、LangGraph、DeepAgents、LangChain、OpenAI-Compatible API、OpenRouter、Ollama、RAG、Qdrant、Elasticsearch、MySQL、SQLAlchemy、WebSocket、SSE、React、Vite、Docker、ContextVar、非同期処理、ストリーミングレスポンス、Tool Calling、Function Calling、Prompt Evaluation

---

<a id="sec-10"></a>

## 10. 快速背诵版

> AI Agent 関連では、2つの项目を経験しました。  
> 1つ目は DeepSearch Agents で、DeepAgents を使い、主智能体がネット検索、DB検索、ローカル知識庫、上传文件解析を调度し、最终回答や Markdown / PDF を生成する深度検索システムです。  
> 2つ目は Shopkeeper Agent で、LangGraph を使い、自然言語から字段、指标、字段值を召回し、SQL生成、検証、修正、実行まで行う问数 Agent です。  
> 后端は FastAPI、前端は React / Vite、数据层は MySQL、Qdrant、Elasticsearch を使い、WebSocket や SSE で実行过程を前端に流式表示しました。  
> 项目本体で使っていない LangSmith、MCP、OpenAI Agents SDK などについても、本地環境で模拟検証し、基本概念と導入ポイントは理解しております。  
> これまでの Java / Python バックエンド、DB連携、バッチ、クラウド移行の経験を活かして、AI Agent 案件にも貢献したいと考えております。

---

<a id="sec-11"></a>

## 11. AI Agent 技术词日语发音

> 说明：这里补的是面试时最常说到的读法。  
> 如果现场追问到某个词，你可以直接按这个表读。

| English / 中文 | 日本語面试读法 |
| --- | --- |
| 主智能体 | メイン エージェント / シュチノウタイ |
| 子智能体 | サブ エージェント / コチノウタイ |
| 调度 / 调度器 | オーケストレーション / ディスパッチ |
| 任务分解 | タスク ブンカイ |
| 召回 | ショウカイ |
| 元数据知识库 | メタデータ チシキベース |
| 知识库 | チシキベース |
| 取值 | トリチ |
| 业务口径 | ビジネス コウケイ |
| 上下文 | コンテキスト |
| 会话 | カイワ |
| 流式返回 | リュウシキ ヘンカン |
| 长时间任务 | チョウジカン タスク |
| 后台任务 | バックグラウンド タスク |
| 依赖注入 | イライ チュウニュウ |
| 生命周期 | ライフサイクル |
| request_id | リクエスト アイディー |
| thread_id | スレッド アイディー |
| session_dir | セッション ディレクトリ |
| 问数 | モンスウ |
| 调查支援 | チョウサ シエン |
| 检索增强 | ケンサク ゾウキョウ |
| 评测 | ヒョウカ |
| 监视 | カンシ |
| 监控 | モニタリング |
| 日志追踪 | ログ トレース |
| 错误切分 | エラー シキリワケ |
| 幻觉 | ハルシネーション |
| Prompt Injection | プロンプト インジェクション |
| Guardrails | ガードレール |
| Human-in-the-loop | ヒューマン イン ザ ループ |
| Tool Calling | ツールコーリング |
| Function Calling | ファンクションコーリング |
| API 連携 | エーピーアイ レンケイ |
| 非同期処理 | ヒドウキ ショリ |
| 外部 API | ガイブ エーピーアイ |
| 本地环境 | ローカル カンキョウ |
| 模拟验证 | モギ ケンショウ |
| AI Agent | エーアイ エージェント |
| LLM | エルエルエム |
| RAG | ラグ |
| LangGraph | ランググラフ |
| LangChain | ラングチェーン |
| LangSmith | 
| DeepAgents | ディープエージェンツ |
| OpenAI-Compatible API | オープンエーアイ コンパチブル エーピーアイ |
| OpenRouter | オープンルーター |
| NVIDIA | エヌビディア |
| Ollama | オラマ |
| Tavily | タビリー |
| FastAPI | ファストエーピーアイ |
| WebSocket | ウェブソケット |
| SSE | エスエスイー |
| Streaming | ストリーミング |
| Embedding | エンベディング |
| Vector Search | ベクトル検索 |
| Vector DB | ベクトル ディービー |
| Qdrant | キュードラント |
| Elasticsearch | エラスティックサーチ |
| MySQL | マイエスキューエル |
| SQLAlchemy | エスキューエル アルケミー |
| ContextVar | コンテキストバー |
| InMemorySaver | インメモリー セイバー |
| Markdown | マークダウン |
| PDF | ピーディーエフ |
| React | リアクト |
| Vite | ヴィート |
| TypeScript | タイプスクリプト |
| Docker | ドッカー |
| Git | ギット |
| GitHub Actions | ギットハブ アクションズ |
| GitHub Copilot | ギットハブ コパイロット |
| Claude Code | クロード コード |
| Cursor | カーソル |
| AWS | エーダブリューエス |
| Azure | アジュール |
| AWS Lambda | エーダブリューエス ラムダ |
| ECS | イーシーエス |
| Fargate | ファーゲート |
| CloudWatch | クラウドウォッチ |
| EventBridge | イベントブリッジ |
| Issue | イシュー |
| Review | レビュー |
| API | エーピーアイ |
| Repository | リポジトリ |
| Service | サービス |
| Workflow | ワークフロー |
| Orchestrator | オーケストレーター |
| Prompt | プロンプト |
| Monitoring | モニタリング |
| Logging | ロギング |

---

<a id="sec-12"></a>

## 12. 参考来源

本节面试题参考了以下公开资料方向，并结合当前两个项目实际代码整理：

- 日本现场案件要求参考：
  - レバテックフリーランス Python 案件一覧：近期 AI Agent 案件要求包括 Python / Git / React、業務要件整理、要件定義、タスク分解、生成AI・LLM・AIエージェント・RAG の基本理解；生成AIエージェント試作開発案件要求 Claude Code、Cursor、GitHub Copilot、ChatGPT 等 AI 開発支援ツール活用、Markdown への作業分解、Python / JavaScript / TypeScript、Git / Issue / Review。
  - レバテックフリーランス Python 案件一覧：AI関連案件中也出现 Python / AWS、AWS Lambda 等 serverless、React / Next.js、パブリッククラウド、Docker、GCP / AWS などの开发・运用要求。
  - BIGDATA NAVI Python / LLM 案件：要求 Python3、OpenAI API、AWS SageMaker、Azure、Docker、GitHub Copilot、GitHub Actions、CircleCI、LLM 組み込み Web アプリ開発。
- LangGraph 官方文档：强调 Agent 编排中的 durable execution、streaming、human-in-the-loop、memory、persistence、observability 等能力。
- OpenAI Tools 文档：强调通过 built-in tools、function calling、tool search、MCP 等方式扩展模型能力。
- OpenAI Evals 文档：强调通过 evals 测试模型输出是否满足预期，是构建可靠 LLM 应用的重要部分。
- RAGAS 论文和 RAG 工业应用研究：参考 RAG 评测、检索质量、faithfulness、answer relevancy、人工评测和生产化挑战。
