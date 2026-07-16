/**
 * Access Token 的浏览器端最小结构校验。
 *
 * 这里不验证 JWT 签名；签名和账号有效性必须由 Backend `/users/me` 最终确认。
 * 前端只用它提前拒绝过期、缺字段或明显损坏的会话，且绝不读取 permissions。
 */
export interface JwtIdentityClaims {
  sub: string;
  user_id: string;
  username: string;
  role: string;
  iat: number;
  exp: number;
  jti: string;
}

function decodeBase64Url(value: string): string {
  const base64 = value.replaceAll("-", "+").replaceAll("_", "/");
  const padded = base64.padEnd(Math.ceil(base64.length / 4) * 4, "=");
  return decodeURIComponent(
    Array.from(atob(padded))
      .map((character) => `%${character.charCodeAt(0).toString(16).padStart(2, "0")}`)
      .join(""),
  );
}

function isNonEmptyString(value: unknown): value is string {
  return typeof value === "string" && value.trim().length > 0;
}

/** 返回 null 表示 Token 不完整、已过期或不符合冻结 JWT 身份合同。 */
export function parseJwtIdentity(
  token: string,
  nowSeconds = Math.floor(Date.now() / 1000),
): JwtIdentityClaims | null {
  const parts = token.split(".");
  if (parts.length !== 3 || parts.some((part) => part.length === 0)) return null;

  try {
    const payload = JSON.parse(decodeBase64Url(parts[1])) as Record<string, unknown>;
    if (
      !isNonEmptyString(payload.sub)
      || !isNonEmptyString(payload.user_id)
      || !isNonEmptyString(payload.username)
      || !isNonEmptyString(payload.role)
      || !isNonEmptyString(payload.jti)
      || typeof payload.iat !== "number"
      || typeof payload.exp !== "number"
      || payload.sub !== payload.user_id
      || payload.exp <= payload.iat
      || payload.exp <= nowSeconds
    ) {
      return null;
    }
    return payload as unknown as JwtIdentityClaims;
  } catch {
    return null;
  }
}
