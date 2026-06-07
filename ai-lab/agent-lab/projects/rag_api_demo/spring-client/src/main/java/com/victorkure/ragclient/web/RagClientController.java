package com.victorkure.ragclient.web;

import com.victorkure.ragclient.dto.AskRequest;
import com.victorkure.ragclient.dto.AskResponse;
import com.victorkure.ragclient.dto.HealthResponse;
import com.victorkure.ragclient.dto.ReloadResponse;
import com.victorkure.ragclient.dto.RootResponse;
import com.victorkure.ragclient.service.RagApiClientService;
import java.util.Map;
import java.util.List;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/client")
public class RagClientController {

    private final RagApiClientService ragApiClientService;
    private final String baseUrl;

    public RagClientController(
        RagApiClientService ragApiClientService,
        @Value("${rag.api.base-url:http://127.0.0.1:8000}") String baseUrl
    ) {
        this.ragApiClientService = ragApiClientService;
        this.baseUrl = baseUrl;
    }

    @GetMapping
    public Map<String, Object> info() {
        return Map.of(
            "client", "rag-api-demo-spring-client",
            "backend_base_url", baseUrl,
            "endpoints", List.of("/client/root", "/client/health", "/client/ask", "/client/reload")
        );
    }

    @GetMapping("/root")
    public RootResponse root() {
        return ragApiClientService.getRoot();
    }

    @GetMapping("/health")
    public HealthResponse health() {
        return ragApiClientService.getHealth();
    }

    @PostMapping("/ask")
    public AskResponse ask(@RequestBody AskRequest request) {
        return ragApiClientService.ask(request);
    }

    @PostMapping("/reload")
    public ReloadResponse reload() {
        return ragApiClientService.reload();
    }
}
