# LDAP List Users Data

Python functionality to take configuration for connecting to an LDAP endpoint and a list of names
to query in the LDAP target and print information such as name, account expiration date, whether an
account is expired, and group memberships for the user. This script is useful for debugging or
keeping track of users in an LDAP/AD environment.

## Assumptions

This script is purpose-built and makes assumptions such as simple authentication being allowed at
the remote LDAP endpoint, the user you're using having permission to query all the attributes being
gathered, etc. This may not suit your needs and you may need to update the script to accommodate
your environment and permissions.

## Prerequisites

Install easy_install, pip and virtualenv. Then, clone this repository and navigate to this example:

```bash
$ git clone https://<git_location>/scriptbox.git
$ cd scriptbox/python--ldap-list-users-data/
```

Install the required environment and libraries:

```bash
$ virtualenv --no-site-packages --distribute .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```

## Configuration

Configure the settings for your environment:

```bash
# make a copy of the example settings file
$ cp config/settings.yml.sample config/settings.yml

# edit the file for your environment
$ vim config/settings.yml

# lock the configuration file down since it has sensitive
# bind information about your remote LDAP environment
$ chmod 600 config/settings.yml
```

## Usage

Execute the query script and a table with the resulting information should be printed for the users
you configured in `config/settings.yml`:

```bash
./get_ldap_info.py
```

There are some additional options available when running the script - see below or use the `-h` argument:

```bash
# get information about usage
./get_ldap_info.py -h

# get group information for each user
./get_ldap_info.py -g

# get debug information as the script runs
./get_ldap_info.py -d
```
