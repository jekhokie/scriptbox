# Kafka Analyzer

Python script to take the output of queries run against a Kafka cluster and produce some
useful metric information around Topic information such as total size of topics, total number
of topics, etc. At the time of this script, there was no "easy" way to get the total storage a
particular Topic consumed on a Kafka cluster, and from this data gathering activity came about
many other useful metrics that were gathered and printed out for convenience.

Note that this script currently expects a JSON file containing the output of the log-dirs
script to exist in order to derive useful information. This is due to the fact that the confluent
libraries at the time of this script creation did not have the built-in capability to query the
partition log information through the Kafka admin API.

## Tech Debt

There are plenty of work/improvements that could be done to this functionality - these specifically
will be kept up in the header of the script itself for ease of reference.

## Prerequisites

Install easy_install, pip and virtualenv. Then, clone this repository and navigate to this example:

```bash
$ git clone https://<git_location>/scriptbox.git
$ cd scriptbox/python--kafka-metrics/
```

Install the required environment and libraries:

```bash
$ python3 -m virtualenv --no-site-packages --distribute .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```

Create a configuration file from the sample and specify the values for your specific environment.
This particular configuration will be our source:

```bash
$ cp config/settings.yml.sample config/settings.yml
# edit the config/settings.yml file for your environment
```

**WARNING**: You will likely want to lock down the `settings.yml` file as it could contain sensitive
information - better yet, just switch the code to use environment variables so you don't need to
worry about storing such sensitive info!

## Kafka Data Gathering Prerequisite

This script expects a JSON file to exist in the `cache/` directory which contains the output of
the `kafka-log-dirs.sh` script for the particular Kafka cluster in question. Run the script and
save the output of the JSON to a file which can be placed into the `cache/` directory and configured
appropriately for reference in your `config/settings.yml` file. This script comes packaged in the
`bin/` directory of your Kafka distribution. For example, to run the script against your cluster,
replace `<HOST_NAME>:<PORT>` with the specific bootstrap server hostname and port, and save the output
to a file named `logdirs.json` like so:

```bash
$ ./kafka-log-dirs.sh --bootstrap-server <HOST_NAME>:<PORT> --describe > ~/logdirs.json
```

**WARNING**: Make sure that you remove the first 2 lines of the file (or however many are not valid
formatted JSON output from the script) to avoid parsing failures by the JSON library within this
script functionality.

You can then place the `logdirs.json` file into the `cache/` directory of this project to get the results
from the script.

## Usage

Now that the configurations are in place, run the script to produce the expected metrics:

```bash
$ ./get_kafka_stats.py
```

If all goes well, you should see some metrics output detailing some information about your Kafka cluster.
Feel free to extend this functionality or derive any additional useful information you may be interested in!
