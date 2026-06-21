package com.victorkure.ragclient.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "rag.api")
// 把 application.yml 中的 rag.api.base-url 映射为类型安全的 Java 配置。
public record RagApiClientProperties(String baseUrl) {
}
