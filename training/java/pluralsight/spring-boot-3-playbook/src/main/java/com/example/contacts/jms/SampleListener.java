package com.example.contacts.jms;

import org.springframework.jms.annotation.JmsListener;
import org.springframework.stereotype.Component;

import jakarta.jms.JMSException;
import jakarta.jms.Message;
import jakarta.jms.TextMessage;

@Component
public class SampleListener {

  @JmsListener(destination = "DLQ")
  public void dlqMessage(Message message) throws JMSException {
    if (message instanceof TextMessage) {
      System.out.println(((TextMessage) message).getText());
    } else {
      throw new IllegalArgumentException("Message must be of type TextMessage");
    }
  }
}
