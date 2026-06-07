package com.victorkure.ragclient.dto;

public record HealthResponse(
    String status,
    String docsDir,
    int chunkCount
) {
}
