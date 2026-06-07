package com.victorkure.ragclient.dto;

public record ReloadResponse(
    String docsDir,
    int chunkCount
) {
}
