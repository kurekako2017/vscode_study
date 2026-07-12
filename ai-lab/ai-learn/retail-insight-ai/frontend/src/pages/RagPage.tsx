import { FormEvent, useState } from "react";

import { ApiClientError, answerInternalRag, searchDocumentRetrieval } from "../api";
import type {
  DisplayError,
  DocumentRetrievalSearchResponse,
  InternalRagAnswerMode,
  InternalRagAnswerResponse,
} from "../types";

/**
 * RagPage 负责 deterministic Retrieval + Internal RAG 两个真实后端能力。
 *
 * 当前实现边界：
 * - 只接 keyword retrieval / deterministic internal RAG。
 * - 不接真实 LLM、embedding、pgvector 或 hybrid retrieval。
 */
export function RagPage() {
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
    } catch (reason) {
      setRetrievalError(toDisplayError(reason, "DOCUMENT_RETRIEVAL_ERROR", "Retrieval request failed"));
      setRetrievalResult(null);
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
    } catch (reason) {
      setRagError(toDisplayError(reason, "INTERNAL_RAG_ERROR", "Internal RAG request failed"));
      setRagResult(null);
    } finally {
      setRagLoading(false);
    }
  }

  return (
    <section className="rag-shell" aria-label="RAG workspace">
      <section className="panel rag-panel">
        <div className="panel-heading">
          <span>01</span>
          <h2>Document Retrieval</h2>
          <small>Keyword Retrieval / Deterministic Retrieval</small>
        </div>
        <form className="stack-form" onSubmit={submitRetrieval}>
          <label htmlFor="retrieval-query">Query</label>
          <textarea
            id="retrieval-query"
            rows={4}
            value={retrievalQuery}
            onChange={(event) => setRetrievalQuery(event.target.value)}
            disabled={retrievalLoading}
          />
          <div className="filter-grid">
            <div>
              <label htmlFor="retrieval-limit">Limit</label>
              <input id="retrieval-limit" value={retrievalLimit} onChange={(event) => setRetrievalLimit(event.target.value)} disabled={retrievalLoading} />
            </div>
            <div>
              <label htmlFor="retrieval-document-type">Document Type</label>
              <input
                id="retrieval-document-type"
                value={retrievalDocumentType}
                onChange={(event) => setRetrievalDocumentType(event.target.value)}
                disabled={retrievalLoading}
              />
            </div>
            <div>
              <label htmlFor="retrieval-language">Language</label>
              <input id="retrieval-language" value={retrievalLanguage} onChange={(event) => setRetrievalLanguage(event.target.value)} disabled={retrievalLoading} />
            </div>
            <div>
              <label htmlFor="retrieval-tags">Tags (comma separated)</label>
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
            Include archived
          </label>
          <div className="action-row">
            <button type="submit" disabled={retrievalLoading || retrievalQuery.trim().length === 0}>
              {retrievalLoading ? "Searching…" : "Search Retrieval"}
            </button>
            <button type="button" className="secondary-button" onClick={() => setRetrievalResult(null)}>
              Clear Result
            </button>
          </div>
        </form>

        {retrievalError && (
          <div className="error-block">
            <div className="error" role="alert">[{retrievalError.code}] {retrievalError.message}</div>
            <button type="button" className="secondary-button" onClick={() => setRetrievalError(null)}>
              Dismiss
            </button>
          </div>
        )}

        {retrievalLoading ? (
          <p className="empty">Loading retrieval result…</p>
        ) : retrievalResult === null ? (
          <p className="empty">Run a keyword retrieval request to see real chunk matches from the backend.</p>
        ) : retrievalResult.results.length === 0 ? (
          <div className="empty-block">
            <p className="empty">No retrieval results found.</p>
            <button type="button" className="secondary-button" onClick={() => setRetrievalResult(null)}>
              Retry with another query
            </button>
          </div>
        ) : (
          <div className="result-stack">
            <div className="success-banner" role="status">
              Retrieval mode: {retrievalResult.retrieval_mode} / Total matches: {retrievalResult.total}
            </div>
            {retrievalResult.results.map((item, index) => (
              <article key={item.chunk_id} className="result-card">
                <div className="subheading">
                  <strong>Rank {index + 1}</strong>
                  <small>Score {item.score.toFixed(3)}</small>
                </div>
                <pre className="excerpt-block">{item.content_excerpt}</pre>
                <dl className="detail-grid result-meta-grid">
                  <div><dt>Document ID</dt><dd>{item.document_id}</dd></div>
                  <div><dt>Chunk ID</dt><dd>{item.chunk_id}</dd></div>
                  <div><dt>Chunk Index</dt><dd>{item.chunk_index}</dd></div>
                  <div><dt>Mode</dt><dd>{retrievalResult.retrieval_mode}</dd></div>
                  <div><dt>Source Type</dt><dd>{item.source.source_type}</dd></div>
                  <div><dt>Source URI</dt><dd>{item.source.uri}</dd></div>
                  <div><dt>Metadata Title</dt><dd>{item.metadata.title}</dd></div>
                  <div><dt>Metadata Status</dt><dd>{item.metadata.status}</dd></div>
                </dl>
              </article>
            ))}
          </div>
        )}
      </section>

      <section className="panel rag-panel">
        <div className="panel-heading">
          <span>02</span>
          <h2>Internal RAG Answer</h2>
          <small>Deterministic Grounded Answer</small>
        </div>
        <form className="stack-form" onSubmit={submitInternalRag}>
          <label htmlFor="rag-question">Question</label>
          <textarea
            id="rag-question"
            rows={4}
            value={ragQuestion}
            onChange={(event) => setRagQuestion(event.target.value)}
            disabled={ragLoading}
          />
          <div className="filter-grid">
            <div>
              <label htmlFor="rag-limit">Limit</label>
              <input id="rag-limit" value={ragLimit} onChange={(event) => setRagLimit(event.target.value)} disabled={ragLoading} />
            </div>
            <div>
              <label htmlFor="rag-document-type">Document Type</label>
              <input id="rag-document-type" value={ragDocumentType} onChange={(event) => setRagDocumentType(event.target.value)} disabled={ragLoading} />
            </div>
            <div>
              <label htmlFor="rag-language">Language</label>
              <input id="rag-language" value={ragLanguage} onChange={(event) => setRagLanguage(event.target.value)} disabled={ragLoading} />
            </div>
            <div>
              <label htmlFor="rag-tags">Tags (comma separated)</label>
              <input id="rag-tags" value={ragTags} onChange={(event) => setRagTags(event.target.value)} disabled={ragLoading} />
            </div>
          </div>
          <div className="filter-grid">
            <div>
              <label htmlFor="rag-answer-mode">Answer Mode</label>
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
            Include archived
          </label>
          <label className="checkbox-row">
            <input type="checkbox" checked={ragRequireCitations} onChange={(event) => setRagRequireCitations(event.target.checked)} disabled={ragLoading} />
            Require citations
          </label>
          <div className="action-row">
            <button type="submit" disabled={ragLoading || ragQuestion.trim().length === 0}>
              {ragLoading ? "Answering…" : "Generate Answer"}
            </button>
            <button type="button" className="secondary-button" onClick={() => setRagResult(null)}>
              Clear Answer
            </button>
          </div>
        </form>

        {ragError && (
          <div className="error-block">
            <div className="error" role="alert">[{ragError.code}] {ragError.message}</div>
            <button type="button" className="secondary-button" onClick={() => setRagError(null)}>
              Dismiss
            </button>
          </div>
        )}

        {ragLoading ? (
          <p className="empty">Loading internal RAG answer…</p>
        ) : ragResult === null ? (
          <p className="empty">Ask a question to see the grounded answer, confidence, warnings, and citations from the backend.</p>
        ) : (
          <div className="result-stack">
            <div className="success-banner" role="status">
              Retrieval mode: {ragResult.retrieval_mode} / Answer mode: {ragResult.answer_mode} / Confidence: {ragResult.confidence.toFixed(2)}
            </div>
            <article className="result-card">
              <div className="subheading">
                <strong>Answer</strong>
                <small>{ragResult.citations.length} citations</small>
              </div>
              <pre className="answer-block">{ragResult.answer}</pre>
              <div className="warning-list">
                {ragResult.warnings.length === 0 ? (
                  <span className="pill">no warnings</span>
                ) : (
                  ragResult.warnings.map((warning) => <span key={warning} className="pill">{warning}</span>)
                )}
              </div>
            </article>

            <div className="citation-grid">
              {ragResult.citations.map((citation, index) => (
                <article key={citation.chunk_id} className="result-card">
                  <div className="subheading">
                    <strong>Citation {index + 1}</strong>
                    <small>Score {citation.score.toFixed(3)}</small>
                  </div>
                  <pre className="excerpt-block">{citation.excerpt}</pre>
                  <dl className="detail-grid result-meta-grid">
                    <div><dt>Document ID</dt><dd>{citation.document_id}</dd></div>
                    <div><dt>Chunk ID</dt><dd>{citation.chunk_id}</dd></div>
                    <div><dt>Chunk Index</dt><dd>{citation.chunk_index}</dd></div>
                    <div><dt>Source Type</dt><dd>{citation.source.source_type}</dd></div>
                    <div><dt>Source URI</dt><dd>{citation.source.uri}</dd></div>
                  </dl>
                </article>
              ))}
            </div>
          </div>
        )}
      </section>
    </section>
  );
}

function parseTags(raw: string): string[] | undefined {
  const tags = raw
    .split(",")
    .map((item) => item.trim())
    .filter((item) => item.length > 0);
  return tags.length > 0 ? tags : undefined;
}
