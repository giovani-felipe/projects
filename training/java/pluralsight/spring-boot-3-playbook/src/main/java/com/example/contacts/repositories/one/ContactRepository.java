package com.example.contacts.repositories.one;


import org.springframework.data.jpa.repository.JpaRepository;

import com.example.contacts.models.one.Contact;

public interface ContactRepository extends JpaRepository<Contact, Long> {
}
