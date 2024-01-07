# Performance comparison between OS threads and virtual threads on different computation types

## Endpoint

`/standard` endpoint is using a simple function
`/mono` endpoint is using Spring-WebFlux
`/suspending` endpoint is using Kotlin suspending function

## Types of computation

`sleep()` - sleeps for one second

`busyWait()` - busy waits for one second

`base64()` - encodes string to base64 in a loop until it takes 1 second total

## Virtual Threads
To enable Virtual Thread processing set variable in application.properties
```
spring.threads.virtual.enabled=true
```

## Method

1. Run the application inside docker container with 1 CPU
2. Perform measurement using JMeter and write data to .csv
3. Stop the application
4. Evaluate results

## Running the application

```
./gradlew assemble
```

```
 docker build -t performance-test .
```

```
 docker run --cpus 1 -p 8080:8080 performance-test
```

```
curl localhost:8080/standard
```

## Visualize throughput

```
python3 plot.py [file1] [file2]
```
