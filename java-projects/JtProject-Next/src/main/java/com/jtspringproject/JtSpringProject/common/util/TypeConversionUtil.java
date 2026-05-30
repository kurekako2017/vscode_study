package com.jtspringproject.JtSpringProject.common.util;

/**
 * 类型转换工具类。
 *
 * <p>用于将请求参数、Session 值等字符串安全转换为常用类型，避免在控制器中散落重复的解析代码。</p>
 */
public final class TypeConversionUtil {

    private TypeConversionUtil() {
    }

    public static String toTrimmedString(Object value) {
        return value == null ? null : InputCheckUtil.trimToNull(String.valueOf(value));
    }

    public static int toInt(String value, int defaultValue) {
        if (InputCheckUtil.isBlank(value)) {
            return defaultValue;
        }
        try {
            return Integer.parseInt(value.trim());
        } catch (NumberFormatException e) {
            return defaultValue;
        }
    }

    public static Integer toNullableInt(String value) {
        if (InputCheckUtil.isBlank(value)) {
            return null;
        }
        try {
            return Integer.valueOf(value.trim());
        } catch (NumberFormatException e) {
            return null;
        }
    }
}
