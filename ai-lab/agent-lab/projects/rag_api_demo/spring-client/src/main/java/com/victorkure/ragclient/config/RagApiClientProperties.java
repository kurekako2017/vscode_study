package com.victorkure.ragclient.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "rag.api")
public record RagApiClientProperties(String baseUrl) {
}
