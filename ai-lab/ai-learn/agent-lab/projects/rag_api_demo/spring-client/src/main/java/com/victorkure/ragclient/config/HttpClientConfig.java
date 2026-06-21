package com.victorkure.ragclient.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.web.client.RestTemplate;

@Configuration
public class HttpClientConfig {

    // @Bean 把 RestTemplate 放进 Spring 容器，Service 构造函数可直接注入复用。
    @Bean
    RestTemplate ragApiRestTemplate(RestTemplateBuilder builder) {
        return builder.build();
    }
}
