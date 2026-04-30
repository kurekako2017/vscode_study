package com.jtspringproject.JtSpringProject;

import org.hibernate.SessionFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.orm.hibernate5.LocalSessionFactoryBean;
import org.springframework.context.annotation.Primary;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;

import javax.sql.DataSource;
import java.util.Properties;

/**
 * Hibernate SessionFactory 配置。
 *
 * <p>该配置用于手动创建 Hibernate SessionFactory，并继续沿用项目现有的 DAO + SessionFactory
 * 访问方式，而不是切换到 Spring Data JPA。</p>
 */
@Configuration
public class HibernateSessionFactoryConfig {

    @Value("${hibernate.dialect:org.hibernate.dialect.MySQL5Dialect}")
    private String hibernateDialect;

    @Value("${hibernate.show_sql:true}")
    private String hibernateShowSql;

    @Value("${hibernate.format_sql:true}")
    private String hibernateFormatSql;

    @Value("${hibernate.hbm2ddl.auto:update}")
    private String hibernateHbm2ddlAuto;

    @Bean
    @Primary
    public LocalSessionFactoryBean sessionFactory(DataSource dataSource) {
        LocalSessionFactoryBean sessionFactory = new LocalSessionFactoryBean();
        sessionFactory.setDataSource(dataSource);
        sessionFactory.setPackagesToScan("com.jtspringproject.JtSpringProject.models");

        Properties hibernateProperties = new Properties();
        hibernateProperties.put("hibernate.dialect", hibernateDialect);
        hibernateProperties.put("hibernate.show_sql", hibernateShowSql);
        hibernateProperties.put("hibernate.format_sql", hibernateFormatSql);
        hibernateProperties.put("hibernate.hbm2ddl.auto", hibernateHbm2ddlAuto);

        sessionFactory.setHibernateProperties(hibernateProperties);
        return sessionFactory;
    }

    @Bean
    @Qualifier("secondarySessionFactory")
    public SessionFactory getSessionFactory(LocalSessionFactoryBean sessionFactoryBean) {
        return sessionFactoryBean.getObject();
    }
}
