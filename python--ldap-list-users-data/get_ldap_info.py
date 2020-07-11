import ldap
import time
import yaml
import datetime
from datetime import datetime, timedelta
from tabulate import tabulate

# specific attributes we need
ldap_attrs = ["dn", "name", "accountExpires", "memberOf"]

# load configs
with open('config/settings.yml', 'r') as yml:
    config = yaml.load(yml, Loader=yaml.FullLoader)

# initialize and attempt to bind - will fail if unsuccessful
l = ldap.initialize("{}://{}".format(config['protocol'], config['host']))
l.simple_bind_s(config['user'], config['passwd'])

# convert an LDAP-provided timestamp to something human readable
def convert_ad_timestamp(ts):
    epoch_sec = ts / 10**7
    return (datetime.fromtimestamp(epoch_sec) - timedelta(days=(1970-1601) * 365 + 89))

user_table = []
users = config['users']
for user in users:
    # set up some reasonable default values for printing
    (given_name, surname) = user.split(" ", 1)
    display_name = user
    expires_date = "NO ACCOUNT/NOT FOUND"
    is_expired = ""
    memberships = ""

    # search for user
    user_result = l.search_s(config['base_dn'], ldap.SCOPE_SUBTREE, "(&(givenName={})(sn={}))".format(given_name, surname), ldap_attrs)

    if user_result:
        dn, attrs = user_result[0]
        display_name = attrs['name'][0].decode('utf-8')

        # manipulate memberships into something useful
        if attrs['memberOf']:
            memberships = "\n".join(sorted([x.decode('utf-8') for x in attrs['memberOf']]))

        # convert account expiration into something useful
        if attrs['accountExpires']:
            ldap_ts = float(attrs['accountExpires'][0])
            expires_dt = convert_ad_timestamp(ldap_ts)
            expires_date = expires_dt.strftime("%a, %d %b %Y %H:%M:%S %Z")

            # check if account is expired
            if expires_dt < datetime.now():
                is_expired = "X"

    # add table row for user info
    user_table.append([display_name, is_expired, expires_date, memberships])

# sort results for easier viewing
user_table.sort(key=lambda x: x[0])

# print the tabular results
print(tabulate(user_table, headers=['Name', 'Expired?', 'Account Expiry', 'Memberships'],
                           tablefmt='fancy_grid',
                           colalign=('left','center','center','left')))
