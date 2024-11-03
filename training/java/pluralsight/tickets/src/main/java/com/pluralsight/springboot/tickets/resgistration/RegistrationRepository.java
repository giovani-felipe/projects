package com.pluralsight.springboot.tickets.resgistration;

import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.Optional;


public interface RegistrationRepository extends MongoRepository<Registration, String> {

  Optional<Registration> findByTicketCode(String ticketCode);

  void deleteByTicketCode(String ticketCode);

}
