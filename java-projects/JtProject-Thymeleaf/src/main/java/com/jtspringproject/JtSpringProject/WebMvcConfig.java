package com.jtspringproject.JtSpringProject;

import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
@Profile("!batch")
public class WebMvcConfig implements WebMvcConfigurer {
}
