package com.victorkure.ragclient.dto;

import java.util.List;

// 对应 FastAPI /ask 的 JSON 响应，字段名由 Spring 的 JSON 映射自动转换。
public record AskResponse(
    String answer,
    String model,
    String docsDir,
    int sourceCount,
    List<SourceItem> sources
) {
}
