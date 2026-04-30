package com.jtspringproject.JtSpringProject;

import org.springframework.stereotype.Component;

/**
 * 简单示例组件。
 *
 * <p>用于验证 Spring 组件扫描和基本 Bean 注入是否正常工作。</p>
 */
@Component
public class AnotherComponent {
    public String getMessage() {
        return "Hello from AnotherComponent!";
    }
}
