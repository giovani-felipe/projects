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
        basePackages = "com.example.contacts.repositories.one",
        entityManagerFactoryRef = "entityManagerFactoryOne",
        transactionManagerRef = "transactionManagerOne"
)
public class DatasourceOneConfig {

    @Primary
    @Bean(name = "dataSourceOne")
    @ConfigurationProperties(prefix = "spring.datasource.one")
    public DataSource dataSourceOne() {
        return DataSourceBuilder.create().build();
    }

    @Bean
    public EntityManagerFactoryBuilder entityManagerFactoryBuilder() {
        HibernateJpaVendorAdapter vendorAdapter = new HibernateJpaVendorAdapter();
        vendorAdapter.setShowSql(true);

        Map<String, String> jpaProperties = new HashMap<>();
        jpaProperties.put("hibernate.dialect", "org.hibernate.dialect.H2Dialect");
        jpaProperties.put("hibernate.hbm2ddl.auto", "create");
        return new EntityManagerFactoryBuilder(vendorAdapter, jpaProperties, null);
    }
    @Primary
    @Bean(name = "entityManagerFactoryOne")
    public LocalContainerEntityManagerFactoryBean entityManagerFactoryOne(
            @Qualifier("dataSourceOne") DataSource dataSource) {
        return  entityManagerFactoryBuilder()
                .dataSource(dataSource)
                .packages("com.example.contacts.models.one")
                .persistenceUnit("one")
                .build();
    }

    @Primary
    @Bean(name = "transactionManagerOne")
    public PlatformTransactionManager transactionManagerOne(
            @Qualifier("entityManagerFactoryOne") EntityManagerFactory entityManagerFactory) {
        return new JpaTransactionManager(entityManagerFactory);
    }
}
