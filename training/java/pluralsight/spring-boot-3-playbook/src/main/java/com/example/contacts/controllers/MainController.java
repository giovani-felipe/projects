package com.example.contacts.controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.jms.core.JmsTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MainController {

  @Value("${spring.application.version}")
  private String version;

  @Autowired
  private JmsTemplate jmsTemplate;

  @GetMapping("/")
  String root() {
    return "Status: Running, version: " + version;
  }

  @GetMapping("/jms")
  String jms() {
    jmsTemplate.convertAndSend("DLQ", "Hello Messaging World!");
    return "Send";
  }
}
