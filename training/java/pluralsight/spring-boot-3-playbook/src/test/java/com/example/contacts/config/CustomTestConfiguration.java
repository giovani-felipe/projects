package com.example.contacts.config;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Bean;

import com.example.contacts.models.Contact;
import com.example.contacts.repositories.ContactRepository;

@TestConfiguration()
public class CustomTestConfiguration {
    @Bean
    CommandLineRunner initDatabase(ContactRepository repository) {

        return args -> {
            System.out.println("Preloading " + repository.save(new Contact("Jerry Smith", "123-456-7890", "jsmith@pluralsight.com")));
            System.out.println("Preloading " + repository.save(new Contact("Nancy Davis", "098-765-4321", "sdavis@pluralsight.com")));
        };
    }

}
