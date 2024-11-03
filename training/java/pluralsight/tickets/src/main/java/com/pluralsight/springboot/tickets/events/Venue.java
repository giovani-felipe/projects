package com.pluralsight.springboot.tickets.events;

import jakarta.persistence.*;

@Entity
@Table(name = "vanues")
public class Venue {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Integer id;

  @Column
  private String name;

  @Column
  private String street;

  @Column
  private String city;

  @Column
  private String country;

  public Venue() {
  }

  public Venue(String name, String street, String city, String country) {
    this.name = name;
    this.street = street;
    this.city = city;
    this.country = country;
  }

  public Integer getId() {
    return id;
  }

  public void setId(Integer id) {
    this.id = id;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public String getStreet() {
    return street;
  }

  public void setStreet(String street) {
    this.street = street;
  }

  public String getCity() {
    return city;
  }

  public void setCity(String city) {
    this.city = city;
  }

  public String getCountry() {
    return country;
  }

  public void setCountry(String country) {
    this.country = country;
  }
}
