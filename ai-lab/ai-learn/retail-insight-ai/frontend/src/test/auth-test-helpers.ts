import type { AuthSession, CurrentUser } from "../auth/AuthContext";
import { getPermissionsForRole } from "../auth/permissions";

function encodeBase64Url(value: object): string {
  return btoa(JSON.stringify(value))
    .replaceAll("+", "-")
    .replaceAll("/", "_")
    .replaceAll("=", "");
}

/** 测试 Token 只验证前端 payload 合同，不用于模拟后端签名安全。 */
export function buildTestJwt(
  role: string,
  username = role,
  userId = `user-${role}`,
  expiresAt = Math.floor(Date.now() / 1000) + 1800,
): string {
  return [
    encodeBase64Url({ alg: "HS256", typ: "JWT" }),
    encodeBase64Url({
      sub: userId,
      user_id: userId,
      username,
      role,
      iat: expiresAt - 1800,
      exp: expiresAt,
      jti: `jti-${role}`,
    }),
    "test-signature",
  ].join(".");
}

export function buildTestUser(role: string, username = role, userId = `user-${role}`): CurrentUser {
  return {
    user_id: userId,
    username,
    role,
    permissions: getPermissionsForRole(role),
  };
}

/** accessToken=null 让既有页面测试继续使用可控 FakeEventSource，不代表生产会话形态。 */
export function buildTestSession(role: string): AuthSession {
  return {
    accessToken: null,
    currentUser: buildTestUser(role),
  };
}

export const ADMIN_SESSION = buildTestSession("admin");
export const MANAGER_SESSION = buildTestSession("manager");
export const EMPLOYEE_SESSION = buildTestSession("employee");
