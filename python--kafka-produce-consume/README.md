# Kafka Produce/Consume

Small scripts demonstrating how to produce to and consume from a Kafka cluster using Python. Includes
a `docker-compose.yml` file that spins up a local Kafka instance (and corresponding ZooKeeper) for testing.

## Test Harness

There is a sample ZooKeeper/Kafka setup (bare-bones) that can be run from this repository using docker-compose.
Simply launch the docker daemon on your device, and then run `docker-compose up` from the root directory of this
project folder. After a few minutes, you should have a functioning ZooKeeper + Kafka running on your local
machine.

If you want to launch this setup as a daemon (so it is not running in the foreground and logging output to your
terminal), simply run `docker-compose up -d`.

## Prerequisites

Install easy_install, pip and virtualenv. Then, clone this repository and navigate to this example:

```bash
$ git clone https://<git_location>/scriptbox.git
$ cd scriptbox/python--kafka-produce-consume/
```

Install the required environment and libraries:

```bash
$ python3 -m virtualenv .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```

Finally, you will likely require a copy of the Kafka command-line tools somewhere. Download the latest version
from the Kafka download site and place them somewhere that you can remember/access easily as we will need the
tools to create the example topic for use.

## Configuration

To configure your producer and consumer to reach the correct endpoint, copy the sample configuration YAML file
and place your environment-specific settings into the configuration.

**Note**: If you use the "Test Harness" method above (running a local ZooKeeper + Kafka instance using docker-compose),
you can simply copy the sample settings file and leave all configurations in place.

```bash
$ cp config/settings.yml.sample config/settings.yml
$ vim config/settings.yml
# enter your environment-specific information, or
# leave alone if you're using docker-compose from
# this repository
```

## Creating a Topic

This functionality requires a test topic be available in your target Kafka cluster. Run the `kafka-topics.sh` script
from the Kafka command-line tools you downloaded in the "Prerequisites" section above, replacing the path with the
path to your `kafka-topics.sh` script, the `bootstrap-server` with your Kafka cluster endpoint, and the `topic` with
the topic configured in your `settings.yml` file. If you left the `config/settings.yml` file the same as the sample
file, you can simply run the command below as-is with the exception of needing to specify the correct path to the
`kafka-topics.sh` script:

```bash
$ ./kafka_2.13-2.7.0/bin/kafka-topics.sh --create --topic test-1 --bootstrap-server localhost:29092
```

To validate that your topics was created, you can run the following, which should output the `test-1` topic (or whatever
topic you specified):

```bash
$ ./kafka_2.13-2.7.0/bin/kafka-topics.sh --list --bootstrap-server localhost:29092
```

## Usage

Now that things are configured, simply launch the consumer and then producer (in separate terminal windows), and you
should start to see output from each indicating producing to and consuming from the Kafka endpoint:

```bash
$ python3 start_consumer.py
$ python3 start_producer.py
```

You now have a fully-functional (albeit basic) Kafka Producer and Consumer environment using Python!
