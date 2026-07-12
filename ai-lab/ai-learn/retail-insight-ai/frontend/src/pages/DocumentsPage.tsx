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
      showBanner(`Upload completed: ${session.document_id}`);
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
        showBanner(`Archive accepted: ${result.document_id} (${result.status})`);
      }
      if (action === "import") {
        const result = await importDocument(selectedDocument.document_id);
        showBanner(`Import result: ${result.status}`);
      }
      if (action === "chunk") {
        const result = await chunkDocument(selectedDocument.document_id);
        showBanner(`Chunk completed: ${result.items.length} chunks`);
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
        eyebrow="DOCUMENT WORKSPACE"
        title="Documents"
        description="Manage document upload, detail, archive, import, and chunk actions through the current backend contract without inventing local-only data."
      />

      <section className="documents-shell" aria-label="文档管理页面">
        <aside className="panel upload-panel">
        <div className="panel-heading">
          <span>01</span>
          <h2>Document Upload</h2>
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
          {uploadFile && <p className="selection">Selected: {uploadFile.name}</p>}

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

          <label htmlFor="upload-owner">Owner</label>
          <input id="upload-owner" value={uploadOwner} onChange={(event) => setUploadOwner(event.target.value)} disabled={uploading} />

          <label htmlFor="upload-language">Language</label>
          <input
            id="upload-language"
            value={uploadLanguage}
            onChange={(event) => setUploadLanguage(event.target.value)}
            disabled={uploading}
          />

          <label htmlFor="upload-tags">Tags (comma separated)</label>
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
            {uploading ? "アップロード中…" : "Upload Document"}
          </button>
          {uploadError && <StatusBanner tone="error">[{uploadError.code}] {uploadError.message}</StatusBanner>}
        </form>
        </aside>

        <section className="documents-main">
        <section className="panel list-panel" aria-live="polite">
          <div className="panel-heading">
            <span>02</span>
            <h2>Document List</h2>
            <small>{documentsRefreshing ? "refreshing" : `${documents.length} items`}</small>
          </div>

          <div className="toolbar">
            <label className="checkbox-row">
              <input type="checkbox" checked={showArchived} onChange={(event) => setShowArchived(event.target.checked)} />
              Include archived
            </label>
            <button type="button" className="secondary-button" onClick={() => void loadDocuments(false)}>
              Retry / Refresh
            </button>
          </div>

          {bannerMessage && <StatusBanner tone="success">{bannerMessage}</StatusBanner>}
          {documentsError && <StatusBanner tone="error">[{documentsError.code}] {documentsError.message}</StatusBanner>}

          {documentsLoading ? (
            <p className="empty">Loading documents…</p>
          ) : documents.length === 0 ? (
            <p className="empty">No documents yet. Upload a file to start the document workflow.</p>
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
            <h2>Document Detail</h2>
            {selectedDocument && <small>{selectedDocument.document_id}</small>}
          </div>

          {detailError && <StatusBanner tone="error">[{detailError.code}] {detailError.message}</StatusBanner>}

          {selectedDocumentId === null ? (
            <p className="empty">Select a document from the list to view detail and actions.</p>
          ) : detailLoading && selectedDocument === null ? (
            <p className="empty">Loading document detail…</p>
          ) : selectedDocument === null ? (
            <div className="empty-block">
              <p className="empty">Document detail is unavailable.</p>
              <button type="button" className="secondary-button" onClick={() => void refreshSelectedDocument(selectedDocumentId)}>
                Retry
              </button>
            </div>
          ) : (
            <>
              <dl className="detail-grid">
                <div><dt>Title</dt><dd>{selectedDocument.title}</dd></div>
                <div><dt>Status</dt><dd>{selectedDocument.status}</dd></div>
                <div><dt>Type</dt><dd>{selectedDocument.document_type}</dd></div>
                <div><dt>Language</dt><dd>{selectedDocument.language}</dd></div>
                <div><dt>Owner</dt><dd>{selectedDocument.owner}</dd></div>
                <div><dt>Version</dt><dd>{selectedDocument.version}</dd></div>
                <div><dt>Created</dt><dd>{formatDate(selectedDocument.created_at)}</dd></div>
                <div><dt>Updated</dt><dd>{formatDate(selectedDocument.updated_at)}</dd></div>
                <div><dt>Chunk Count</dt><dd>{chunkData ? chunkData.items.length : chunkLoading ? "Loading…" : "—"}</dd></div>
                <div><dt>Tags</dt><dd>{selectedDocument.tags.length > 0 ? selectedDocument.tags.join(", ") : "—"}</dd></div>
              </dl>

              {selectedDocument.description && (
                <div className="detail-note">
                  <strong>Description</strong>
                  <p>{selectedDocument.description}</p>
                </div>
              )}

              <div className="action-grid">
                <button type="button" disabled={selectedDocumentBusy} onClick={() => void runDocumentAction("archive")}>
                  {activeDocumentAction === "archive" ? "Archiving…" : "Archive"}
                </button>
                <button type="button" disabled={selectedDocumentBusy} onClick={() => void runDocumentAction("import")}>
                  {activeDocumentAction === "import" ? "Importing…" : "Import"}
                </button>
                <button type="button" disabled={selectedDocumentBusy} onClick={() => void runDocumentAction("chunk")}>
                  {activeDocumentAction === "chunk" ? "Chunking…" : "Chunk"}
                </button>
                <button
                  type="button"
                  className="secondary-button"
                  disabled={selectedDocumentBusy}
                  onClick={() => void refreshSelectedDocument(selectedDocument.document_id)}
                >
                  Reload Detail
                </button>
              </div>

              {chunkError && <StatusBanner tone="error">[{chunkError.code}] {chunkError.message}</StatusBanner>}

              <div className="chunk-panel">
                <div className="subheading">
                  <strong>Chunk Preview</strong>
                  {chunkLoading && <small>loading…</small>}
                </div>
                {chunkData === null ? (
                  <div className="empty-block">
                    <p className="empty">No chunk data yet, or the backend rejected the current state.</p>
                    <button type="button" className="secondary-button" onClick={() => void refreshSelectedDocument(selectedDocument.document_id)}>
                      Retry
                    </button>
                  </div>
                ) : chunkData.items.length === 0 ? (
                  <p className="empty">Chunk API returned zero items.</p>
                ) : (
                  <ol className="chunk-list">
                    {chunkData.items.slice(0, 3).map((chunk) => (
                      <li key={chunk.chunk_id}>
                        <div className="chunk-head">
                          <strong>#{chunk.chunk_index}</strong>
                          <small>{chunk.character_count} chars</small>
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
