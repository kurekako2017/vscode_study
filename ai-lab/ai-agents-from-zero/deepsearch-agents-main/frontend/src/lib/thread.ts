// 这个文件负责管理前端会话 ID（thread_id）。
// 后端把它当作“当前任务会话的唯一标识”，所以前端需要稳定保存它。
const STORAGE_KEY = "deepsearch.thread_id";

export function createThreadId(): string {
  // 优先用浏览器原生 randomUUID；老环境没有时再降级到时间戳方案。
  if (crypto.randomUUID) {
    return crypto.randomUUID();
  }

  return `manual-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

export function getStoredThreadId(): string {
  // 页面刷新后，仍然尽量复用之前的会话 ID，
  // 这样同一个会话的文件和事件流还能对应上。
  const existing = window.localStorage.getItem(STORAGE_KEY);
  if (existing) {
    return existing;
  }

  const threadId = createThreadId();
  window.localStorage.setItem(STORAGE_KEY, threadId);
  return threadId;
}

export function storeThreadId(threadId: string): void {
  window.localStorage.setItem(STORAGE_KEY, threadId);
}
