/**
 * 前端只读权限镜像。
 *
 * 谁调用它：AuthContext、ProtectedRoute、App 导航和业务按钮。
 * 输入：Backend `/users/me` 返回的 role 与页面要求的 Permission。
 * 输出：稳定权限集合和 fail-closed 判断结果。
 * 设计理由：JWT 只保存身份；权限仍由集中注册表按 role 推导，避免页面散落 role 字符串。
 * 日本现场面试：前端 RBAC 只负责 UX，真正授权仍由 Backend `require_permission()` 执行。
 */
export const PERMISSIONS = [
  "documents.read",
  "documents.write",
  "documents.archive",
  "retrieval.query",
  "analysis.execute",
  "approval.submit",
  "approval.review",
  "approval.admin",
  "audit.read",
  "security.manage",
] as const;

export type Permission = (typeof PERMISSIONS)[number];
export type Role = "admin" | "manager" | "employee";

export const ROLE_PERMISSIONS: Readonly<Record<Role, readonly Permission[]>> = Object.freeze({
  admin: Object.freeze([...PERMISSIONS]) as readonly Permission[],
  manager: Object.freeze([
    "documents.read",
    "documents.write",
    "documents.archive",
    "retrieval.query",
    "analysis.execute",
    "approval.submit",
    "approval.review",
    "approval.admin",
    "audit.read",
  ]) as readonly Permission[],
  employee: Object.freeze([
    "documents.read",
    "documents.write",
    "retrieval.query",
    "analysis.execute",
    "approval.submit",
  ]) as readonly Permission[],
});

/** 未知角色返回空集合，不能因为前端字符串异常而获得默认权限。 */
export function getPermissionsForRole(role: string): readonly Permission[] {
  if (role === "admin" || role === "manager" || role === "employee") {
    return ROLE_PERMISSIONS[role];
  }
  return [];
}

export function hasPermission(permissions: readonly Permission[], permission: Permission): boolean {
  return permissions.includes(permission);
}

export function hasAnyPermission(
  permissions: readonly Permission[],
  required: readonly Permission[],
): boolean {
  return required.some((permission) => permissions.includes(permission));
}

export function hasAllPermissions(
  permissions: readonly Permission[],
  required: readonly Permission[],
): boolean {
  return required.every((permission) => permissions.includes(permission));
}
