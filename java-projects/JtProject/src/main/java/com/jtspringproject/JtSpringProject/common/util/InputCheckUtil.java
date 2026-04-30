package com.jtspringproject.JtSpringProject.common.util;

import java.util.Collection;

/**
 * 输入校验工具类。
 *
 * <p>提供字符串空白判断、去空白转换和集合非空判断等通用方法，供 Controller、Service 和 DAO
 * 层在参数校验时复用。</p>
 */
public final class InputCheckUtil {

    private InputCheckUtil() {
    }

    public static boolean isBlank(String value) {
        return value == null || value.trim().isEmpty();
    }

    public static boolean hasText(String value) {
        return !isBlank(value);
    }

    public static String trimToNull(String value) {
        if (value == null) {
            return null;
        }
        String trimmed = value.trim();
        return trimmed.isEmpty() ? null : trimmed;
    }

    public static String trimToEmpty(String value) {
        return value == null ? "" : value.trim();
    }

    public static boolean hasItems(Collection<?> values) {
        return values != null && !values.isEmpty();
    }
}
