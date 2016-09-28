# RabbitMQ Producer/Consumer

Scripts to demonstrate interaction with the RabbitMQ message queueing service.

## Prerequisites

These scripts/this setup assumes that RVM is already installed and configured on your system. To
install/configure RVM, follow the instructions on this site:

- https://rvm.io/


In addition, the scripts assume that a RabbitMQ service/cluster is already deployed and configured
for communication. Installation and configuration of a RabbitMQ instance/cluster is outside the
scope of this project, but instructions can be found here:

- https://www.rabbitmq.com/

At a minimum, the configuration for the virtual host, username and password for RabbitMQ defined in
the .env file must match a valid permissions scheme for RabbitMQ, otherwise, an "access to vhost...
refused for user..." error will be reported. Something like the following on the RabbitMQ cluster
should work:

```bash
$ sudo rabbitmqctl add_vhost /<VHOST_NAME>
$ sudo rabbitmqctl add_user <RMQ_USERNAME> <RMQ_PASSWORD>
$ sudo rabbitmqctl set_permissions -p /<VHOST_NAME> <RMQ_USERNAME> ".*" ".*" ".*"
$ sudo rabbitmqctl set_user_tags <RMQ_USERNAME> management
```

## Configuration

Install bundler:

```bash
$ gem install bundler
```

Install the required gems:

```bash
$ bundle install
```

Copy and update the .env for your environment configuration:

```bash
$ cp .env.sample .env
$ vim .env
# add the RabbitMQ endpoint to communicate with along with other environment-specific settings
```

## Usage

There are two scripts within the project - one script deals with publishing data to a RabbitMQ service
while the other deals with subscribing and pulling data from a RabbitMQ service.

### RabbitMQ Producer

To publish random data to a RabbitMQ instance queue, run the producer script as follows:

```bash
$ ./producer.rb
# should expect to see output such as:
#   TODO: FILLMEIN
#   Connection Established...
#   Host: 10.11.12.13
#   Port: 5672
#   Username: test
#   Password: ****
#   Virtual Host: /testing
#   Queue: test
#   --------------------------------
#   Sending '538' to queue
#   Sending '319' to queue
#   Sending '255' to queue
#   Sending '961' to queue
#   Sending '768' to queue
#   Sending '161' to queue
#   Sending '367' to queue
#   ...
```

Press CTRL-C to terminate the producer script.

### RabbitMQ Subscriber/Reader

To read information/data from a RabbitMQ instance queue, run the consumer script as follows:

```bash
$ ./consumer.rb
# should expect to see output such as:
#   Connection Established...
#   Host: 10.11.12.13
#   Port: 5672
#   Username: test
#   Password: ****
#   Virtual Host: /testing
#   Queue: test
#   --------------------------------
#   Received: 538
#   Received: 319
#   Received: 255
#   Received: 961
#   Received: 768
#   Received: 161
#   Received: 367
#   ...
```

Press CTRL-C to terminate the consumer script.
