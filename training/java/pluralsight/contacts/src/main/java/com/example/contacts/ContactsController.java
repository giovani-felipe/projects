package com.example.contacts;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class ContactsController {
  @Autowired
  private ContactRepository contactRepository;

  @GetMapping("/contacts")
  List<Contact> all() {
    return contactRepository.findAll();
  }
}
