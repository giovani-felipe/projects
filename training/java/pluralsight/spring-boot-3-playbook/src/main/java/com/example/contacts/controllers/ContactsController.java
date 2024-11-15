package com.example.contacts.controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.contacts.models.one.Contact;
import com.example.contacts.repositories.one.ContactRepository;

import java.util.List;

@RestController
public class ContactsController {

    @Autowired
    private ContactRepository repository;

    @GetMapping("/contacts")
    List<Contact> all() {
        return repository.findAll();
    }

    @GetMapping("/contacts/add")
    @Transactional
    List<Contact> add() {
        Contact one = new Contact();
        one.setEmail("test1@email.com");
        one.setName("Test1");

        repository.save(one);

        if(1 == 1) {
            throw new RuntimeException();
        }

        Contact two = new Contact();
        two.setEmail("test2@email.com");
        two.setName("Test2");

        repository.save(two);

        return repository.findAll();
    }
}
