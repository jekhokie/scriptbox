# GCP Live Migration Check

GCP live migrations have been known to be impactful to some workloads. There are multiple pieces
of functionality in this repository to help with some troubleshooting:

1. `check_live_migrations.sh`: This script queries the GCP `system_event` log for all live migration
events that have occurred since the start of the current day (GMT time) and reports a list of local
timings and hostnames that had been migrated to help with troubleshooting efforts.
2. `live_migration_history.sh`: This script accepts a number of weeks and will query the number of
GCP live migrations events that have occurred each week previous to the current day, back to the
number of weeks specified, and print (and optionally graph) the results.

## Requirements

* Stackdriver APIs enabled.
* Access to the GCP project being queried, and specifically access to Stackdriver logs.
* Command line environment adequately configured to run `gcloud` commands, including the project
you wish to run the command within.

In order to accomplish the environment configurations, ensure that you run (for example) the following
types of commands:

```bash
# authenticate
$ gcloud auth login
```

## Required Libraries

* All scripts require the `jq` binary.
* `live_migration_history.sh` requires `gnuplot` if you wish to plot the results.

## Usage

First, create a copy of `config/settings.sh.sample` as `config/settings.sh` and update the permissions
to protect any sensitive information:

```bash
$ cp config/settings.sh.sample config/settings.sh
# edit the config/settings.sh to suit your needs
$ chmod 600 config/settings.sh
```

Then, depending on which script you wish to use, ensure the parameters required are passed in - some examples:

```bash
# check and print migration events for current day
$ ./check_live_migrations.sh

# use the local test files instead of querying the GCP API
$ ./check_live_migrations.sh --test-local

# print historical migration events for the
# last 6 weeks leading up to current day
$ ./live_migration_history.sh 6

# print and plot historical migration events for the
# last 6 weeks leading up to current day
$ ./live_migration_history.sh 6 --plot

# use the local test files instead of querying the GCP API
$ ./live_migration_history.sh 6 --test-local
```

## Disclaimer

This functionality is ROUGH - function calls and return arguments are kind of all over the place and the
use of variables is crude at best. This functionality requires a refactor to pretty it up, but serves its
purpose for the time being, so may never get it.
