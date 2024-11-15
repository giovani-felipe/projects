package com.example.contacts.config;

import jakarta.persistence.EntityManagerFactory;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.jdbc.DataSourceBuilder;
import org.springframework.boot.orm.jpa.EntityManagerFactoryBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.orm.jpa.JpaTransactionManager;
import org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean;
import org.springframework.orm.jpa.vendor.HibernateJpaVendorAdapter;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.annotation.EnableTransactionManagement;

import javax.sql.DataSource;
import java.util.HashMap;
import java.util.Map;

@Configuration
@EnableTransactionManagement
@EnableJpaRepositories(
        basePackages = "com.example.contacts.repositories.two",
        entityManagerFactoryRef = "entityManagerFactoryTwo",
        transactionManagerRef = "transactionManagerTwo"
)
public class DatasourceTwoConfig {

    @Bean(name = "dataSourceTwo")
    @ConfigurationProperties(prefix = "spring.datasource.two")
    public DataSource dataSourceTwo() {
        return DataSourceBuilder.create().build();
    }

    @Bean
    public EntityManagerFactoryBuilder entityManagerFactoryBuilderTwo() {
        HibernateJpaVendorAdapter vendorAdapter = new HibernateJpaVendorAdapter();
        vendorAdapter.setShowSql(true);

        Map<String, String> jpaProperties = new HashMap<>();
        jpaProperties.put("hibernate.dialect", "org.hibernate.dialect.H2Dialect");
        jpaProperties.put("hibernate.hbm2ddl.auto", "create");
        return new EntityManagerFactoryBuilder(vendorAdapter, jpaProperties, null);
    }
    @Bean(name = "entityManagerFactoryTwo")
    public LocalContainerEntityManagerFactoryBean entityManagerFactoryTwo(
            @Qualifier("dataSourceTwo") DataSource dataSource) {
        return entityManagerFactoryBuilderTwo()
                .dataSource(dataSource)
                .packages("com.example.contacts.models.two")
                .persistenceUnit("two")
                .build();
    }

    @Bean(name = "transactionManagerTwo")
    public PlatformTransactionManager transactionManagerTwo(
            @Qualifier("entityManagerFactoryTwo") EntityManagerFactory entityManagerFactory) {
        return new JpaTransactionManager(entityManagerFactory);
    }
}
