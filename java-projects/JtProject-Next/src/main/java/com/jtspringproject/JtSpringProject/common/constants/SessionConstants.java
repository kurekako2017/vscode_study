package com.jtspringproject.JtSpringProject.common.constants;

/**
 * Session 键名常量。
 *
 * <p>统一管理登录状态、用户名和购物车提示等 Session 属性名，避免硬编码字符串分散在控制器中。</p>
 */
public final class SessionConstants {

    public static final String USERNAME = "username";
    public static final String USER_ROLE = "userRole";
    public static final String ADMIN_LOGGED_IN = "adminLoggedIn";
    public static final String ADMIN_USERNAME = "adminUsername";
    public static final String CART_MESSAGE = "cartMsg";

    private SessionConstants() {
    }
}
