#!/usr/bin/env python
#
# Purpose: Send Graphite-formatted metrics to a Graphite endpoint at a rate specified
#          by the user as metrics/minute. This script will loop until the kill signal
#          CTRL-C is sent to terminate the script itself.
#
# See the README for more information.

import sys, time
from socket import socket
from random import random, choice

# obtain input parameters
try:
    graphite_host = sys.argv[1]
    graphite_port = int(sys.argv[2])
    num_unique_metrics = int(sys.argv[3])
    per_minute_metrics = int(sys.argv[4])
except:
    print "Expected usage: ./load_test_graphite.py <GRAPHITE_HOST> <GRAPHITE_PORT> <NUM_UNIQUE_METRICS> <METRICS_PER_MINUTE>"
    sys.exit(1)

# establish a connection to the Graphite endpoint specified
print "Connecting to the Graphite endpoint: %s:%s" % (graphite_host, graphite_port)
graphite_endpoint = socket()
graphite_endpoint.connect((graphite_host, graphite_port))

# perform some calculations for the load test
metric_range = xrange(1, num_unique_metrics)
group_count = int(round(per_minute_metrics / 60))
print "Configured to send %d unique metrics at %d metrics per minute (roughly %d metrics per second)..." % (num_unique_metrics, per_minute_metrics, group_count)

# start the sending sequence
while True:
    count = 0
    start = time.time()
    for i in xrange(0, group_count):
        # choose a random metric instance to send based on the total range of metrics desired - note
        # that there could be updates to existing values at the same time stamp - this is fine, Graphite
        # does not care and it is still a valid case from an 'ingest' perspective but should be considered
        # another one of the 'environmental' considerations based on the sort strategy used
        r = choice(metric_range)
        metric_name = "testing.metric.%d" % (r)
        data_point = random()
        count += 1

        # send the metric on its way
        graphite_endpoint.sendall("%s %s %s\n" % (metric_name, data_point, start))

    # sleep for a second - this is artificial given that time to perform calculations above may
    # take some time, but we can at least report how long the metrics send took so that the user
    # sees how close to 1 second resolution we are with this - adjust the sleep time to adjust
    # the resolution - this is much faster than performing "on the second" calculations
    time.sleep(0.75)
    time_now = time.time()
    print "[%d] -- %d metrics sent -- %.3f seconds" % (time_now, count, time_now - start)
