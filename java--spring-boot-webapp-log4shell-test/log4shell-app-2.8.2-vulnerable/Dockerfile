FROM alpine

RUN apk add openjdk8

COPY target/hello-world-1.0.0.jar /home/hello-world-1.0.0.jar

EXPOSE 8880/tcp

CMD java -jar /home/hello-world-1.0.0.jar
