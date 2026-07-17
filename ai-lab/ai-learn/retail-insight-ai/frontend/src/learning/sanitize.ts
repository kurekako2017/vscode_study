/** 学习 Trace 脱敏：禁止显示 Token、Password、API Key、完整正文。 */

const SENSITIVE_KEY = /access[_-]?token|password|authorization|cookie|api[_-]?key|secret|bearer|prompt|refresh[_-]?token/i;

export function isSensitiveKey(key: string): boolean {
  return SENSITIVE_KEY.test(key);
}

export function redactValue(key: string, value: unknown): string {
  if (isSensitiveKey(key)) return "[REDACTED]";
  if (value === null || value === undefined) return String(value);
  if (typeof value === "boolean" || typeof value === "number") return String(value);
  if (typeof value === "string") {
    if (value.length > 80) return `${value.slice(0, 40)}…(${value.length} chars)`;
    if (/^Bearer\s+/i.test(value)) return "[REDACTED Bearer]";
    return value;
  }
  if (Array.isArray(value)) return `Array(${value.length})`;
  if (typeof value === "object") {
    const keys = Object.keys(value as object);
    return `Object{${keys.slice(0, 6).join(", ")}${keys.length > 6 ? ", …" : ""}}`;
  }
  return typeof value;
}

export function safeSummary(value: unknown, keyHint = "value"): string {
  return redactValue(keyHint, value);
}

export function sanitizeRecord(input: Record<string, unknown> | undefined): Record<string, string | number | boolean | null> {
  if (!input) return {};
  const out: Record<string, string | number | boolean | null> = {};
  for (const [key, value] of Object.entries(input)) {
    if (isSensitiveKey(key)) {
      out[key] = "[REDACTED]";
      continue;
    }
    if (value === null || typeof value === "boolean" || typeof value === "number") {
      out[key] = value as boolean | number | null;
    } else {
      out[key] = redactValue(key, value);
    }
  }
  return out;
}
