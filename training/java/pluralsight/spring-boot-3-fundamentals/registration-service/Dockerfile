FROM eclipse-temurin:21-jre-alpine
ADD target/registration-service-0.0.1-SNAPSHOT.jar registration-service.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "registration-service.jar"]
