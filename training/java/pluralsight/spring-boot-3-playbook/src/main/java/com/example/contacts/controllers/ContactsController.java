package com.example.contacts.controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.contacts.models.Contact;
import com.example.contacts.repositories.ContactRepository;

import java.util.List;

@RestController
public class ContactsController {

    @Autowired
    private ContactRepository repository;

    @GetMapping("/contacts")
    List<Contact> all() {
        return repository.findAll();
    }
}
