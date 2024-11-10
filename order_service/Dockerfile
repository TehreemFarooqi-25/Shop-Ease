FROM maven:3.8.6-openjdk-11 AS build
WORKDIR /app

# Copy your pom.xml and the source code
COPY pom.xml ./
COPY src ./src

# Package the application
RUN mvn clean package -DskipTests

# Use OpenJDK image for running the application
FROM openjdk:11-jre-slim
COPY --from=build /app/target/order_service-0.0.1-SNAPSHOT.jar app.jar
ENTRYPOINT ["java", "-jar", "/app.jar"]
