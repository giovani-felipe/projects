package com.example.contacts;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;

@SpringBootApplication
public class ContactsApplication {

  public static void main(String[] args) {
    SpringApplication.run(ContactsApplication.class, args);
  }
}
