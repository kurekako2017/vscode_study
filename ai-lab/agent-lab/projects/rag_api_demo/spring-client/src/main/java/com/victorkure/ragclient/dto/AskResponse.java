package com.victorkure.ragclient.dto;

import java.util.List;

public record AskResponse(
    String answer,
    String model,
    String docsDir,
    int sourceCount,
    List<SourceItem> sources
) {
}
