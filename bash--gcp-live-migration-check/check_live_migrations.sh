#!/bin/bash
#
# Purpose: Perform a query of GCP system_event logs for all GCP live migrations that have
#          occurred since the start of the day (GMT) and print the results including the
#          date/time (local time zone) and host/resource that was migrated.
#
# Simply update the configs in the file config/settings.sh (copy from config/settings.sh.sample)
# and run the script:
#
#   ./check_live_migrations.sh
#
# Options:
#   * Pass `--test-local` as a command-line switch to utilize the `migration_events.json` local
#          test file for parsing system_event log data.
#
#   # to run a test using the local test file
#   ./check_live_migrations.sh --test-local

# colors for logs
RESET_COLOR="$(tput sgr0)"
ERROR_COLOR="$(tput setaf 1)"
INFO_COLOR="$(tput setaf 2)"

# sample file for local file testing
LOCAL_EVENTS="test_data/migration_events.json"

# variables
migrationEvents=()

# determine if local test or remote API invocation
local_test=false
if [[ $* == *--test-local* ]]; then local_test=true; fi

# output an informational message (green)
function write_output {
    printf '%s[%s] -- %s%s\n' $INFO_COLOR "$(date)" "${1}" $RESET_COLOR
}

# source configured settings
configFile="config/settings.sh"
if [ -f $configFile ]; then
    source config/settings.sh
else
    printf '%s[%s] -- %s%s\n' $ERROR_COLOR "$(date)" "Please create config/settings.sh and configure for your environment." $RESET_COLOR
    exit 1
fi

# get shared functions
source lib/functions.sh

write_output "**START TIME**"

##### MAIN EXECUTION #####

# perform query of system_event log
curDate=$(date -j +"%F")
get_live_migration_events $curDate

# print results of any migrations
if [[ ${#migrationEvents[@]} > 0 ]]; then
    write_output "List of migration events that have occurred since start of day (GMT):"
    print_current_day_migration_results
else
    write_output "No migration events since start of day (GMT)."
fi

write_output "**END TIME**"
