# ReactJS Brooklin MirrorMaker Controller

Small ReactJS application that enables controlling [Brooklin Streams](https://github.com/linkedin/brooklin).
Includes a `docker-compose.yml` file for setting up a local environment containing 2x local ZooKeeper and 2x local
Kafka instances to enable testing.

**NOTE**: The infrastructure in this repository should be considered brittle/for development purposes ONLY. There
are many aspects of hard-coded dependencies (port relationships between containers, Brooklin properties hard-coded to
expect hostnames that are contained in `docker-compose.yml`, etc.). Point is - if you attempt to start changing things,
ensure you understand where all the links are as you will likely encounter errors. This will be left as a "TODO" for
later iterations of this repository.

## Prerequisites

There are several prerequisites required. Specifically, ensure your environment has the following available:

- **npm**: Node Package Manager (used to run ReactJS application)
- **Docker**: A Docker engine
- **docker-compose**: The `docker-compose` command-line interface

Getting the above set up is left as an exercise for the reader (in the interest of not reproducing well-written
documentation on the general internet).

## Building Brooklin Container Image

First step is to build the Docker image for Brooklin. The rest of the Kafka and ZooKeeper Docker images utilize
the Confluent-provided images (trusted), but there were no trusted sources for the Brooklin software at the time
of this repository creation, so "rolling our own" is preferred using decently trusted base images in order to reduce
the risk of malicious code:

```bash
$ docker build -t brooklin .
```

You should see the image built, and can check that it exists locally via `docker image ls brooklin`.

## Start ZooKeepers, Kafkas, and Brooklin

Now that you have your Brooklin image built, we'll start the ecosystem. The full ecosystem contains 2x Kafka clusters
which each use their own ZooKeeper instances, and a single Brooklin instance, all on a common Docker network. More
specific details:

- **kafka1**: Linked to **zookeeper1** (port 2181), exposes publish/consume port 29092 to `localhost`
- **kafka2**: Linked to **zookeeper2** (port 2182), exposes publish/consume port 29093 to `localhost`
- **brooklin**: Linked to **zookeeper2** (port 2182), uses **kafka2** (port 29093) as destination, exposes datastream
management port 32311 to `localhost`

To start up all required components, simply use the following command:

```bash
$ docker-compose up
```

If all goes well, you should see many (MANY) logs scroll by. Investigate some of them to check whether all components
appear healthy/running. You can also use `docker-compose ps` to check whether all instances are up and healthy.

To start, create a Brooklin stream (as of this repo creation, "Create Stream" was not yet implemented). Download the Brooklin
1.1.0 package, unpackage it, and run the following from the `brooklin-1.1.0` directory:

```bash
$ bin/brooklin-rest-client.sh -o CREATE -u http://localhost:32311/ -n first-datastream -s "kafka://localhost:29092/test-events1" -p 1 -c kafkaMirroringConnector -t kafkaTransportProvider -m '{"owner":"test-user","system.reuseExistingDestination":"false"}'
```

The above will create your first datastream, which will be shown in the ReactJS interface in the next step.

## Start ReactJS Brooklin Management App

**WARNING**: To avoid complexities related to CORS setup and keep focus on the functionality being developed, the
Brooklin management app will result in browser errors complaining about CORS errors when running. To work around this,
launch a browser with CORS checking disabled by default (Safari on Mac OS is good for this, or Chrome can be launched
from the command line with CORS disabled - check the web for instructions). If you don't disable CORS before loading the
web page, nothing will appear to work (but you will certainly see errors in the Console logs if you inspect them in the
developer tools!). This was the easiest way to handle this in the short term given no apparent Brooklin CORS handling
controls at the time of this repository creation.

Now that the supporting infrastructure is up, we can launch the Brooklin datastream management application. Simply
run the following:

```bash
$ cd brooklin-stream-manager/
$ npm install
$ npm start
```

After a few minutes, you should have a web page open with the management interface. At this time, it is expected that
Kafka topics will exist in source and destination prior to adding a new stream in Brooklin. The easiest way to do this is
to download the Kafka binaries and pre-create them - start with 2 in each cluster for testing (note that the commands below
assume that you have downloaded/unpacked a version of the Kafka tar file and are in the Kafka directory):

```bash
# create first topic in kafka1 and kafka2
$ bin/kafka-topics.sh --create --topic test-events1 --bootstrap-server localhost:29092
$ bin/kafka-topics.sh --create --topic test-events1 --bootstrap-server localhost:29093

# create second topic in kafka1 and kafka2
$ bin/kafka-topics.sh --create --topic test-events2 --bootstrap-server localhost:29092
$ bin/kafka-topics.sh --create --topic test-events2 --bootstrap-server localhost:29093
```

Once the above is complete, feel free to use the stream manager app to create streams, delete them, pause them, etc. using
the pre-created Kafka topics `test-events1` and `test-events2` created above. Note that the Brooklin instance by default
publishes to **kafka2** as its destination - specifying destination for the Kafka connector was not dynamically supported
at the time of this repository creation and was hard-coded as a default in the `config/server.properties` file that can be
viewed in the `brooklin-config/server.properties` file in this repository.

## Notes

Some useful commands utilizing command-line binaries for interacting with Kafka, Brooklin, and some related links that
reference API endpoints, etc. are contained below.

### Brooklin

Various scripts in the Brooklin package accomplish tasks by executing commands against the
[REST API](https://github.com/linkedin/brooklin/wiki/REST-Endpoints#endpoints) for Brooklin. These commands expect that
you have downloaded, unpackaged, and are in the directory of the Brooklin package.

- Create data stream - mirrors `test-events1` from kafka1 to kafka2 (default Brooklin Kafka)

    ```bash
    $ bin/brooklin-rest-client.sh -o CREATE -u http://localhost:32311/ -n first-datastream -s "kafka://localhost:29092/test-events1" -p 1 -c kafkaMirroringConnector -t kafkaTransportProvider -m '{"owner":"test-user","system.reuseExistingDestination":"false"}'
    ```

- Show stream details

    ```bash
    $ bin/brooklin-rest-client.sh -o READALL -u http://localhost:32311/
    ```

- Same way to show stream details by executing curl request against the API directly

    ```bash
    $ curl http://localhost:32311/datastream/
    ```

- Delete a stream

    ```bash
    $ bin/brooklin-rest-client.sh -o DELETE -u http://localhost:32311 -n first-datastream
    ```

### Kafka

Various scripts in the Kafka package accomplish tasks for Kafka. These commands expect that you have downloaded, unpackaged,
and are in the directory of the Kafka package.

- Read from destination cluster (kafka2)

    ```bash
    $ bin/kafka-console-consumer.sh --topic test-events1 --from-beginning --bootstrap-server localhost:29093
    ```

- Write to source (kafka1) - should see messages show up on kafka2 if you're monitoring using consumer script above

    ```bash
    $ bin/kafka-console-producer.sh --topic test-events1 --bootstrap-server localhost:29092
    ```
