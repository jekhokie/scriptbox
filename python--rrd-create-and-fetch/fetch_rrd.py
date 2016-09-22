#!/usr/bin/env python
#
# Purpose: Fetch data from an RRD file for the last X seconds worth of information.
#
#          Command-line arguments are as follows:
#
#          --last-seconds [-l] - Specifies last X seconds to retrieve information for
#
# WARNING: There is very little defensive coding in this script - your mileage may vary.

import argparse
import rrdtool
from datetime import datetime, timedelta

# parse the user arguments
parser = argparse.ArgumentParser(description='Fetch the last X seconds of data from the rrds/test.rrd file')
parser.add_argument('-l', '--last-seconds', help='Print data from the last X seconds', required=True)
args = parser.parse_args()

# format RRD filename and calculate epoch values for now and X seconds ago
rrd_file = 'rrds/test.rrd'
time_now = datetime.now()
time_x_seconds_ago = time_now - timedelta(seconds=int(args.last_seconds))

# attempt to get the data from the specified RRD file using the time boundaries
metrics = rrdtool.fetch(rrd_file,
                        'LAST', 
                        '--start', time_x_seconds_ago.strftime('%s'),
                        '--end', time_now.strftime('%s'))

start, end, step = metrics[0]
ds = metrics[1]
rows = metrics[2]

# print the results of the RRD fetch operation
print "Start Epoch: %s" % start
print "End Epoch: %s" % end
print "Step: %s" % step
print "DS: %s" % ds
print "Values for last '%s' seconds:" % args.last_seconds

for data in rows:
    if data[0] is None:
        print 'UNKNOWN'
    else:
        print int(data[0])
