package com.jtspringproject.JtSpringProject.common.constants;

/**
 * 角色常量。
 *
 * <p>集中定义普通用户和管理员角色标识，并提供简单的角色判定方法。</p>
 */
public final class RoleConstants {

    public static final String ROLE_NORMAL = "ROLE_NORMAL";
    public static final String ROLE_ADMIN = "ROLE_ADMIN";

    private RoleConstants() {
    }

    public static boolean isAdmin(String role) {
        return ROLE_ADMIN.equals(role);
    }

    public static boolean isNormalUser(String role) {
        return ROLE_NORMAL.equals(role);
    }
}
