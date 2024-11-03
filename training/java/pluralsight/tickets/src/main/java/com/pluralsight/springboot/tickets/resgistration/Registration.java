package com.pluralsight.springboot.tickets.resgistration;

import jakarta.persistence.Id;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import org.springframework.data.mongodb.core.mapping.Document;

@Document("registrations")
public record Registration(@Id String id, @NotNull(message = "Product id is required") Integer productId,
                           String ticketCode, @NotBlank(message = "Attendee name is required") String attendeeName) {
}
