package com.jtspringproject.JtSpringProject.common.constants;

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
