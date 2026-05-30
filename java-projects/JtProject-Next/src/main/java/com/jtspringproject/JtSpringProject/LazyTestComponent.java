package com.jtspringproject.JtSpringProject;

import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Component;

/**
 * 懒加载依赖示例组件。
 *
 * <p>用于测试 Spring 的 `@Lazy` 注入行为，避免 `AnotherComponent` 在容器启动时立即实例化。</p>
 */
@Component
public class LazyTestComponent {

    private final AnotherComponent anotherComponent;

    public LazyTestComponent(@Lazy AnotherComponent anotherComponent) {
        this.anotherComponent = anotherComponent;
    }

    public AnotherComponent getAnotherComponent() {
        return anotherComponent;
    }
}
