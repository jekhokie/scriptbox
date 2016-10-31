# Load Test Graphite

Script to very quickly test a Graphite endpoint.

WARNING: Graphite environments are inherently dynamic in nature, as are the metrics that are sent to
it. This script is a VERY rudimentary implementation of a stresser for a Graphite endpoint but in NO
way should be considered a very precies tuning mechanism. Various environmental conditions (number of
metrics per data packet, complexity of namespacing, etc) can severely impact the actual operation of
Graphite, and this script does not take these into account.

## Prerequisites

Install easy_install, pip, and virtualenv. Then, clone this repository and navigate to this example:

```bash
$ git clone https://<git_location>/scriptbox.git
$ cd scriptbox/python--load-test-graphite
```

Set up a virtual environment for use (optional - you can likely use the system Python without issue):

```bash
$ virtualenv --no-site-packages --distribute .env
$ source .env/bin/activate
```

## Usage

To run the load tester, the following command sequence is expected:

```bash
./load_test_graphite.py <GRAPHITE_HOST> <GRAPHITE_PORT> <NUM_UNIQUE_METRICS> <METRICS_PER_MINUTE>
```

Where:

* GRAPHITE_HOST: Hostname or IP address of the Graphite (Carbon) endpoint.
* GRAPHITE_PORT: Port (TCP) of the Graphite (Carbon) endpoint.
* NUM_UNIQUE_METRICS: Total number of unique metrics that will be generated.
* METRICS_PER_MINUTE: How many metrics per minute desired to be generated.

For example, you can load test a Graphite endpoint having a hostname of graphite.test.instance on
TCP port 2003 at a rate of 500k metrics per minute for 200 unique metrics via the following:

```bash
./load_test_graphite.py graphite.test.instance 2003 200 500000
# should expect to see output such as:
#   ...
#   [1137235156] -- 8333 metrics sent -- 0.970 seconds
#   [1137235157] -- 8333 metrics sent -- 0.953 seconds
#   [1137235158] -- 8333 metrics sent -- 0.948 seconds
#   [1137235159] -- 8333 metrics sent -- 0.950 seconds
#   ...
```
