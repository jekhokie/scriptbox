#!/bin/bash
#
# Purpose: Display a list of live migrations that have occurred week over week for USER_DEFINED
#          number of weeks.
#
# Simply update the configs in the file config/settings.sh (copy from config/settings.sh.sample)
# and run the script, providing the number of weeks back to query for, week-over-week:
#
#   ./live_migration_history.sh 12

# Options:
#   * Pass `--test-local` as a command-line switch to utilize the test files in the `test_files/`
#     directory for parsing system event data.
#   * Pass `--plot` to optionally/additionally plot a terminal graph of the results.
#
#   # to run a test using the local test file
#   ./live_migration_history.sh 2 --test-local

#   # to run a test using the local test file and plot the results
#   ./live_migration_history.sh 2 --test-local --plot
#
#   # to plot real results in addition to showing the table
#   ./live_migration_history.sh 2 --plot
#

# colors for logs
RESET_COLOR="$(tput sgr0)"
ERROR_COLOR="$(tput setaf 1)"
INFO_COLOR="$(tput setaf 2)"

local_test=false
should_plot=false
if [[ $* == *--test-local* ]]; then local_test=true; fi
if [[ $* == *--plot* ]]; then should_plot=true; fi

# ensure the user specified a number of weeks to query
if [ "$#" -lt 1 ]; then
    printf '%s[%s] -- %s%s\n' $ERROR_COLOR "$(date)" "Usage: ./live_migration_history.sh <NUM_WEEKS_BACK> [--test-local] [--plot]" $RESET_COLOR
    exit 1
elif [ $1 -eq 1 ]; then
    printf '%s[%s] -- %s%s\n' $ERROR_COLOR "$(date)" "This script is intended for trending - for 1 week of data, use ./check_live_migrations.sh" $RESET_COLOR
    exit 1
else
    num_weeks=$1
fi

# source configured settings
configFile="config/settings.sh"
if [ -f $configFile ]; then
    source config/settings.sh
else
    printf '%s[%s] -- %s%s\n' $ERROR_COLOR "$(date)" "Please create config/settings.sh and configure for your environment." $RESET_COLOR
    exit 1
fi

# output an informational message (green)
function write_output {
    printf '%s[%s] -- %s%s\n' $INFO_COLOR "$(date)" "${1}" $RESET_COLOR
}

# get shared functions
source lib/functions.sh

write_output "**START TIME**"
write_output "Querying for ${num_weeks} weeks back, week-over-week..."

# iterate over each week of data, capturing migrations
migrationTrends=()
if [[ "${local_test}" == 'true' ]]; then
    for f in "migrations_week_1.json" "migrations_week_2.json"; do
        if [[ "${f}" == "migrations_week_1.json" ]]; then
            startDate="2020-11-14"
            endDate="2020-11-20"
        else
            startDate="2020-11-21"
            endDate="2020-11-27"
        fi

        migration_events=()
        LOCAL_EVENTS="test_data/${f}"
        get_live_migration_events

        # parse the migration events
        migrationTrends+=("${startDate}\n${endDate} ${#migrationEvents[@]}")
    done
else
    for i in $(seq 1 $num_weeks); do
        migration_events=()

        # establish start and end date
        startDate=$(date -j -v-${i}w +"%F")
        endDate=$(date -j -v-$((i-1))w -v-1d +"%F")

        # perform the query
        write_output "Querying for ${startDate} -> ${endDate}..."
        get_live_migration_events $startDate $endDate

        # parse the migration events
        migrationTrends+=("${startDate}\n${endDate} ${#migrationEvents[@]}")
    done
fi

# output the results in a tabular format
print_migration_trends

# optionally, output a bar graph
if [[ "${should_plot}" == 'true' ]]; then
    trendsDB=$(printf "%s\n" "${migrationTrends[@]}")
    graph_migration_trends
fi
