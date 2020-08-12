#!/usr/bin/env python3

import argparse
import ldap
import time
import yaml
import datetime
from datetime import datetime, timedelta
from tabulate import tabulate

# specific attributes we need
ldap_attrs = ["dn", "name", "displayName", "mail", "accountExpires", "memberOf"]

# load configs
with open('config/settings.yml', 'r') as yml:
    config = yaml.load(yml, Loader=yaml.FullLoader)

# determine if groups should be output
parser = argparse.ArgumentParser(description='Capture and display user information and groups')
parser.add_argument('-g', action='store_true', default=False, dest='show_groups', help='Include group information for each user in output')
parser.add_argument('-d', action='store_true', default=False, dest='debug_output', help='Whether to include debug output during search')
args = parser.parse_args()

# initialize and attempt to bind - will fail if unsuccessful
l = ldap.initialize("{}://{}".format(config['protocol'], config['host']))
l.simple_bind_s(config['user'], config['passwd'])

# convert an LDAP-provided timestamp to something human readable
def convert_ad_timestamp(ts):
    epoch_sec = ts / 10**7
    expiry_date = "NEVER"
    is_expired = ""
    try:
        expiry = datetime.fromtimestamp(epoch_sec) - timedelta(days=(1970-1601) * 365 + 89)
        expiry_date = expiry.strftime("%a, %d %b %Y %H:%M:%S %Z")

        if expiry < datetime.now():
            is_expired = "X"
    except:
        pass    # some date way in the future to prevent expiry

    return (expiry_date, is_expired)

user_table = []
user_groups = []
users = config['users']
for user in users:
    # set up some reasonable default values for printing
    (given_name, surname) = user.split(" ", 1)
    name = user
    display_name = ""
    email = ""
    expires_date = "NO ACCOUNT/NOT FOUND"
    is_expired = ""
    memberships = ""

    # search for user
    if args.debug_output:
        print("Searching values for: {}".format(user))

    user_result = l.search_s(config['base_dn'], ldap.SCOPE_SUBTREE, "(&(givenName={})(sn={}))".format(given_name, surname), ldap_attrs)

    if user_result:
        dn, attrs = user_result[0]
        name = attrs['name'][0].decode('utf-8')
        display_name = attrs['displayName'][0].decode('utf-8')
        email = attrs['mail'][0].decode('utf-8')

        # output values if requested
        if args.debug_output:
            print("   dn:{}|display_name:{}|email:{}".format(dn, display_name, email))

        # manipulate memberships into something useful
        if attrs['memberOf']:
            memberships = "\n".join(sorted([x.decode('utf-8') for x in attrs['memberOf']]))

        # convert account expiration into something useful
        if attrs['accountExpires']:
            ldap_ts = float(attrs['accountExpires'][0])
            (expires_date, is_expired) = convert_ad_timestamp(ldap_ts)
    elif args.debug_output:
        print("   No user data found!")

    # add table row for user info
    user_table.append([name, display_name, email, is_expired, expires_date])
    user_groups.append([name, memberships])

# sort results for easier viewing
user_table.sort(key=lambda x: x[0])

# print the tabular results
print(tabulate(user_table, headers=['Name', 'displayName', 'Mail', 'Expired?', 'Account Expiry'],
                           tablefmt='fancy_grid',
                           colalign=('left','center','center','center','center')))

# print the results of memberships
if args.show_groups:
    print(tabulate(user_groups, headers=['Name', 'Memberships'],
                                tablefmt='fancy_grid',
                                colalign=('left','left')))
