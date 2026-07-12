import { FormEvent, useState } from "react";

import { ApiClientError, answerInternalRag, searchDocumentRetrieval } from "../api";
import { BusinessLearningPanel } from "../components/BusinessLearningPanel";
import { PageHeader } from "../components/PageHeader";
import { StatusBadge } from "../components/StatusBadge";
import { StatusBanner } from "../components/StatusBanner";
import type {
  DisplayError,
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
}

export function RagPage({ onLearningEvent }: RagPageProps = {}) {
  const [retrievalQuery, setRetrievalQuery] = useState("");
  const [retrievalLimit, setRetrievalLimit] = useState("10");
  const [retrievalDocumentType, setRetrievalDocumentType] = useState("");
  const [retrievalLanguage, setRetrievalLanguage] = useState("");
  const [retrievalTags, setRetrievalTags] = useState("");
  const [retrievalIncludeArchived, setRetrievalIncludeArchived] = useState(false);
  const [retrievalLoading, setRetrievalLoading] = useState(false);
  const [retrievalError, setRetrievalError] = useState<DisplayError | null>(null);
  const [retrievalResult, setRetrievalResult] = useState<DocumentRetrievalSearchResponse | null>(null);

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
        <section className="panel rag-panel">
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
          </div>
        )}
      </section>

      <section className="panel rag-panel">
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
      </section>
      </section>

      <BusinessLearningPanel
        pageName="RAG検索"
        purpose="确认关东地区饮料销售资料已能被关键词检索，并以可引用结果生成固定逻辑的 Internal RAG 回答。"
        scenario="资料已在文書管理完成 Chunk 后，分析人员查询“関東地域の飲料カテゴリの売上減少”，再询问主要原因并检查 citation。"
        prerequisites="存在 validated 的 markdown／text Chunk；查询或问题不能为空。当前只有 Keyword Retrieval 与 deterministic answer，不使用真实 LLM 或 pgvector。"
        relationship="本页读取文书产生的 Chunk，并返回 document_id、chunk_id、citation。当前检索结果不会自动填入分析依頼；用户需手动把结论或问题带到下一页。"
        cases={[
          { id: "RAG-BIZ-001", purpose: "检索关东饮料销售下降资料。", input: "検索語：関東地域の飲料カテゴリの売上減少；取得件数：5。", expected: "POST 搜索返回 results、total、retrieval_mode；页面显示文書 ID、Chunk ID、score 与来源。" },
          { id: "RAG-BIZ-002", purpose: "确认搜索必填项。", input: "清空検索語。", expected: "「検索する」不可点击，不发送请求；空白 query 直接请求时 Backend 返回实际校验错误。" },
          { id: "RAG-BIZ-003", purpose: "确认无资料命中。", input: "输入不存在的业务关键词。", expected: "HTTP 成功但 results 为 0，页面显示「検索結果はありません。」。" },
          { id: "RAG-BIZ-004", purpose: "确认资料不足的 RAG 业务错误。", input: "質問输入无法由现有 Chunk 支撑的问题，引用必須为 true。", expected: "Backend 返回实际 insufficient_context 或 citation 相关错误，页面显示 error code 与 message。" },
          { id: "RAG-BIZ-005", purpose: "确认清除只影响页面。", input: "点击「結果をクリア」或「回答をクリア」。", expected: "仅 setRetrievalResult(null)／setRagResult(null)，不发起 Backend 请求，可重新执行搜索或回答。" },
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

function parseTags(raw: string): string[] | undefined {
  const tags = raw
    .split(",")
    .map((item) => item.trim())
    .filter((item) => item.length > 0);
  return tags.length > 0 ? tags : undefined;
}
