#!/usr/bin/env python
#
# Purpose: Align user permissions in each Delphix engine specified in
# the configuration file with the users specified in the CSV config file.
#

import csv
import json
from subprocess import check_output

# variable for location of the DXTOOLKIT configuration file
dx_config = "DXTOOLKIT_CONF=config/settings.conf"

# import users needing access - this is CSV to make it easier for the user to input the data
with open('config/users.csv', 'r') as f_csv:
    users = csv.DictReader(filter(lambda row: row[0]!='#', f_csv))
    user_json = json.loads(json.dumps([row for row in users]))

    # store usernames for comparison later when we do complete alignment of users
    desired_usernames = [i['username'] for i in user_json]

# parse each engine in the configuration file
# TODO: Enhance error checking
engines_out = check_output(["{} ./bin/dx_get_appliance -format json".format(dx_config)], shell=True)
engines = json.loads(engines_out)
for engine in engines['results']:
    if engine['Status'] == 'UP':
        print("Engine '{}' is UP - Adding Users...".format(engine['Appliance']))

        # get the list of users from the engine
        users_out = check_output(["{} ./bin/dx_get_users -engine {} -format json".format(dx_config, engine['Appliance'])], shell=True)
        users = json.loads(users_out)

        # store usernames from engine for future when we do actual alignment of users (not just creations)
        engine_usernames = [i['Username'] for i in users['results']]

        # TODO: Update this section to differentiate 'engine_usernames' from 'desired_usernames' and
        #       automatically handle creates vs. updates vs. deletions - for now, just create the users
    else:
        print("Engine '{}' is DOWN - No Further Action to Take, Moving On".format(engine['Appliance']))
