package com.victorkure.ragclient.dto;

import java.util.List;

public record RootResponse(
    String service,
    String status,
    String message,
    List<String> endpoints
) {
}
