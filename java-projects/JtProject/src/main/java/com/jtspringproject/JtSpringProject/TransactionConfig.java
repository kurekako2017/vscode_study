package com.jtspringproject.JtSpringProject;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.transaction.annotation.EnableTransactionManagement;
import org.springframework.orm.hibernate5.HibernateTransactionManager;
import org.hibernate.SessionFactory;

/**
 * 事务管理配置。
 *
 * <p>为基于 Hibernate SessionFactory 的 DAO 层启用声明式事务管理。</p>
 */
@Configuration
@EnableTransactionManagement
public class TransactionConfig {

    @Bean
    public HibernateTransactionManager transactionManager(SessionFactory sessionFactory) {
        HibernateTransactionManager transactionManager = new HibernateTransactionManager();
        transactionManager.setSessionFactory(sessionFactory);
        return transactionManager;
    }
}
