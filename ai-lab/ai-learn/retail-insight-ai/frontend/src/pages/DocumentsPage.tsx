import { FormEvent, useEffect, useState } from "react";

import {
  ApiClientError,
  archiveDocument,
  chunkDocument,
  getDocument,
  getDocumentChunks,
  importDocument,
  listDocuments,
  uploadDocument,
} from "../api";
import { BusinessLearningPanel } from "../components/BusinessLearningPanel";
import { PageHeader } from "../components/PageHeader";
import { StatusBadge } from "../components/StatusBadge";
import { StatusBanner } from "../components/StatusBanner";
import type { DisplayError, DocumentChunkListResponse, DocumentListResponse, DocumentResponse } from "../types";
import type { RecordLearningEvent } from "../learning/learningTypes";

const defaultOwner = "analysis-team";
type DocumentAction = "archive" | "import" | "chunk" | null;

/**
 * DocumentsPage 负责上传、列表、详情和文档状态操作。
 *
 * 为什么独立成页：
 * - 这一页的状态已经和 Tasks 页面没有直接耦合，拆开后更便于继续扩展 RAG / Approval。
 */
interface DocumentsPageProps {
  onLearningEvent?: RecordLearningEvent;
  canWrite?: boolean;
  canArchive?: boolean;
}

export function DocumentsPage({
  onLearningEvent,
  canWrite = true,
  canArchive = true,
}: DocumentsPageProps = {}) {
  const [documents, setDocuments] = useState<DocumentListResponse["items"]>([]);
  const [documentsLoading, setDocumentsLoading] = useState(false);
  const [documentsRefreshing, setDocumentsRefreshing] = useState(false);
  const [documentsError, setDocumentsError] = useState<DisplayError | null>(null);
  const [selectedDocumentId, setSelectedDocumentId] = useState<string | null>(null);
  const [selectedDocument, setSelectedDocument] = useState<DocumentResponse | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);
  const [detailError, setDetailError] = useState<DisplayError | null>(null);
  const [chunkData, setChunkData] = useState<DocumentChunkListResponse | null>(null);
  const [chunkLoading, setChunkLoading] = useState(false);
  const [chunkError, setChunkError] = useState<DisplayError | null>(null);
  const [activeDocumentAction, setActiveDocumentAction] = useState<DocumentAction>(null);
  const [bannerMessage, setBannerMessage] = useState<string | null>(null);
  const [showArchived, setShowArchived] = useState(false);

  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [uploadTitle, setUploadTitle] = useState("");
  const [uploadDescription, setUploadDescription] = useState("");
  const [uploadOwner, setUploadOwner] = useState(defaultOwner);
  const [uploadLanguage, setUploadLanguage] = useState("ja");
  const [uploadTags, setUploadTags] = useState("");
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState<DisplayError | null>(null);

  useEffect(() => {
    void loadDocuments(true);
  }, [showArchived]);

  useEffect(() => {
    if (selectedDocumentId === null) {
      setSelectedDocument(null);
      setDetailError(null);
      setChunkData(null);
      setChunkError(null);
      return;
    }
    void refreshSelectedDocument(selectedDocumentId);
  }, [selectedDocumentId]);

  function toDisplayError(reason: unknown, fallbackCode: string, fallbackMessage: string): DisplayError {
    if (reason instanceof ApiClientError) {
      return { code: reason.code, message: reason.message };
    }
    return { code: fallbackCode, message: fallbackMessage };
  }

  function showBanner(message: string) {
    setBannerMessage(message);
  }

  async function loadDocuments(force = false) {
    if (force) {
      setDocumentsLoading(true);
    } else {
      setDocumentsRefreshing(true);
    }
    setDocumentsError(null);
    try {
      const data = await listDocuments({ include_archived: showArchived });
      setDocuments(data.items);
      setSelectedDocumentId((current) => {
        if (current !== null && data.items.some((item) => item.document_id === current)) {
          return current;
        }
        return data.items[0]?.document_id ?? null;
      });
    } catch (reason) {
      setDocumentsError(toDisplayError(reason, "DOCUMENT_LIST_ERROR", "ドキュメント一覧の取得に失敗しました"));
    } finally {
      setDocumentsLoading(false);
      setDocumentsRefreshing(false);
    }
  }

  async function refreshSelectedDocument(documentId: string) {
    setDetailLoading(true);
    setDetailError(null);
    setChunkLoading(true);
    setChunkError(null);

    try {
      setSelectedDocument(await getDocument(documentId));
    } catch (reason) {
      setSelectedDocument(null);
      setDetailError(toDisplayError(reason, "DOCUMENT_DETAIL_ERROR", "ドキュメント詳細の取得に失敗しました"));
    } finally {
      setDetailLoading(false);
    }

    try {
      setChunkData(await getDocumentChunks(documentId));
    } catch (reason) {
      setChunkData(null);
      setChunkError(toDisplayError(reason, "DOCUMENT_CHUNK_READ_ERROR", "チャンク情報の取得に失敗しました"));
    } finally {
      setChunkLoading(false);
    }
  }

  async function submitUpload(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (uploadFile === null) return;

    setUploading(true);
    setUploadError(null);
    setBannerMessage(null);

    try {
      const session = await uploadDocument({
        file: uploadFile,
        metadata: {
          title: uploadTitle.trim(),
          description: uploadDescription.trim() || undefined,
          owner: uploadOwner.trim(),
          tags: parseTags(uploadTags),
          language: uploadLanguage,
        },
      });
      await loadDocuments(false);
      setSelectedDocumentId(session.document_id);
      setUploadFile(null);
      setUploadTitle("");
      setUploadDescription("");
      setUploadTags("");
      showBanner(`アップロードが完了しました: ${session.document_id}`);
      onLearningEvent?.({
        eventName: "submitUpload()",
        apiMethod: "POST",
        apiPath: "/api/v1/documents",
        apiStatus: "201 Created",
        stateChanges: ["uploading: true → false", `selectedDocumentId: ${session.document_id}`, "documents: 刷新"],
        backendFlow: ["documents.py upload_document()", "DocumentUploadService.upload_document()", "InMemoryDocumentRepository.create()"],
      });
    } catch (reason) {
      setUploadError(toDisplayError(reason, "DOCUMENT_UPLOAD_ERROR", "ドキュメントのアップロードに失敗しました"));
      onLearningEvent?.({ eventName: "submitUpload()", apiMethod: "POST", apiPath: "/api/v1/documents", apiStatus: "Backend error", stateChanges: ["uploading: true → false", "uploadError: null → error"], backendFlow: ["documents.py upload_document()", "DocumentUploadService.upload_document()"] });
    } finally {
      setUploading(false);
    }
  }

  async function runDocumentAction(action: Exclude<DocumentAction, null>) {
    if (selectedDocument === null) return;

    setActiveDocumentAction(action);
    setBannerMessage(null);
    setDetailError(null);
    setChunkError(null);

    try {
      if (action === "archive") {
        const result = await archiveDocument(selectedDocument.document_id);
        showBanner(`アーカイブを受け付けました: ${result.document_id} (${result.status})`);
        onLearningEvent?.({ eventName: 'runDocumentAction("archive")', apiMethod: "DELETE", apiPath: `/api/v1/documents/${selectedDocument.document_id}`, apiStatus: "202 Accepted", stateChanges: ["activeDocumentAction: archive → null", `status: ${result.status}`, "列表与详情刷新"], backendFlow: ["documents.py archive_document()", "DocumentArchiveService.archive_document()", "InMemoryDocumentRepository.update()"] });
      }
      if (action === "import") {
        const result = await importDocument(selectedDocument.document_id);
        showBanner(`Import 結果: ${result.status}`);
        onLearningEvent?.({ eventName: 'runDocumentAction("import")', apiMethod: "POST", apiPath: `/api/v1/documents/${selectedDocument.document_id}/import`, apiStatus: "201 Created", stateChanges: ["activeDocumentAction: import → null", `import status: ${result.status}`, "列表与详情刷新"], backendFlow: ["document_imports.py import_document()", "DocumentImportService.import_document()", "InMemoryDocumentRepository.get() / update()"] });
      }
      if (action === "chunk") {
        const result = await chunkDocument(selectedDocument.document_id);
        showBanner(`Chunk 処理が完了しました: ${result.items.length} 件`);
        onLearningEvent?.({ eventName: 'runDocumentAction("chunk")', apiMethod: "POST", apiPath: `/api/v1/documents/${selectedDocument.document_id}/chunks`, apiStatus: "201 Created", stateChanges: ["activeDocumentAction: chunk → null", `chunkData: ${result.items.length} items`, "列表与详情刷新"], backendFlow: ["document_chunks.py chunk_document()", "DocumentChunkService.chunk_document()", "InMemoryDocumentChunkRepository.replace_for_document()"] });
      }
      await loadDocuments(false);
      await refreshSelectedDocument(selectedDocument.document_id);
    } catch (reason) {
      const display = toDisplayError(reason, "DOCUMENT_ACTION_ERROR", "ドキュメント操作に失敗しました");
      if (action === "chunk") {
        setChunkError(display);
      } else {
        setDetailError(display);
      }
      onLearningEvent?.({ eventName: `runDocumentAction("${action}")`, apiStatus: "Backend error", stateChanges: ["activeDocumentAction: action → null", "detailError / chunkError: null → error"], backendFlow: ["对应 Document Router", "对应 Document Service", "业务校验或 Repository 错误"] });
    } finally {
      setActiveDocumentAction(null);
    }
  }

  const selectedDocumentBusy = activeDocumentAction !== null;

  return (
    <>
      <PageHeader
        eyebrow="文書ワークスペース / PostgreSQL"
        title="文書管理"
        description="列表来自当前 Backend Repository（正式运行为 PostgreSQL）。上传后正文写入数据库 content 字段（非独立对象存储）。状态：uploaded→Import(validated)→Chunk 后才适合检索。"
      />

      <section className="documents-shell" aria-label="文档管理页面">
        {canWrite && <aside className="panel upload-panel">
        <div className="panel-heading">
          <span>01</span>
          <h2>文書アップロード</h2>
        </div>
        <form onSubmit={submitUpload} className="stack-form">
          <label htmlFor="upload-file">ファイル</label>
          <input
            id="upload-file"
            type="file"
            onChange={(event) => {
              const nextFile = event.target.files?.[0] ?? null;
              setUploadFile(nextFile);
              if (nextFile !== null && uploadTitle.trim().length === 0) {
                setUploadTitle(nextFile.name);
              }
            }}
            disabled={uploading}
          />
          {uploadFile && <p className="selection">選択済み: {uploadFile.name}</p>}

          <label htmlFor="upload-title">タイトル</label>
          <input id="upload-title" value={uploadTitle} onChange={(event) => setUploadTitle(event.target.value)} disabled={uploading} />

          <label htmlFor="upload-description">説明</label>
          <textarea
            id="upload-description"
            rows={3}
            value={uploadDescription}
            onChange={(event) => setUploadDescription(event.target.value)}
            disabled={uploading}
          />

          <label htmlFor="upload-owner">担当者</label>
          <input id="upload-owner" value={uploadOwner} onChange={(event) => setUploadOwner(event.target.value)} disabled={uploading} />

          <label htmlFor="upload-language">言語</label>
          <input
            id="upload-language"
            value={uploadLanguage}
            onChange={(event) => setUploadLanguage(event.target.value)}
            disabled={uploading}
          />

          <label htmlFor="upload-tags">タグ（カンマ区切り）</label>
          <input id="upload-tags" value={uploadTags} onChange={(event) => setUploadTags(event.target.value)} disabled={uploading} />

          <button
            type="submit"
            disabled={
              uploading
              || uploadFile === null
              || uploadTitle.trim().length === 0
              || uploadOwner.trim().length === 0
              || uploadLanguage.trim().length === 0
            }
          >
            {uploading ? "アップロード中…" : "文書をアップロード"}
          </button>
          {uploadError && <StatusBanner tone="error">[{uploadError.code}] {uploadError.message}</StatusBanner>}
        </form>
        </aside>}

        <section className="documents-main">
        <section className="panel list-panel" aria-live="polite">
          <div className="panel-heading">
            <span>02</span>
            <h2>文書一覧</h2>
            <small>{documentsRefreshing ? "更新中" : `${documents.length} 件`}</small>
          </div>

          <div className="toolbar">
            <label className="checkbox-row">
              <input type="checkbox" checked={showArchived} onChange={(event) => setShowArchived(event.target.checked)} />
              アーカイブ済みを含める
            </label>
            <button type="button" className="secondary-button" onClick={() => void loadDocuments(false)}>
              再試行 / 更新
            </button>
          </div>

          {bannerMessage && <StatusBanner tone="success">{bannerMessage}</StatusBanner>}
          {documentsError && <StatusBanner tone="error">[{documentsError.code}] {documentsError.message}</StatusBanner>}

          {documentsLoading ? (
            <p className="empty">文書を読み込み中…</p>
          ) : documents.length === 0 ? (
            <p className="empty">文書はまだありません。ファイルをアップロードして文書ワークフローを開始してください。</p>
          ) : (
            <div className="document-table" role="list" aria-label="document-list">
              {documents.map((document) => {
                const selected = selectedDocumentId === document.document_id;
                return (
                  <button
                    key={document.document_id}
                    type="button"
                    role="listitem"
                    className={selected ? "document-row selected" : "document-row"}
                    onClick={() => setSelectedDocumentId(document.document_id)}
                  >
                    <div>
                      <strong>{document.title}</strong>
                      <small>{document.document_id}</small>
                    </div>
                    <div className="row-meta">
                      <StatusBadge value={document.status} />
                      <span title="检索就绪提示">
                        {document.status === "validated" || document.status === "indexed"
                          ? "已 Import，需确认 Chunk"
                          : document.status === "uploaded"
                            ? "需 Import"
                            : document.status === "archived"
                              ? "已归档"
                              : document.status}
                      </span>
                      <span>{document.document_type}</span>
                      <span>{formatDate(document.updated_at)}</span>
                    </div>
                  </button>
                );
              })}
            </div>
          )}
        </section>

        <section className="panel detail-panel" aria-live="polite">
          <div className="panel-heading">
            <span>03</span>
            <h2>文書詳細</h2>
            {selectedDocument && <small>{selectedDocument.document_id}</small>}
          </div>

          {detailError && <StatusBanner tone="error">[{detailError.code}] {detailError.message}</StatusBanner>}

          {selectedDocumentId === null ? (
            <p className="empty">一覧から文書を選択すると、詳細と操作を確認できます。</p>
          ) : detailLoading && selectedDocument === null ? (
            <p className="empty">文書詳細を読み込み中…</p>
          ) : selectedDocument === null ? (
            <div className="empty-block">
              <p className="empty">文書詳細を取得できません。</p>
              <button type="button" className="secondary-button" onClick={() => void refreshSelectedDocument(selectedDocumentId)}>
                再試行
              </button>
            </div>
          ) : (
            <>
              <dl className="detail-grid">
                <div><dt>タイトル</dt><dd>{selectedDocument.title}</dd></div>
                <div><dt>ステータス</dt><dd>{selectedDocument.status}</dd></div>
                <div><dt>種類</dt><dd>{selectedDocument.document_type}</dd></div>
                <div><dt>言語</dt><dd>{selectedDocument.language}</dd></div>
                <div><dt>担当者</dt><dd>{selectedDocument.owner}</dd></div>
                <div><dt>バージョン</dt><dd>{selectedDocument.version}</dd></div>
                <div><dt>作成日時</dt><dd>{formatDate(selectedDocument.created_at)}</dd></div>
                <div><dt>更新日時</dt><dd>{formatDate(selectedDocument.updated_at)}</dd></div>
                <div><dt>Chunk 数</dt><dd>{chunkData ? chunkData.items.length : chunkLoading ? "読み込み中…" : "—"}</dd></div>
                <div>
                  <dt>检索就绪</dt>
                  <dd>
                    {chunkData && chunkData.items.length > 0
                      ? "已 Chunk，可用于 RAG 检索"
                      : selectedDocument.status === "validated"
                        ? "已 Import，请执行 Chunk"
                        : selectedDocument.status === "uploaded"
                          ? "仅 uploaded：请 Import → Chunk"
                          : selectedDocument.status}
                  </dd>
                </div>
                <div>
                  <dt>存储说明</dt>
                  <dd>正文保存在 PostgreSQL documents.content（仓库内 Scenario01 文件需上传后才入库）</dd>
                </div>
                <div><dt>タグ</dt><dd>{selectedDocument.tags.length > 0 ? selectedDocument.tags.join(", ") : "—"}</dd></div>
              </dl>

              {selectedDocument.description && (
                <div className="detail-note">
                  <strong>説明</strong>
                  <p>{selectedDocument.description}</p>
                </div>
              )}

              <div className="action-grid">
                {canArchive && <button type="button" disabled={selectedDocumentBusy} onClick={() => void runDocumentAction("archive")}>
                  {activeDocumentAction === "archive" ? "アーカイブ中…" : "アーカイブ"}
                </button>}
                {canWrite && <button type="button" disabled={selectedDocumentBusy} onClick={() => void runDocumentAction("import")}>
                  {activeDocumentAction === "import" ? "Import 中…" : "Import"}
                </button>}
                {canWrite && <button type="button" disabled={selectedDocumentBusy} onClick={() => void runDocumentAction("chunk")}>
                  {activeDocumentAction === "chunk" ? "Chunk 処理中…" : "Chunk 実行"}
                </button>}
                <button
                  type="button"
                  className="secondary-button"
                  disabled={selectedDocumentBusy}
                  onClick={() => void refreshSelectedDocument(selectedDocument.document_id)}
                >
                  詳細を再読み込み
                </button>
              </div>

              {chunkError && <StatusBanner tone="error">[{chunkError.code}] {chunkError.message}</StatusBanner>}

              <div className="chunk-panel">
                <div className="subheading">
                  <strong>Chunk プレビュー</strong>
                  {chunkLoading && <small>読み込み中…</small>}
                </div>
                {chunkData === null ? (
                  <div className="empty-block">
                    <p className="empty">Chunk データがまだないか、Backend が現在の状態を受け付けませんでした。</p>
                    <button type="button" className="secondary-button" onClick={() => void refreshSelectedDocument(selectedDocument.document_id)}>
                      再試行
                    </button>
                  </div>
                ) : chunkData.items.length === 0 ? (
                  <p className="empty">Chunk API は 0 件を返しました。</p>
                ) : (
                  <ol className="chunk-list">
                    {chunkData.items.slice(0, 3).map((chunk) => (
                      <li key={chunk.chunk_id}>
                        <div className="chunk-head">
                          <strong>#{chunk.chunk_index}</strong>
                          <small>{chunk.character_count} 文字</small>
                        </div>
                        <pre>{chunk.content}</pre>
                      </li>
                    ))}
                  </ol>
                )}
              </div>
            </>
          )}
        </section>
      </section>
      </section>

      <BusinessLearningPanel
        pageName="文書管理"
        purpose="登记关东地区饮料销售资料，并以 document_id、import_id 与 Chunk 为后续检索留下可追踪依据。"
        scenario="经营企划人员上传“関東飲料売上分析.md”，确认文档状态后执行 Import 和 Chunk，为 RAG検索准备内部资料。"
        prerequisites="准备 markdown 或 text 文件、标题、担当者和语言。Chunk 仅支持 validated 的 markdown／text；页面不自动把 document_id 传给 RAG検索。"
        relationship="本页产生 document_id、import_id 和 Chunk。RAG検索 使用已完成 Chunk 的内部资料，但当前只能由用户手动输入相同检索条件，未传递 document_id。"
        journey={{
          previous: "无，企业内部资料入口。",
          current: "1 / 4 文書管理",
          completion: "文档完成 Upload、Import、Chunk，且详情中存在可检索 Chunk。",
          next: "RAG検索",
          recommendedCase: "RAG-BIZ-001",
          transferredObjects: "document_id、Chunk",
          connection: "Backend 数据层自动连接；前端不自动传 document_id。",
        }}
        standardSop={{
          title: "标准操作流程：将企业资料准备为可检索 Chunk",
          scenarioFile: "docs/learning/sample-data/Scenario01_Sales_Decline/02_関東地域在庫レポート.md",
          summary: "只使用文件名与当前操作相关的摘要：这是 Scenario01 中用于确认关东饮料库存情况的内部资料。标准顺序是 Upload → Import → Chunk → RAG検索；Archive 不属于这条流程。",
          steps: [
            {
              title: "步骤 1：选择输入文档",
              purpose: "把将作为检索证据的企业资料交给文书页面。",
              prerequisite: "准备 Scenario01 的 markdown 或 text 文件。",
              input: "文件、タイトル、担当者、言語；tags 可选。",
              action: "选择文件；文件名会在标题为空时自动填入标题。确认「文書をアップロード」可点击。",
              api: "无；尚未发送请求。",
              backendResult: "无。按钮的可用性由前端确认 file、title、owner、language 均非空。",
              pageResult: "显示「選択済み」文件名。",
              technology: "HTML file input、React onChange、React useState、File API。",
              failureCheck: "检查是否未选文件，或标题、担当者、言語为空。",
              next: "点击上传。",
            },
            {
              title: "步骤 2：上传文档",
              purpose: "创建文档实体和可追溯的上传会话。",
              prerequisite: "步骤 1 的必填项完整。",
              input: "文件及 metadata JSON。",
              action: "点击「文書をアップロード」。",
              api: "uploadDocument() → POST /api/v1/documents（multipart/form-data：file、metadata）→ 201 Created。",
              backendResult: "返回 upload_id、document_id、上传会话 status=completed；新建文档实体的实际 status=uploaded。",
              pageResult: "显示上传成功信息，刷新列表，并以返回的 document_id 选中详情。",
              technology: "Event Handler、FormData、multipart/form-data、Fetch API、REST API、React useState、React Re-render。",
              failureCheck: "检查 missing_title、empty_file、unsupported_document_type、invalid_metadata 等 Backend error code。",
              next: "选择刚上传且 status=uploaded 的文档，执行 Import。",
            },
            {
              title: "步骤 3：执行 Import",
              purpose: "校验文档并将可导入文档推进到 Chunk 所需状态。",
              prerequisite: "文档存在、未 archived，状态为 uploaded 或 validated，且类型为 markdown/text/csv/json。",
              input: "当前选中的 document_id。",
              action: "点击「Import」。",
              api: "importDocument() → POST /api/v1/documents/{document_id}/import → 201 Created。",
              backendResult: "返回 import_id、status=completed；成功时文档状态更新为 validated。当前没有独立 validate 按钮，验证在 Import 内完成。",
              pageResult: "显示真实 Import 结果并刷新列表、详情。",
              technology: "React Event Handler、REST API、FastAPI Router、Service Layer、Repository Pattern、Backend Validation。",
              failureCheck: "archived 返回 409 document_archived；不支持类型返回 415 unsupported_document_type；不存在文档返回 404 document_not_found。",
              next: "确认详情 status=validated 后执行 Chunk。",
            },
            {
              title: "步骤 4：执行 Chunk",
              purpose: "把已验证的文档切分为 Keyword Retrieval 可读取的 Chunk。",
              prerequisite: "文档 status=validated、未 archived，且类型是 markdown 或 text。",
              input: "当前选中的 document_id。",
              action: "点击「Chunk実行」。",
              api: "chunkDocument() → POST /api/v1/documents/{document_id}/chunks → 201 Created。",
              backendResult: "返回 document_id、version、items；每项包含 chunk_id、chunk_index、content、character_count 与 metadata。",
              pageResult: "Chunk 数大于 0，详情显示数量并可查看 Chunk 内容；不再出现 document_not_validated 等前置条件错误。",
              technology: "Document Processing、Text Chunking、REST API、Service Layer、Repository Pattern。",
              failureCheck: "uploaded 等非 validated 状态返回 409 document_not_validated；archived 返回 409 document_archived；非 markdown/text 返回 415 unsupported_document_type。",
              next: "进入 RAG検索，使用与该资料内容直接相关的问题。",
            },
            {
              title: "步骤 5：进入 RAG検索",
              purpose: "验证资料已经成为可检索证据，而不是只停留在上传列表。",
              prerequisite: "Upload 会话 completed、文档已 Import 为 validated，且 Chunk items 已生成。",
              input: "从 Scenario01 的 07_RAG質問集.md 选择与库存报告直接相关的问题。",
              action: "进入 RAG検索，执行 RAG-BIZ-001。",
              api: "POST /api/v1/document-retrieval/search 或 POST /api/v1/internal-rag/answer。",
              backendResult: "Keyword Retrieval 返回当前文档的 Chunk；Internal RAG 仅在证据足够时返回 answer 与 citations。",
              pageResult: "确认 document_id、chunk_id、score 或 citation 与已准备资料一致。",
              technology: "Keyword Retrieval、Deterministic RAG、Fetch API、REST API。",
              failureCheck: "若没有结果，先确认步骤 4 的 Chunk 是否成功，以及 query 是否与资料内容匹配。",
              next: "继续 RAG-BIZ-001，再手动整理结论进入分析依頼。",
            },
          ],
        }}
        cases={[
          { id: "DOC-BIZ-001", group: "标准业务 Case", purpose: "完整标准流程：把库存报告准备为可检索 Chunk。", input: "02_関東地域在庫レポート.md。", steps: ["选择文件并填写必填 metadata。", "Upload 后确认 201、upload_id、document_id、上传会话 completed 与文档 uploaded。", "Import 后确认 201、import_id=imp-*、import status=completed 与文档 validated。", "Chunk 后确认 201、items 数量大于 0 与 chunk_id。", "进入 RAG検索 执行 RAG-BIZ-001。"], expected: "顺序固定为 Upload → Import → Chunk → RAG検索；不执行 Archive。" },
          { id: "DOC-BIZ-002", group: "异常与维护测试 Case", purpose: "输入校验。", input: "未选择文件，或清空タイトル／担当者／言語。", expected: "「文書をアップロード」不可点击；若绕过前端校验，页面显示 Backend 的真实 validation error。" },
          { id: "DOC-BIZ-003", group: "异常与维护测试 Case", purpose: "前置条件校验。", input: "对 uploaded 文档直接执行 Chunk；或对 archived 文档执行 Import／Chunk。", expected: "Chunk 对未 validated 文档返回 409 document_not_validated；archived 的 Import／Chunk 返回 409 document_archived。" },
          { id: "DOC-BIZ-004", group: "异常与维护测试 Case", purpose: "不存在数据。", input: "读取或操作不存在的 document_id。", expected: "GET / POST / DELETE 的目标不存在时返回 404 document_not_found，页面显示结构化错误。" },
          { id: "DOC-BIZ-005", group: "异常与维护测试 Case", purpose: "Archive 维护场景，不是标准上传流程。", input: "旧版库存报告已被新版替换：选择旧文档，点击「アーカイブ」，再勾选「アーカイブ済みを含める」。", steps: ["确认 DELETE /api/v1/documents/{document_id} 返回 202 与 status=archived。", "默认 include_archived=false 的列表不再显示该文档。", "勾选后以 include_archived=true 重新读取，归档文档重新出现。", "确认默认 RAG 检索排除 archived；只有 request.include_archived=true 才包含它。"], expected: "Archive 只用于过期、错误或被新版替换的资料维护；归档后不能再 Import 或 Chunk。" },
        ]}
        flows={[
          {
            title: "上传、列表与详情",
            api: "POST /api/v1/documents；GET /api/v1/documents；GET /api/v1/documents/{document_id}",
            frontend: ["DocumentsPage submitUpload() / loadDocuments() / refreshSelectedDocument()", "uploadDocument() / listDocuments() / getDocument()", "setDocuments / setSelectedDocument"],
            backend: ["documents.py upload_document() / list_documents() / get_document()", "DocumentUploadService.upload_document()", "DocumentReadService.list_documents() / get_document()", "InMemoryDocumentRepository.create() / list_all() / get()"],
          },
          {
            title: "Import、Chunk 与归档",
            api: "POST /api/v1/documents/{document_id}/import；POST|GET /api/v1/documents/{document_id}/chunks；DELETE /api/v1/documents/{document_id}",
            frontend: ["runDocumentAction()", "importDocument() / chunkDocument() / archiveDocument() / getDocumentChunks()", "刷新列表、详情和 Chunk 预览"],
            backend: ["document_imports.py import_document() → DocumentImportService.import_document()", "document_chunks.py chunk_document() / get_document_chunks() → DocumentChunkService", "documents.py archive_document() → DocumentArchiveService.archive_document()", "InMemoryDocumentRepository.get() / update()；InMemoryDocumentChunkRepository.replace_for_document() / list_for_document()"],
            note: "「詳細を再読み込み」只更新 React 数据状态并重新发起 GET；不是新的业务流程。",
          },
        ]}
      />
    </>
  );
}

function parseTags(raw: string): string[] {
  return raw
    .split(",")
    .map((item) => item.trim())
    .filter((item) => item.length > 0);
}

function formatDate(value: string): string {
  return new Date(value).toLocaleString("ja-JP");
}
