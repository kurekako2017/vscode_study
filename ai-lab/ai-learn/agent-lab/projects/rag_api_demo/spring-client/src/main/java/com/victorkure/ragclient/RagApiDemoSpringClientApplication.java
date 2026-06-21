package com.victorkure.ragclient;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.ConfigurationPropertiesScan;

@SpringBootApplication
@ConfigurationPropertiesScan
public class RagApiDemoSpringClientApplication {

    public static void main(String[] args) {
        // Spring Client 本身不执行推理，实际模型由它所调用的 FastAPI 后端选择。
        System.out.println("MODEL: provider=backend model=request-dependent mode=spring-client");
        SpringApplication.run(RagApiDemoSpringClientApplication.class, args);
    }
}
