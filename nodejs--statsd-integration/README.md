# Statsd Integration

This is a quick project set up to test the integration with the Statsd product (https://github.com/etsy/statsd).

## Graphite/Statsd Prerequisites

Some configuration parameters must be set within Statsd and Graphite in order for the 1 second metric resolution
to work as expected. These assume that Graphite is installed in /opt/graphite. The following settings are required.

### Graphite

```bash
# /opt/graphite/webapp/graphite/local_settings.py
MEMCACHE_DURATION = 1
```

```bash
# /opt/graphite/conf/storage-schemas.conf
[1s_for_1hour]
priority = 100
pattern = ^stats.*
retentions = 1:3600
```

### Statsd

```bash
# /opt/statsd/exampleConfig.js (assuming this is your configuration file)
...
  flushInterval: 1000
...
```

## Prerequisites

Install NodeJS and npm. Then, clone this repository and navigate to this example:

```bash
$ git clone https://<git_location>/scriptbox.git
$ cd scriptbox/nodejs--statsd-integration
```

Install the required environment and libraries:

```bash
$ npm install
```

Create a configuration file from the sample and specify the values for your specific environment.

```bash
$ cp config/.env.sample config/.env
# edit the config/.env file for your environment
$ chmod 600 config/.env
# lock down the file as it contains sensitive information
```

## Usage

Now that the configurations are in place, run the script to interact with the Statsd service.

```bash
$ nodejs submit-metric.js
# you should see output corresponding to the request/response sequence
```
