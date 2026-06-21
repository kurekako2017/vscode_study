package com.victorkure.ragclient.dto;

// 重载接口完成后返回新的文档目录和 chunk 数量。
public record ReloadResponse(
    String docsDir,
    int chunkCount
) {
}
