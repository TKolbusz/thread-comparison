# Base image
FROM openjdk:21-jdk-slim

# Set working directory
WORKDIR /app

# Copy build artifacts to container
COPY build/libs/test-0.0.1-SNAPSHOT.jar /app/app.jar

# Expose port
EXPOSE 8080

# Start the app
CMD ["java", "-jar", "app.jar"]
