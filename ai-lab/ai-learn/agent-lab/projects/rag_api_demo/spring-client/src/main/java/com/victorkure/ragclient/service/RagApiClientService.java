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

    private final RestTemplate restTemplate;
    private final RagApiClientProperties properties;

    public RagApiClientService(RestTemplate ragApiRestTemplate, RagApiClientProperties properties) {
        this.restTemplate = ragApiRestTemplate;
        this.properties = properties;
    }

    public RootResponse getRoot() {
        return restTemplate.getForObject(properties.baseUrl() + "/", RootResponse.class);
    }

    public HealthResponse getHealth() {
        return restTemplate.getForObject(properties.baseUrl() + "/health", HealthResponse.class);
    }

    public AskResponse ask(AskRequest request) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<AskRequest> entity = new HttpEntity<>(request, headers);
        return restTemplate.postForObject(properties.baseUrl() + "/ask", entity, AskResponse.class);
    }

    public ReloadResponse reload() {
        return restTemplate.postForObject(properties.baseUrl() + "/reload", HttpEntity.EMPTY, ReloadResponse.class);
    }
}
