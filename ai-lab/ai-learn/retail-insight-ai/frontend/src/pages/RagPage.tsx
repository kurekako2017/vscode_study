import { FormEvent, useState } from "react";

import { ApiClientError, answerInternalRag, executeAIAnalysis, generateExecutiveReport, searchDocumentRetrieval } from "../api";
import { BusinessLearningPanel } from "../components/BusinessLearningPanel";
import { PageHeader } from "../components/PageHeader";
import { StatusBadge } from "../components/StatusBadge";
import { StatusBanner } from "../components/StatusBanner";
import type {
  DisplayError,
  AIAnalysisResponse,
  ExecutiveReportResponse,
  DocumentRetrievalSearchResponse,
  InternalRagAnswerMode,
  InternalRagAnswerResponse,
} from "../types";
import type { RecordLearningEvent } from "../learning/learningTypes";

/**
 * RagPage 负责 deterministic Retrieval + Internal RAG 两个真实后端能力。
 *
 * 当前实现边界：
 * - 只接 keyword retrieval / deterministic internal RAG。
 * - 不接真实 LLM、embedding、pgvector 或 hybrid retrieval。
 */
interface RagPageProps {
  onLearningEvent?: RecordLearningEvent;
  canRetrieve?: boolean;
  canAnalyze?: boolean;
}

/** 成功応答の provider 名から開発 Stub / OpenRouter を表示する（Key や内部設定は出さない）。 */
function providerModeLabel(provider: string): string {
  if (provider.startsWith("stub")) {
    return "Development Stub";
  }
  if (provider.startsWith("openrouter")) {
    return "OpenRouter";
  }
  return "Server Provider";
}

export function RagPage({
  onLearningEvent,
  canRetrieve = true,
  canAnalyze = true,
}: RagPageProps = {}) {
  const [retrievalQuery, setRetrievalQuery] = useState("");
  const [retrievalLimit, setRetrievalLimit] = useState("10");
  const [retrievalDocumentType, setRetrievalDocumentType] = useState("");
  const [retrievalLanguage, setRetrievalLanguage] = useState("");
  const [retrievalTags, setRetrievalTags] = useState("");
  const [retrievalIncludeArchived, setRetrievalIncludeArchived] = useState(false);
  const [retrievalLoading, setRetrievalLoading] = useState(false);
  const [retrievalError, setRetrievalError] = useState<DisplayError | null>(null);
  const [retrievalResult, setRetrievalResult] = useState<DocumentRetrievalSearchResponse | null>(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiError, setAiError] = useState<DisplayError | null>(null);
  const [aiResult, setAiResult] = useState<AIAnalysisResponse | null>(null);
  const [aiIdempotencyKey, setAiIdempotencyKey] = useState<string | null>(null);
  const [reportLoading, setReportLoading] = useState(false);
  const [reportError, setReportError] = useState<DisplayError | null>(null);
  const [reportResult, setReportResult] = useState<ExecutiveReportResponse | null>(null);
  const [reportIdempotencyKey, setReportIdempotencyKey] = useState<string | null>(null);

  const [ragQuestion, setRagQuestion] = useState("");
  const [ragLimit, setRagLimit] = useState("5");
  const [ragDocumentType, setRagDocumentType] = useState("");
  const [ragLanguage, setRagLanguage] = useState("");
  const [ragTags, setRagTags] = useState("");
  const [ragIncludeArchived, setRagIncludeArchived] = useState(false);
  const [ragAnswerMode, setRagAnswerMode] = useState<InternalRagAnswerMode>("extractive");
  const [ragRequireCitations, setRagRequireCitations] = useState(true);
  const [ragLoading, setRagLoading] = useState(false);
  const [ragError, setRagError] = useState<DisplayError | null>(null);
  const [ragResult, setRagResult] = useState<InternalRagAnswerResponse | null>(null);

  /** 成功応答の provider 名から開発 Stub / OpenRouter を表示する（Key や内部設定は出さない）。 */
function providerModeLabel(provider: string): string {
  if (provider.startsWith("stub")) {
    return "Development Stub";
  }
  if (provider.startsWith("openrouter")) {
    return "OpenRouter";
  }
  return "Server Provider";
}

function toDisplayError(reason: unknown, fallbackCode: string, fallbackMessage: string): DisplayError {
    if (reason instanceof ApiClientError) {
      return { code: reason.code, message: reason.message };
    }
    return { code: fallbackCode, message: fallbackMessage };
  }

  async function submitRetrieval(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setRetrievalLoading(true);
    setRetrievalError(null);
    try {
      // 前端只把表单映射到真实后端 request，不自己做检索。
      const response = await searchDocumentRetrieval({
        query: retrievalQuery.trim(),
        limit: Number(retrievalLimit),
        include_archived: retrievalIncludeArchived,
        document_type: retrievalDocumentType.trim() || undefined,
        language: retrievalLanguage.trim() || undefined,
        tags: parseTags(retrievalTags),
      });
      setRetrievalResult(response);
      onLearningEvent?.({
        eventName: "submitRetrieval()",
        apiMethod: "POST",
        apiPath: "/api/v1/document-retrieval/search",
        apiStatus: "200 OK",
        stateChanges: ["retrievalLoading: true → false", `retrievalResult: ${response.total} matches`, "retrievalError: null"],
        backendFlow: ["document_retrieval.py search_documents()", "DocumentRetrievalService.search()", "DocumentRetrievalProvider.search()", "InMemoryKeywordRetrieval.search()"],
      });
    } catch (reason) {
      setRetrievalError(toDisplayError(reason, "DOCUMENT_RETRIEVAL_ERROR", "検索リクエストに失敗しました"));
      setRetrievalResult(null);
      onLearningEvent?.({ eventName: "submitRetrieval()", apiMethod: "POST", apiPath: "/api/v1/document-retrieval/search", apiStatus: "Backend error", stateChanges: ["retrievalLoading: true → false", "retrievalError: null → error", "retrievalResult: null"], backendFlow: ["document_retrieval.py search_documents()", "DocumentRetrievalService.search()"] });
    } finally {
      setRetrievalLoading(false);
    }
  }

  async function submitInternalRag(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setRagLoading(true);
    setRagError(null);
    try {
      // 当前 answer 页面只能展示后端已给出的 grounded answer，不在前端拼装 citation。
      const response = await answerInternalRag({
        question: ragQuestion.trim(),
        limit: Number(ragLimit),
        include_archived: ragIncludeArchived,
        document_type: ragDocumentType.trim() || undefined,
        language: ragLanguage.trim() || undefined,
        tags: parseTags(ragTags),
        answer_mode: ragAnswerMode,
        require_citations: ragRequireCitations,
      });
      setRagResult(response);
      onLearningEvent?.({
        eventName: "submitInternalRag()",
        apiMethod: "POST",
        apiPath: "/api/v1/internal-rag/answer",
        apiStatus: "200 OK",
        stateChanges: ["ragLoading: true → false", "ragResult: null → response", "ragError: null"],
        backendFlow: ["internal_rag.py answer_internal_rag()", "InternalRagService.answer()", "DocumentRetrievalProvider.search()", "RAGAnswerGenerator.generate()", "InternalRagEvaluationService"],
      });
    } catch (reason) {
      const displayError = toDisplayError(reason, "INTERNAL_RAG_ERROR", "Internal RAG リクエストに失敗しました");
      setRagError(displayError);
      setRagResult(null);
      onLearningEvent?.({
        eventName: "submitInternalRag()",
        apiMethod: "POST",
        apiPath: "/api/v1/internal-rag/answer",
        apiStatus: displayError.code === "insufficient_context" ? "422 Unprocessable Entity" : "Backend error",
        stateChanges: ["ragLoading: true → false", "ragError: null → error", "ragResult: null"],
        backendFlow: ["internal_rag.py answer_internal_rag()", "InternalRagService.answer()", "DocumentRetrievalProvider.search()"],
        note: displayError.code === "insufficient_context" ? "Backend 未找到足够的相关 Chunk：输入可能不匹配文档内容，或文档尚未完成 Chunk；这不是 RAG 页面故障。" : undefined,
      });
    } finally {
      setRagLoading(false);
    }
  }

  async function runExplicitAIAnalysis() {
    if (!retrievalResult || retrievalResult.results.length === 0 || aiLoading || reportLoading) return;
    const evidenceChars = retrievalResult.results.reduce((total, item) => total + item.content_excerpt.length, 0);
    const estimatedInputTokens = Math.max(1, Math.ceil((retrievalQuery.length + evidenceChars) / 4));
    // 确认对话在发送请求之前展示，取消时 fetch 次数保持为 0。
    const confirmed = window.confirm(
      [
        "AI分析を実行しますか？",
        "route_tier: low_cost",
        `推定入力: ${estimatedInputTokens} tokens`,
        "出力上限: 256 tokens",
        "Provider: サーバー設定（Development Stub または OpenRouter low_cost）",
        "モデル名はクライアントから指定できません。",
      ].join("\n"),
    );
    if (!confirmed) return;
    const key = aiIdempotencyKey ?? createAIIdempotencyKey();
    setAiIdempotencyKey(key);
    setAiLoading(true);
    setAiError(null);
    setReportResult(null);
    setReportError(null);
    try {
      const response = await executeAIAnalysis({
        question: retrievalQuery.trim(),
        evidence: retrievalResult.results.map((item) => ({
          document_id: item.document_id,
          chunk_id: item.chunk_id,
          score: item.score,
        })),
        confirmed: true,
      }, key);
      setAiResult(response);
      setAiIdempotencyKey(null);
    } catch (reason) {
      setAiError(toDisplayError(reason, "AI_ANALYSIS_ERROR", "AI分析に失敗しました"));
    } finally {
      setAiLoading(false);
    }
  }

  async function runExecutiveReport() {
    if (!aiResult || aiResult.status !== "succeeded" || !aiResult.citations?.length || reportLoading || aiLoading) {
      return;
    }
    const evidenceChars = aiResult.citations.reduce((total, item) => total + (item.excerpt?.length ?? 0), 0);
    const estimatedInputTokens = Math.max(1, Math.ceil((aiResult.answer.length + evidenceChars) / 4));
    const confirmed = window.confirm(
      [
        "取締役会報告を生成しますか？",
        "route_tier: high_quality（AI分析より高コスト）",
        `推定入力: ${estimatedInputTokens} tokens`,
        "出力上限: 1024 tokens",
        "Provider: サーバー設定（Development Stub または OpenRouter high_quality）",
        "モデル名はクライアントから指定できません。",
        "成功後も Approval は自動提出しません。",
      ].join("\n"),
    );
    if (!confirmed) return;
    const key = reportIdempotencyKey ?? createReportIdempotencyKey();
    setReportIdempotencyKey(key);
    setReportLoading(true);
    setReportError(null);
    try {
      const response = await generateExecutiveReport({
        ai_analysis_id: aiResult.analysis_id,
        title: `Board Report: ${retrievalQuery.trim() || "RAG Evidence"}`,
        confirmed: true,
      }, key);
      setReportResult(response);
      setReportIdempotencyKey(null);
    } catch (reason) {
      setReportError(toDisplayError(reason, "EXECUTIVE_REPORT_ERROR", "取締役会報告の生成に失敗しました"));
    } finally {
      setReportLoading(false);
    }
  }

  function clearRetrievalResult() {
    setRetrievalResult(null);
    onLearningEvent?.({ eventName: "clearRetrievalResult()", stateChanges: ["retrievalResult: response → null"], note: "清除仅修改 React state，不发送 API 请求。" });
  }

  function clearRagResult() {
    setRagResult(null);
    onLearningEvent?.({ eventName: "clearRagResult()", stateChanges: ["ragResult: response → null"], note: "清除仅修改 React state，不发送 API 请求。" });
  }

  return (
    <>
      <PageHeader
        eyebrow="RAG 検索と回答"
        title="RAG検索"
        description="現在はキーワード検索と固定ロジックによる回答を利用できます。ベクトル検索と実際の LLM 生成は未接続です。"
      />

      <section className="rag-shell" aria-label="RAG 検索ワークスペース">
        {canRetrieve && <section className="panel rag-panel">
        <div className="panel-heading">
          <span>01</span>
          <h2>文書検索</h2>
          <small>Keyword Retrieval / Deterministic Retrieval</small>
        </div>
        <form className="stack-form" onSubmit={submitRetrieval}>
          <label htmlFor="retrieval-query">検索語</label>
          <textarea
            id="retrieval-query"
            rows={4}
            value={retrievalQuery}
            onChange={(event) => setRetrievalQuery(event.target.value)}
            disabled={retrievalLoading}
          />
          <div className="filter-grid">
            <div>
              <label htmlFor="retrieval-limit">取得件数</label>
              <input id="retrieval-limit" value={retrievalLimit} onChange={(event) => setRetrievalLimit(event.target.value)} disabled={retrievalLoading} />
            </div>
            <div>
              <label htmlFor="retrieval-document-type">文書種別</label>
              <input
                id="retrieval-document-type"
                value={retrievalDocumentType}
                onChange={(event) => setRetrievalDocumentType(event.target.value)}
                disabled={retrievalLoading}
              />
            </div>
            <div>
              <label htmlFor="retrieval-language">言語</label>
              <input id="retrieval-language" value={retrievalLanguage} onChange={(event) => setRetrievalLanguage(event.target.value)} disabled={retrievalLoading} />
            </div>
            <div>
              <label htmlFor="retrieval-tags">タグ（カンマ区切り）</label>
              <input id="retrieval-tags" value={retrievalTags} onChange={(event) => setRetrievalTags(event.target.value)} disabled={retrievalLoading} />
            </div>
          </div>
          <label className="checkbox-row">
            <input
              type="checkbox"
              checked={retrievalIncludeArchived}
              onChange={(event) => setRetrievalIncludeArchived(event.target.checked)}
              disabled={retrievalLoading}
            />
            アーカイブ済みを含める
          </label>
          <div className="action-row">
            <button type="submit" disabled={retrievalLoading || retrievalQuery.trim().length === 0}>
              {retrievalLoading ? "検索中…" : "検索する"}
            </button>
            <button type="button" className="secondary-button" onClick={clearRetrievalResult}>
              結果をクリア
            </button>
          </div>
        </form>

        {retrievalError && (
          <div className="error-block">
            <StatusBanner tone="error">[{retrievalError.code}] {retrievalError.message}</StatusBanner>
            <button type="button" className="secondary-button" onClick={() => setRetrievalError(null)}>
              閉じる
            </button>
          </div>
        )}

        {retrievalLoading ? (
          <p className="empty">検索結果を読み込み中…</p>
        ) : retrievalResult === null ? (
          <p className="empty">キーワード検索を実行すると、Backend が返す実際の Chunk 一致結果を確認できます。</p>
        ) : retrievalResult.results.length === 0 ? (
          <div className="empty-block">
            <p className="empty">検索結果はありません。</p>
            <button type="button" className="secondary-button" onClick={() => setRetrievalResult(null)}>
              別の検索語で再試行
            </button>
          </div>
        ) : (
          <div className="result-stack">
            <StatusBanner tone="success">
              検索方式: {retrievalResult.retrieval_mode} / 一致件数: {retrievalResult.total}
            </StatusBanner>
            {retrievalResult.results.map((item, index) => (
              <article key={item.chunk_id} className="result-card">
                <div className="subheading">
                  <strong>順位 {index + 1}</strong>
                  <small>スコア {item.score.toFixed(3)}</small>
                </div>
                <pre className="excerpt-block">{item.content_excerpt}</pre>
                <dl className="detail-grid result-meta-grid">
                  <div><dt>文書 ID</dt><dd>{item.document_id}</dd></div>
                  <div><dt>Chunk ID</dt><dd>{item.chunk_id}</dd></div>
                  <div><dt>Chunk 番号</dt><dd>{item.chunk_index}</dd></div>
                  <div><dt>検索方式</dt><dd>{retrievalResult.retrieval_mode}</dd></div>
                  <div><dt>ソース種別</dt><dd>{item.source.source_type}</dd></div>
                  <div><dt>ソース URI</dt><dd>{item.source.uri}</dd></div>
                  <div><dt>文書タイトル</dt><dd>{item.metadata.title}</dd></div>
                  <div><dt>文書ステータス</dt><dd>{item.metadata.status}</dd></div>
                </dl>
              </article>
            ))}
            {canAnalyze && (
              <div className="result-card" aria-label="明示的 AI 分析">
                <div className="subheading">
                  <strong>AI分析（明示的呼び出し）</strong>
                  <small>low_cost / コスト管理対象</small>
                </div>
                <p>上記の検索証拠だけを使用します。ページ表示や検索では自動実行されません。Provider はサーバー設定のみです。</p>
                <button type="button" onClick={runExplicitAIAnalysis} disabled={aiLoading || retrievalResult.results.length === 0}>
                  {aiLoading ? "AI分析中…" : "AI分析"}
                </button>
                {aiError && <StatusBanner tone="error">[{aiError.code}] {aiError.message}</StatusBanner>}
                {aiResult && (
                  <div className="result-stack">
                    <StatusBanner tone="success">
                      {providerModeLabel(aiResult.provider)} / {aiResult.provider} / {aiResult.model} / {aiResult.route_tier ?? "low_cost"} / {aiResult.status}
                    </StatusBanner>
                    <pre className="answer-block">{aiResult.answer}</pre>
                    <p>Usage: {aiResult.usage.input_tokens} + {aiResult.usage.output_tokens} = {aiResult.usage.total_tokens} tokens</p>
                    <p>Cost: {aiResult.cost} {aiResult.currency}</p>
                    {canAnalyze && aiResult.status === "succeeded" && aiResult.citations.length > 0 && (
                      <div className="result-card" aria-label="高品質取締役会報告">
                        <div className="subheading">
                          <strong>生成取締役会報告（high_quality）</strong>
                          <small>高コスト / サーバー選定モデル</small>
                        </div>
                        <p>AI分析より高い LLM 用量が発生します。ページ読み込みでは自動実行されず、Approval も自動提出しません。</p>
                        <button
                          type="button"
                          onClick={runExecutiveReport}
                          disabled={reportLoading || aiLoading}
                        >
                          {reportLoading ? "取締役会報告生成中…" : "生成取締役会報告"}
                        </button>
                        {reportError && (
                          <StatusBanner tone="error">[{reportError.code}] {reportError.message}</StatusBanner>
                        )}
                        {reportResult && (
                          <div className="result-stack">
                            <StatusBanner tone="success">
                              {providerModeLabel(reportResult.provider)} / {reportResult.provider} / {reportResult.model} / {reportResult.route_tier} / {reportResult.status}
                            </StatusBanner>
                            <p>Report: {reportResult.report_id} / Version: {reportResult.report_version_id}</p>
                            <pre className="answer-block">{reportResult.executive_summary}</pre>
                            <p>Usage: {reportResult.usage.input_tokens} + {reportResult.usage.output_tokens} = {reportResult.usage.total_tokens} tokens</p>
                            <p>Cost: {reportResult.actual_cost} {reportResult.currency} (est. {reportResult.estimated_cost})</p>
                            <p>Citations: {reportResult.citations.length}</p>
                            <p>
                              Approval 入口: Tasks / Approval 画面で task_id <code>{reportResult.task_id}</code> を開き、手動で submit-approval を実行してください。自動提出は行いません。
                            </p>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </section>}

      {canAnalyze && <section className="panel rag-panel">
        <div className="panel-heading">
          <span>02</span>
          <h2>Internal RAG 回答</h2>
          <small>Deterministic Grounded Answer</small>
        </div>
        <form className="stack-form" onSubmit={submitInternalRag}>
          <label htmlFor="rag-question">質問</label>
          <textarea
            id="rag-question"
            rows={4}
            value={ragQuestion}
            onChange={(event) => setRagQuestion(event.target.value)}
            disabled={ragLoading}
          />
          <div className="filter-grid">
            <div>
              <label htmlFor="rag-limit">取得件数</label>
              <input id="rag-limit" value={ragLimit} onChange={(event) => setRagLimit(event.target.value)} disabled={ragLoading} />
            </div>
            <div>
              <label htmlFor="rag-document-type">文書種別</label>
              <input id="rag-document-type" value={ragDocumentType} onChange={(event) => setRagDocumentType(event.target.value)} disabled={ragLoading} />
            </div>
            <div>
              <label htmlFor="rag-language">言語</label>
              <input id="rag-language" value={ragLanguage} onChange={(event) => setRagLanguage(event.target.value)} disabled={ragLoading} />
            </div>
            <div>
              <label htmlFor="rag-tags">タグ（カンマ区切り）</label>
              <input id="rag-tags" value={ragTags} onChange={(event) => setRagTags(event.target.value)} disabled={ragLoading} />
            </div>
          </div>
          <div className="filter-grid">
            <div>
              <label htmlFor="rag-answer-mode">回答方式</label>
              <select
                id="rag-answer-mode"
                value={ragAnswerMode}
                onChange={(event) => setRagAnswerMode(event.target.value as InternalRagAnswerMode)}
                disabled={ragLoading}
              >
                <option value="extractive">extractive</option>
                <option value="summary">summary</option>
              </select>
            </div>
          </div>
          <label className="checkbox-row">
            <input type="checkbox" checked={ragIncludeArchived} onChange={(event) => setRagIncludeArchived(event.target.checked)} disabled={ragLoading} />
            アーカイブ済みを含める
          </label>
          <label className="checkbox-row">
            <input type="checkbox" checked={ragRequireCitations} onChange={(event) => setRagRequireCitations(event.target.checked)} disabled={ragLoading} />
            引用を必須にする
          </label>
          <div className="action-row">
            <button type="submit" disabled={ragLoading || ragQuestion.trim().length === 0}>
              {ragLoading ? "回答を生成中…" : "回答を生成"}
            </button>
            <button type="button" className="secondary-button" onClick={clearRagResult}>
              回答をクリア
            </button>
          </div>
        </form>

        {ragError && (
          <div className="error-block">
            <StatusBanner tone="error">[{ragError.code}] {ragError.message}</StatusBanner>
            <button type="button" className="secondary-button" onClick={() => setRagError(null)}>
              閉じる
            </button>
          </div>
        )}

        {ragLoading ? (
          <p className="empty">Internal RAG 回答を読み込み中…</p>
        ) : ragResult === null ? (
          <p className="empty">質問を入力すると、Backend が返す回答、信頼度、警告、引用を確認できます。</p>
        ) : (
          <div className="result-stack">
            <StatusBanner tone="success">
              検索方式: {ragResult.retrieval_mode} / 回答方式: {ragResult.answer_mode} / 信頼度: {ragResult.confidence.toFixed(2)}
            </StatusBanner>
            <article className="result-card">
              <div className="subheading">
                <strong>回答</strong>
                <small>引用 {ragResult.citations.length} 件</small>
              </div>
              <pre className="answer-block">{ragResult.answer}</pre>
              <div className="warning-list">
                {ragResult.warnings.length === 0 ? (
                  <StatusBadge value="no_warnings" />
                ) : (
                  ragResult.warnings.map((warning) => <StatusBadge key={warning} value={warning} />)
                )}
              </div>
            </article>

            <div className="citation-grid">
              {ragResult.citations.map((citation, index) => (
                <article key={citation.chunk_id} className="result-card">
                  <div className="subheading">
                    <strong>引用 {index + 1}</strong>
                    <small>スコア {citation.score.toFixed(3)}</small>
                  </div>
                  <pre className="excerpt-block">{citation.excerpt}</pre>
                  <dl className="detail-grid result-meta-grid">
                    <div><dt>文書 ID</dt><dd>{citation.document_id}</dd></div>
                    <div><dt>Chunk ID</dt><dd>{citation.chunk_id}</dd></div>
                    <div><dt>Chunk 番号</dt><dd>{citation.chunk_index}</dd></div>
                    <div><dt>ソース種別</dt><dd>{citation.source.source_type}</dd></div>
                    <div><dt>ソース URI</dt><dd>{citation.source.uri}</dd></div>
                  </dl>
                </article>
              ))}
            </div>
          </div>
        )}
      </section>}
      </section>

      <BusinessLearningPanel
        pageName="RAG検索"
        purpose="确认关东地区饮料销售资料已能被关键词检索，并以可引用结果生成固定逻辑的 Internal RAG 回答。"
        scenario="资料已在文書管理完成 Chunk 后，分析人员查询“関東地域の飲料カテゴリの売上減少”，再询问主要原因并检查 citation。"
        prerequisites="存在 validated 的 markdown／text Chunk；查询或问题不能为空。当前只有 Keyword Retrieval 与 deterministic answer，不使用真实 LLM 或 pgvector。"
        relationship="本页读取文书产生的 Chunk，并返回 document_id、chunk_id、citation。当前检索结果不会自动填入分析依頼；用户需手动把结论或问题带到下一页。"
        journey={{ previous: "文書管理", current: "2 / 4 RAG検索", completion: "检索到相关 Chunk，或生成带 citation 的 Internal RAG 回答。", next: "分析依頼", recommendedCase: "TASK-BIZ-001", transferredObjects: "检索结论、citation", connection: "当前手动整理分析问题，不自动传递 citation。" }}
        operationGuideTitle="如何选择 RAG 输入"
        operationGuides={[
          { title: "首次测试：先看这里", prerequisite: "实际操作测试优先展开本页底部「业务测试与源码学习」。", input: "当前推荐测试文档：02_関東地域在庫レポート.md。", action: "需要完整规则和六份资料对照时阅读 FRONTEND_SOURCE_LEARNING_GUIDE.md 第 6 章；07_RAG質問集.md 只作为扩展问题库。", expected: "页面提供第一次可直接复制的输入，不需要先阅读全部 Scenario01 文档。" },
          { title: "步骤 1：Document Retrieval", prerequisite: "02_関東地域在庫レポート.md 已完成 Upload → Import → Chunk，且 Chunk Count > 0。", input: "検索語：神奈川 配送遅延 夕方欠品", settings: "取得件数：5；首次测试不填 document_type、language、tags，且不勾选 archived。", action: "先点击「検索する」，不要直接生成 Internal RAG Answer。", expected: "HTTP 200；results > 0。", verification: "确认 document_id 是库存报告、chunk_id 存在、score 有返回、Chunk 摘要包含库存或配送相关内容。", next: "Retrieval 成功后再执行步骤 2。" },
          { title: "步骤 2：Internal RAG Answer", prerequisite: "步骤 1 已有相关 results。", input: "質問：神奈川で夕方欠品が増加した理由は何ですか。\n可选问题：関東地域の飲料在庫における主な問題を要約してください。\n可选问题：炭酸飲料と無糖飲料の欠品率が高い理由は何ですか。", settings: "limit=5；answer_mode=extractive；require_citations=true；首次测试不填 filters。", action: "点击「回答を生成」。", expected: "当前 Deterministic Internal RAG 从 Backend 返回 answer 与 citations，不由前端生成答案。", verification: "确认 answer、citation、confidence、warnings、retrieval_mode、answer_mode；citation 应关联库存报告 Chunk。", next: "手动整理检索结论后进入分析依頼。" },
          { title: "不推荐问题与 insufficient_context", prerequisite: "当前只准备库存报告时。", input: "不推荐：競合店舗はなぜ値下げしましたか。", action: "不要把竞争店问题当作库存报告的单文档问题。", expected: "该主题属于 05_競合店舗調査；当前 Chunk 没有相应证据时，insufficient_context 是正常业务结果。", troubleshooting: "依次确认 Import 完成、Chunk 完成、Chunk Count > 0、検索語来自正文、Retrieval 已有 results、language/tags/document_type 未过滤过严、require_citations 证据是否不足、文档是否已 archived。" },
          { title: "综合经营问题的前置资料", prerequisite: "要询问卖上、在库、促销、顾客、竞争、KPI 的综合原因时。", input: "関東地域の飲料カテゴリの売上減少原因を、売上、在庫、販促、顧客、競合、KPIの観点から整理してください。", action: "先将 01 销售、02 库存、03 促销、04 顾客、05 竞争、06 KPI 的相关资料完成 Chunk。", expected: "一份库存报告不能独立证明全部销售下降原因；当前 RAG 只根据已存在证据回答。", next: "Retrieval 成功 → Internal RAG → 分析依頼；citation 不会自动带入 TasksPage。" },
          { title: "清除操作", prerequisite: "已有检索或回答结果。", input: "「結果をクリア」或「回答をクリア」。", action: "点击对应清除按钮。", expected: "只修改 React state，不调用 Backend；可重新执行搜索或回答。" },
        ]}
        cases={[
          { id: "RAG-BIZ-001", group: "标准业务 Case", purpose: "库存报告的正常 Retrieval → Internal RAG 流程。", prerequisite: "02_関東地域在庫レポート.md 已完成 Upload、Import、Chunk，Chunk Count > 0。", input: "検索語：神奈川 配送遅延 夕方欠品；質問：神奈川で夕方欠品が増加した理由は何ですか。", operation: "先搜索并确认 results，再以相同主题生成回答。", expectedApi: "POST /api/v1/document-retrieval/search → 200；POST /api/v1/internal-rag/answer → 200", pageOutput: "results、document_id、chunk_id、score；随后显示 answer、citation、confidence、warnings。", businessCheck: "先确认库存证据，再读取确定性回答；不让前端补造原因。", expected: "Retrieval 成功后才执行 Answer。" },
          { id: "RAG-BIZ-002", group: "异常与维护测试 Case", purpose: "确认真实支持的 filters。", prerequisite: "先完成 RAG-BIZ-001 的无 filter 首次检索。", input: "在已有匹配关键词基础上，测试 document_type=markdown、language 或 tags；每次只增加一个 filter。", operation: "重新搜索并比较 results。", expectedApi: "POST /api/v1/document-retrieval/search → 200", pageOutput: "过滤条件过严时 results 可为 0；首次测试不建议预先添加 filters。", businessCheck: "区分无证据与前端过滤条件排除了已有证据。", expected: "确认 filters 只缩小当前 Keyword Retrieval 范围。" },
          { id: "RAG-BIZ-003", group: "异常与维护测试 Case", purpose: "确认无 Chunk 命中。", prerequisite: "已有至少一份完成 Chunk 的资料。", input: "検索語：南米向け飲料輸出", operation: "只执行 Document Retrieval。", expectedApi: "POST /api/v1/document-retrieval/search → 200", pageOutput: "results=0，页面显示「検索結果はありません。」。", businessCheck: "空结果说明当前 Chunk 没有该主题，不是页面伪造答案。", expected: "results=0 时不建议直接生成 Internal RAG Answer。" },
          { id: "RAG-BIZ-004", group: "异常与维护测试 Case", purpose: "确认资料不匹配时的证据不足。", prerequisite: "当前只准备库存报告，引用必須为 true。", input: "質問：競合店舗はなぜ値下げしましたか。", operation: "生成 Internal RAG Answer。", expectedApi: "POST /api/v1/internal-rag/answer → 422 insufficient_context", pageOutput: "页面显示 error code 与 message。", businessCheck: "竞争店主题需要 05_競合店舗調査 的 Chunk；库存资料不能证明该事实。", expected: "insufficient_context 是正常业务结果。" },
          { id: "RAG-BIZ-005", group: "异常与维护测试 Case", purpose: "确认清除只影响 React state。", prerequisite: "已执行 Retrieval 或 Internal RAG。", input: "点击「結果をクリア」和「回答をクリア」。", operation: "分别清除结果。", expectedApi: "无 API 请求", pageOutput: "对应结果区域恢复为空状态，可再次输入。", businessCheck: "清除不删除 Backend 文档、Chunk 或 Citation。", expected: "仅 setRetrievalResult(null)／setRagResult(null)。" },
        ]}
        flows={[
          {
            title: "关键词文书搜索",
            api: "POST /api/v1/document-retrieval/search",
            frontend: ["RagPage submitRetrieval()", "searchDocumentRetrieval()", "setRetrievalResult", "结果／空状态显示"],
            backend: ["document_retrieval.py search_documents()", "DocumentRetrievalService.search()", "DocumentRetrievalProvider.search()", "InMemoryKeywordRetrieval.search()"],
            note: "检索实现按 Chunk 的关键词匹配排序；当前没有向量检索或 reranker。",
          },
          {
            title: "Internal RAG 回答",
            api: "POST /api/v1/internal-rag/answer",
            frontend: ["RagPage submitInternalRag()", "answerInternalRag()", "setRagResult", "回答、warnings、citations 显示"],
            backend: ["internal_rag.py answer_internal_rag()", "InternalRagService.answer()", "DocumentRetrievalProvider.search()", "RAGAnswerGenerator.generate()", "InternalRagEvaluationService"],
            note: "回答是基于检索结果的 deterministic assembly；citation 来自 Backend response，不由前端拼装。",
          },
        ]}
      />
    </>
  );
}

function createReportIdempotencyKey(): string {
  if (typeof crypto !== "undefined" && typeof crypto.randomUUID === "function") {
    return `er-${crypto.randomUUID()}`;
  }
  return `er-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function createAIIdempotencyKey(): string {
  const randomUUID = globalThis.crypto?.randomUUID?.bind(globalThis.crypto);
  return `ai-${randomUUID ? randomUUID() : `${Date.now()}-${Math.random().toString(16).slice(2)}`}`;
}

function parseTags(raw: string): string[] | undefined {
  const tags = raw
    .split(",")
    .map((item) => item.trim())
    .filter((item) => item.length > 0);
  return tags.length > 0 ? tags : undefined;
}
