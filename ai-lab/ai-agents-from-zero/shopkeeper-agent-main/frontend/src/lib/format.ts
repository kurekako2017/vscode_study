/**
 * 通用格式化工具
 * 提供 className 合并、时间格式化和查询结果文本化等通用工具函数
 */
export function cn(...classes: Array<string | false | null | undefined>) {
  // 只保留真实存在的 className，再拼成最终字符串。
  return classes.filter(Boolean).join(" ");
}

export function formatTime(timestamp: number) {
  // 把毫秒时间戳格式化成用户更容易读懂的“时:分”。
  return new Intl.DateTimeFormat("zh-CN", {
    hour: "2-digit",
    minute: "2-digit",
  }).format(timestamp);
}

export function summarizeResult(data: unknown) {
  // 结果展示优先给出简短总结，避免前端一上来就把整份 JSON 全塞给用户。
  if (Array.isArray(data)) {
    return data.length > 0 ? `查询完成，共 ${data.length} 行结果。` : "查询完成，结果为空。";
  }

  if (data && typeof data === "object") {
    return "查询完成，已返回结构化结果。";
  }

  if (data === null || data === undefined || data === "") {
    return "查询完成，结果为空。";
  }

  return `查询完成：${String(data)}`;
}

export function toClipboardText(value: unknown) {
  // 复制到剪贴板时，把对象转成格式化 JSON，便于后续粘贴查看。
  if (typeof value === "string") return value;
  return JSON.stringify(value, null, 2);
}
