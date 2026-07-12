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

const defaultOwner = "analysis-team";
type DocumentAction = "archive" | "import" | "chunk" | null;

/**
 * DocumentsPage 负责上传、列表、详情和文档状态操作。
 *
 * 为什么独立成页：
 * - 这一页的状态已经和 Tasks 页面没有直接耦合，拆开后更便于继续扩展 RAG / Approval。
 */
export function DocumentsPage() {
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
    } catch (reason) {
      setUploadError(toDisplayError(reason, "DOCUMENT_UPLOAD_ERROR", "ドキュメントのアップロードに失敗しました"));
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
      }
      if (action === "import") {
        const result = await importDocument(selectedDocument.document_id);
        showBanner(`Import 結果: ${result.status}`);
      }
      if (action === "chunk") {
        const result = await chunkDocument(selectedDocument.document_id);
        showBanner(`Chunk 処理が完了しました: ${result.items.length} 件`);
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
    } finally {
      setActiveDocumentAction(null);
    }
  }

  const selectedDocumentBusy = activeDocumentAction !== null;

  return (
    <>
      <PageHeader
        eyebrow="文書ワークスペース"
        title="文書管理"
        description="現在の Backend API を使用して、文書のアップロード、詳細確認、アーカイブ、Import、Chunk 操作を行います。"
      />

      <section className="documents-shell" aria-label="文档管理页面">
        <aside className="panel upload-panel">
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
        </aside>

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
                <div><dt>タグ</dt><dd>{selectedDocument.tags.length > 0 ? selectedDocument.tags.join(", ") : "—"}</dd></div>
              </dl>

              {selectedDocument.description && (
                <div className="detail-note">
                  <strong>説明</strong>
                  <p>{selectedDocument.description}</p>
                </div>
              )}

              <div className="action-grid">
                <button type="button" disabled={selectedDocumentBusy} onClick={() => void runDocumentAction("archive")}>
                  {activeDocumentAction === "archive" ? "アーカイブ中…" : "アーカイブ"}
                </button>
                <button type="button" disabled={selectedDocumentBusy} onClick={() => void runDocumentAction("import")}>
                  {activeDocumentAction === "import" ? "Import 中…" : "Import"}
                </button>
                <button type="button" disabled={selectedDocumentBusy} onClick={() => void runDocumentAction("chunk")}>
                  {activeDocumentAction === "chunk" ? "Chunk 処理中…" : "Chunk 実行"}
                </button>
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
        cases={[
          { id: "DOC-BIZ-001", purpose: "正常登记关东饮料销售资料。", input: "选择文件、填写タイトル／担当者／言語，点击「文書をアップロード」。", expected: "实际 POST 返回 upload_id、document_id、status；列表刷新并选中该文档。" },
          { id: "DOC-BIZ-002", purpose: "确认上传必填项。", input: "不选择文件，或清空タイトル／担当者／言語。", expected: "上传按钮不可点击；Backend 返回的校验错误会显示在页面。" },
          { id: "DOC-BIZ-003", purpose: "确认不存在文档。", input: "选择已不存在的 document_id 或刷新详情。", expected: "GET 文档／Chunk 接口实际返回 404，页面显示结构化错误并允许再试。" },
          { id: "DOC-BIZ-004", purpose: "确认 Import 与 Chunk 的业务前置条件。", input: "对文档点击 Import、Chunk。", expected: "Import 返回真实 import_id／status；Chunk 对非 validated、archived 或不支持类型返回 Backend 业务错误。" },
          { id: "DOC-BIZ-005", purpose: "确认归档和重新读取。", input: "点击「アーカイブ」，然后勾选「アーカイブ済みを含める」。", expected: "DELETE 返回 202 与 archived 状态；列表与详情刷新，查询条件只改变页面读取结果。" },
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
