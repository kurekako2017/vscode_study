package com.jtspringproject.JtSpringProject;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.transaction.annotation.EnableTransactionManagement;
import org.springframework.orm.hibernate5.HibernateTransactionManager;
import org.hibernate.SessionFactory;

@Configuration
@EnableTransactionManagement
public class TransactionConfig {

    @Bean
    public HibernateTransactionManager transactionManager(SessionFactory sessionFactory) {
        // 统一把 Hibernate 的 SessionFactory 交给 Spring 事务管理器，
        // 这样 DAO 层只需要依赖当前线程绑定的事务上下文即可。
        HibernateTransactionManager transactionManager = new HibernateTransactionManager();
        transactionManager.setSessionFactory(sessionFactory);
        return transactionManager;
    }
}
