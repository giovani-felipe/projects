package com.example.contacts.config;

import com.example.contacts.models.two.User;
import com.example.contacts.repositories.two.UserRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.example.contacts.models.one.Contact;
import com.example.contacts.repositories.one.ContactRepository;

@Configuration
public class ContactDBLoad {
    @Bean
    CommandLineRunner initDatabase(ContactRepository repository, UserRepository repositoryTwo) {

        return args -> {
            System.out.println("Preloading " + repository.save(new Contact("John Smith", "123-456-7890", "jsmith@pluralsight.com")));
            System.out.println("Preloading " + repository.save(new Contact("Samantha Davis", "098-765-4321", "sdavis@pluralsight.com")));
            System.out.println("Preloading Two " + repositoryTwo.save(new User("User")));
        };
    }

}
