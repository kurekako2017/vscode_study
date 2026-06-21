package com.victorkure.ragclient.service;

import com.victorkure.ragclient.dto.AskRequest;
import com.victorkure.ragclient.dto.AskResponse;
import com.victorkure.ragclient.dto.HealthResponse;
import com.victorkure.ragclient.dto.ReloadResponse;
import com.victorkure.ragclient.dto.RootResponse;
import com.victorkure.ragclient.config.RagApiClientProperties;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class RagApiClientService {

    // Service 层只负责访问后端，不包含 Controller 的 HTTP 入参处理逻辑。

    private final RestTemplate restTemplate;
    private final RagApiClientProperties properties;

    public RagApiClientService(RestTemplate ragApiRestTemplate, RagApiClientProperties properties) {
        this.restTemplate = ragApiRestTemplate;
        this.properties = properties;
    }

    public RootResponse getRoot() {
        // getForObject 会发送 GET，并把 JSON 映射为指定的 record。
        return restTemplate.getForObject(properties.baseUrl() + "/", RootResponse.class);
    }

    public HealthResponse getHealth() {
        return restTemplate.getForObject(properties.baseUrl() + "/health", HealthResponse.class);
    }

    public AskResponse ask(AskRequest request) {
        // /ask 需要 JSON body，因此显式设置 Content-Type 并包装 HttpEntity。
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<AskRequest> entity = new HttpEntity<>(request, headers);
        return restTemplate.postForObject(properties.baseUrl() + "/ask", entity, AskResponse.class);
    }

    public ReloadResponse reload() {
        return restTemplate.postForObject(properties.baseUrl() + "/reload", HttpEntity.EMPTY, ReloadResponse.class);
    }
}
