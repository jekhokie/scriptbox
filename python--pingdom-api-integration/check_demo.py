#!/usr/bin/env python
#
# Purpose: Create a Pingdom check.
#
# NOTE: This script assumes that the account being used to interact with is not the same
#       account used to perform the requests. In other words, it assumes the "Multi-User
#       Authentication" section of the API documentation:
#           https://www.pingdom.com/resources/api#multi-user+authentication

import requests
import yaml

# import configuration settings
with open('config/settings.yml', 'r') as yml:
    config = yaml.load(yml)

# construct the required headers for requests
headers = {
    'App-Key': config['app_key'],
    'Account-Email': config['account_email']
}

# demo 1, get a list of all checks and print status information
print "############################################################"
print "Getting check counts..."
check_url = "{}/checks".format(config['api_url'])
r = requests.get(check_url, auth=(config['username'], config['password']), headers=headers)
res = r.json()

if 'error' in res:
    raise Exception("Received exception '{}'".format(res['error']['errormessage']))

for check in res['checks']:
    print "{}: {}".format(check['name'], check['status'])
