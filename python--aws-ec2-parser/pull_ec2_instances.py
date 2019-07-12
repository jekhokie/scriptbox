#!/usr/bin/env python
#
# Given a file in the directory 'instances.json', parse the JSON output from an
# AWS EC2 command-line query and print information about the instances. This functionality
# could certainly be converted to also pull down the 'instances.json' as a JSON stream
# or data structure in memory, or many other things. This is just a quick demo of JSON
# parsing logic.
#

import json
from pprint import pprint

# import file
with open('instances.json') as f:
    data = json.load(f)

# parse each instance and print output
for instances in data["Reservations"]:
    for instance in instances["Instances"]:
        hostname = "Unknown"
        hostname_dict = next((item for item in instance["Tags"] if item["Key"] == "Name"), None)
        if hostname_dict is not None:
            hostname = hostname_dict["Value"]
        pprint(instance)

        print(hostname)
        pprint(instance["InstanceType"])
        pprint(instance["LaunchTime"])
