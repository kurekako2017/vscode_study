// ChatComposer 是当前主页面底部的输入区。
// 它负责三件事：输入任务、选择附件、发送或取消任务。
import {
  PaperClipOutlined,
  PlusOutlined,
  SendOutlined,
  StopOutlined
} from "@ant-design/icons";
import { Button, Tooltip, Upload } from "antd";
import type { UploadFile } from "antd";
import type { UploadedItem } from "../types";

interface ChatComposerProps {
  isCancelling: boolean;
  isRunning: boolean;
  isUploading: boolean;
  onNewSession: () => void;
  onCancel: () => void;
  onQueryChange: (value: string) => void;
  onSubmit: () => void;
  onUpload: (items: UploadedItem[]) => Promise<void> | void;
  query: string;
  stagedItems: UploadedItem[];
  uploadedItems: UploadedItem[];
  onStagedItemsChange: (items: UploadedItem[]) => void;
}

function toUploadedItem(file: UploadFile): UploadedItem | null {
  // Ant Design Upload 返回的是 UploadFile；
  // 这里把它转成项目内部统一使用的 UploadedItem。
  if (!file.originFileObj) {
    return null;
  }

  return {
    uid: file.uid,
    name: file.name,
    size: file.size || 0,
    raw: file.originFileObj
  };
}

function uniqueUploadedItems(items: UploadedItem[]): UploadedItem[] {
  // 用文件名做一次轻量去重，避免同一批次里重复显示同名附件。
  const names = new Set<string>();
  return items.filter((item) => {
    if (names.has(item.name)) {
      return false;
    }
    names.add(item.name);
    return true;
  });
}

export function ChatComposer({
  isCancelling,
  isRunning,
  isUploading,
  onCancel,
  onNewSession,
  onQueryChange,
  onStagedItemsChange,
  onSubmit,
  onUpload,
  query,
  stagedItems,
  uploadedItems
}: ChatComposerProps) {
  const hasStagedFiles = stagedItems.length > 0;
  const canSubmit = query.trim().length > 0;

  function handleAttachmentChange(fileList: UploadFile[]) {
    // 这个组件选择完文件后会立即触发上传，
    // 所以 stagedItems 更像“上传前的一瞬间缓存”。
    const nextItems = uniqueUploadedItems(
      fileList
        .map(toUploadedItem)
        .filter((item): item is UploadedItem => Boolean(item))
    );

    if (nextItems.length === 0) {
      return;
    }

    onStagedItemsChange(nextItems);
    void Promise.resolve(onUpload(nextItems)).finally(() => {
      onStagedItemsChange([]);
    });
  }

  return (
    <section className="chat-composer" aria-label="发送研搜任务">
      {uploadedItems.length > 0 ? (
        <div className="attachment-strip" aria-label="当前会话附件">
          {uploadedItems.map((item) => (
            <span className="attachment-pill" key={`${item.uid}-${item.name}`}>
              <PaperClipOutlined aria-hidden />
              {item.name}
            </span>
          ))}
        </div>
      ) : null}

      {hasStagedFiles ? (
        <div className="attachment-strip" aria-label="待上传附件">
          {stagedItems.map((item) => (
            <span className="attachment-pill attachment-pill--pending" key={item.uid}>
              <PaperClipOutlined aria-hidden />
              {item.name}
            </span>
          ))}
          {isUploading ? <span className="attachment-uploading">附着中...</span> : null}
        </div>
      ) : null}

      <div className="composer-shell">
        <textarea
          aria-label="研搜任务"
          disabled={isRunning}
          onChange={(event) => onQueryChange(event.target.value)}
          onKeyDown={(event) => {
            // Enter 直接发送；Shift + Enter 才换行。
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              onSubmit();
            }
          }}
          placeholder="向 DeepSearch Agents 发送任务..."
          value={query}
        />

        <div className="composer-toolbar">
          <div className="composer-left-actions">
            <Tooltip title="新建会话">
              <Button
                aria-label="新建会话"
                className="composer-icon-button"
                icon={<PlusOutlined />}
                onClick={onNewSession}
                shape="circle"
              />
            </Tooltip>
            <Upload
              beforeUpload={() => false}
              fileList={[]}
              multiple
              onChange={(info) => {
                // antd 在只选一个文件时，info.fileList 可能为空，
                // 所以这里补一个 [info.file] 的兜底。
                handleAttachmentChange(info.fileList.length > 0 ? info.fileList : [info.file]);
              }}
              showUploadList={false}
            >
              <Tooltip title="选择附件">
                <Button
                  aria-label="选择附件"
                  className="composer-icon-button"
                  disabled={isRunning || isUploading}
                  icon={<PaperClipOutlined />}
                  shape="circle"
                />
              </Tooltip>
            </Upload>
          </div>

          <Tooltip title={isRunning ? "取消当前任务" : "发送任务"}>
            <Button
              aria-label={isRunning ? "取消当前任务" : "发送任务"}
              className={isRunning ? "send-button send-button--cancel" : "send-button"}
              disabled={isRunning ? isCancelling : !canSubmit}
              icon={isRunning ? <StopOutlined /> : <SendOutlined />}
              loading={isCancelling}
              onClick={isRunning ? onCancel : onSubmit}
              shape="circle"
              type="primary"
            />
          </Tooltip>
        </div>
      </div>
    </section>
  );
}
