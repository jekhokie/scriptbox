# Delphix Manage Users

At the time of this project, Delphix does not have the ability to utilize Active Directory/LDAP
security groups for managing users. This can be cumbersome for enterprises that want a
centralized, source-based user management for who should/should not have access to the tool.
Additionally, it is extra painful if there are multiple Delphix engines and many users that
need access.

This script intends to manage the life cycle of users for multiple Delphix engines. It will
start as a utility which compares and updates users in each engine specified and will hopefully
evolve into a much more sophisticated user management utility.

*NOTE*: This utility assumes that your desired end state is a set of Delphix engines with users
specified that authenticate using LDAP with their Active Directory/LDAP credentials.

## Prerequisites

Install easy_install, pip and virtualenv. Then, clone this repository and navigate to this example:

```bash
$ git clone https://<git_location>/scriptbox.git
$ cd scriptbox/python--delphix-manage-users/
```

Install the required environment and libraries:

```bash
$ virtualenv --no-site-packages --distribute .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```

Create a configuration file from the sample and specify the values for your specific environment.
This particular configuration will be our source for the Delphix engine specifications:

```bash
$ cp config/settings.conf.sample config/settings.conf
# edit the config/settings.conf file for your environment
```

Next, create your file containing the users you wish to add to the Engines. Note that this file
expects a very specific format. The `bin` directory in this project contains an executable
dxtoolkit binary which expects the format in this project so as to pin the version of binary
required. Note that this may go out of date over time and will likely need to be updated as
newer versions of dxtoolkit and Delphix come out, but is a likely decent starting point:

```bash
$ cp config/users.csv.sample config/users.csv
# edit the config/users.csv file for the user information of the users you wish to create
```

Note that this CSV file is *NOT* the same format as what the dxtoolkit expects - instead, this
file is a *definitive* list of all users that require access to each engine. This wrapper
script/project is specifically intended to take this configuration file and interact with each
Delphix engine to align the engine permissions/users with the users specified in this file.

Finally, download the dxtoolkit binary for your operating system and place it into the `bin/`
directory named `dxtoolkit`. At the time of writing this script, the compatible version is
2.3.7 and can be found [here](https://github.com/delphix/dxtoolkit/releases/tag/v2.3.7).

```bash
$ cd bin/
$ wget https://github.com/delphix/dxtoolkit/releases/tag/v2.3.7/<YOUR_OS_VERSION>.tar.gz
$ tar -xzvf <YOUR_OS_VERSION>.tar.gz
$ mv dxtoolkit2/* .
$ rm -rf dxtoolkit2
```

## Usage

Now that the configurations are in place, run the script to align the Delphix engine users with
the users that have been specified in the respective configuration file:

```bash
$ python align_users.py
# you should see output corresponding to the actions being taken on each of
# the users specified in the previous CSV file
```
