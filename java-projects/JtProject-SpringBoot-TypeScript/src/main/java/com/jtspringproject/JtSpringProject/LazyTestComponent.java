package com.jtspringproject.JtSpringProject;

import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Component;

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
