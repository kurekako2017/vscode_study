package com.victorkure.ragclient.dto;

// 健康检查返回当前文档目录和已建立索引的 chunk 数量。
public record HealthResponse(
    String status,
    String docsDir,
    int chunkCount
) {
}
