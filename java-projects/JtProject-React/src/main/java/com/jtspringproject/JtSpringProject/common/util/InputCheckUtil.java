package com.jtspringproject.JtSpringProject.common.util;

import java.util.Collection;

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
