package com.example.contacts.repositories.two;


import com.example.contacts.models.two.User;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository<User, Long> {
}
