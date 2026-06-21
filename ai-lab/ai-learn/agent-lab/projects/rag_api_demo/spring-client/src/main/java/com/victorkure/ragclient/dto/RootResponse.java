package com.victorkure.ragclient.dto;

import java.util.List;

// 根接口用于说明后端服务状态和可用端点，不包含模型回答。
public record RootResponse(
    String service,
    String status,
    String message,
    List<String> endpoints
) {
}
