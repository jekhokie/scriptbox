#!/usr/bin/env python
#
# Purpose: Create an RRD file with random data every 1 second. This script will loop until the kill
#          signal CTRL-C is sent to terminate the script itself.
#
# WARNING: There is very little defensive coding in this script - your mileage may vary.

import argparse
import rrdtool
import time
from datetime import datetime
from random import randint

# parse the user arguments
parser = argparse.ArgumentParser(description='Create an RRD file rrds/test.rrd and populate with data points every 1 second')
args = parser.parse_args()

# capture some initial variables
rrd_file = 'rrds/test.rrd'
start_epoch = datetime.now().strftime('%s')

# create an RRD file with:
#   * step of 1 second (expecting data at 1 second intervals)
#   * start of the current epoch time (now)
#   * data source named 'test'
#      - type GAUGE
#      - 5 second heartbeat (wait up to 5s for data point before writing 'UNK')
#      - unknown min/max values
#   * archive
#      - type LAST (always store last value received)
#      - xFiles-factor of 0.1 (at least 10% of values must not be UNK for return data of non-UNK)
#      - step of 1 second (store last value every 1 second)
#      - 10 minutes worth of last values (10m * 60s/min * 1s = 600 rows of values over 10 minutes)
#
# Note: Making the archive LAST step match the ingest rate step will result in storage of raw
#       data points for the DS (data source) since LAST @ ingest step rate = raw values.
rrdtool.create(rrd_file,
               '--step', '1s',
               '--start', start_epoch,
               'DS:test:GAUGE:5s:U:U',
               'RRA:LAST:0.1:1s:1m')

# necessary to sleep 1 second since the create operation counts at the current epoch
# (failure to sleep/write within the same epoch second results in a step error)
time.sleep(1)

# write a random integer to the RRD file every 1 second
while True:
    val = randint(0,1000)
    epoch = datetime.now().strftime('%s')
    print "Adding value '%s' at epoch '%s'" % (val, epoch)
    rrdtool.update(rrd_file, '%s:%1s' % (int(epoch), int(val)))
    time.sleep(1)
