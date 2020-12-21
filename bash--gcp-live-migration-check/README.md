# GCP Live Migration Check

GCP live migrations have been known to be impactful to some workloads. This script queries the
GCP `system_event` log for all live migration events that have occurred since the start of the
day (GMT time) and reports a list of local timings and hostnames that had been migrated to help
with troubleshooting efforts.

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

The only prerequisite for this script to function is the presence/availability of the `jq` binary.

## Usage

First, create a copy of `config/settings.sh.sample` as `config/settings.sh` and update the permissions
to protect any sensitive information:

```bash
$ cp config/settings.sh.sample config/settings.sh
# edit the config/settings.sh to suit your needs
$ chmod 600 config/settings.sh
```

Then, simply execute the script and the GCP project Stackdriver logs will be queried, with information about
each event printed to the terminal:

```bash
$ ./check_live_migrations.sh
```

You can also pass the following command-line switches:

* `--test-local`: Use the local test files rather than interacting with GCP directly (good for local
debugging/troubleshooting).
