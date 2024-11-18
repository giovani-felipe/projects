package com.example.contacts.services;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.when;

import java.util.Optional;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import com.example.contacts.models.Contact;
import com.example.contacts.repositories.ContactRepository;

@ExtendWith(MockitoExtension.class)
public class ContactServiceUnitTest {

  @Mock
  private ContactRepository repository;

  @InjectMocks
  private ContactService service;

  @Test
  public void testMockRepo() throws Exception {
    Contact contact = new Contact();
    contact.setId(1L);
    contact.setName("Giovani Santos");

    when(repository.findById(1L)).thenReturn(Optional.of(contact));

    Contact result = service.getContactById(1L);
    assertEquals(contact, result);
  }
}
