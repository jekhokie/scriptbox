#!/bin/bash
#
# Purpose: Perform audit of GCP projects and report on various attributes including creator
#          and creation time.
#
# Requirements: This script requires the `jq` binary be present and in the path, as well as
#               `gcloud` configuration available (see README).
#
# Limitations: There is limited error checking in this script (assumes happy path) and likely
#              needs to be enhanced with boundary and error checking. This script is also not
#              DRY, but this is intentional to allow for rapid local development against the
#              local test file.
#
# Options:
#   * Pass `--test-local` as a command-line switch to utilize the `sample.json` local
#          test file for parsing audit log data.
#   * Pass `--debug` as a command-line switch to print extra details/debug information.


# colors for logs
RESET_COLOR="$(tput sgr0)"
ERROR_COLOR="$(tput setaf 1)"
INFO_COLOR="$(tput setaf 2)"
WARN_COLOR="$(tput setaf 3)"

# outputs and vars corresponding to local testing
AUDITED_JSON="project_audit.json"
LOCAL_PROJECT_LIST="test_data/project_list.json"
LOCAL_LOG="test_data/project_log.json"
LOCAL_ACCOUNT_LIST="test_data/billing_accounts.json"

# variables to hold projects and information
billingAccounts=()
gcpProjects=()
auditedProjects=()

# determine if local test or remote API invocation
local_test=false
debug=false
if [[ $* == *--test-local* ]]; then local_test=true; fi
if [[ $* == *--debug* ]]; then debug=true; fi

# output an informational message (green)
function write_output {
    printf '%s[%s] -- %s%s\n' $INFO_COLOR "$(date)" "${1}" $RESET_COLOR
}

write_output "**START TIME**"

function get_active_billing_accounts {
    write_output "Getting a list of active billing accounts..."

    if [ $local_test = true ]; then
        write_output "Local test - getting list from local file:"
        billingAccounts=( $(cat $LOCAL_ACCOUNT_LIST | jq -r '.[].name') )
    else
        write_output "Querying GCP endpoint..."
        billingAccounts=( $(gcloud beta billing accounts list \
                                --filter="OPEN=True" \
                                --format=json | \
                                  jq -r '.[].name')
                        )
    fi
}

function get_gcp_projects {
    write_output "Getting a list of GCP projects..."

    if [ $local_test = true ]; then
        # the local file method will not use the billing accounts to limit
        # the relational aspects of obtaining projects from billing accounts
        write_output "Local test - getting list from local file:"
        gcpProjects=( $(cat $LOCAL_PROJECT_LIST | jq -r '.[].projectId') )
    else
        write_output "Querying GCP endpoint..."
        for acct in "${billingAccounts[@]}"; do
            gcpProjects+=( $(gcloud beta billing projects list --billing-account=$acct \
                                 --format=json | \
                                   jq -r '.[].projectId') )
        done
    fi

    if [ $debug = true ]; then printf '%s\n' "${gcpProjects[@]}"; fi
}

function get_audited_projects {
    write_output "Getting a list of already-audited projects (to skip)..."

    if test -f "$AUDITED_JSON"; then
        write_output "Audit file exists - checking project IDs:"
        for projectId in $(awk -F',' '{print $1}' $AUDITED_JSON); do
            auditedProjects+=($projectId)
        done
    else
        write_output "Audit file does not exist - creating blank audit file."
        touch $AUDITED_JSON
    fi

    if [ $debug = true ]; then printf '%s\n' "${auditedProjects[@]}"; fi
}

function get_to_audit {
    write_output "Getting a list of projects to audit..."

    if [ ${#auditedProjects[@]} = 0 ]; then
        # if nothing has been audited, audit all projects
        toAudit=("${gcpProjects[@]}")
    else
        # this is not elegant or performant but suits the need
        for i in "${gcpProjects[@]}"; do
            skipElement=false

            for j in "${auditedProjects[@]}"; do
                if [[ $i == $j ]]; then
                    skipElement=true
                    break
                fi
            done

            [ $skipElement = false ] && toAudit+=($i)
        done
    fi

    if [ $debug = true ]; then printf '%s\n' "${toAudit[@]}"; fi
}

function perform_audit {
    write_output "Performing audit of projects..."

    if [ $local_test = true ]; then
        write_output "Running audit locally:"

        for projectId in "${toAudit[@]}"; do
            # query the local file for project details for a specific project
            # note this is only for 1 project detail (to save time/space on creating
            # detailed test project details for each project)
            auditInfo=$(cat $LOCAL_LOG | jq -r '.[0].protoPayload |
                                                  [
                                                    .request.project.name,
                                                    .request.project.createTime,
                                                    .authenticationInfo.principalEmail
                                                  ]
                                                | join(",")')
            echo "${projectId},$auditInfo" >> $AUDITED_JSON
        done
    else
        write_output "Running audit on user-configured GCP organization:"

        # loop over projects, building the query and getting
        # the resulting audit log
        for projectId in "${toAudit[@]}"; do
            write_output "    -- ${projectId}"
            read -r -d '' logQuery <<EOF
resource.type=project AND
logName:"projects/${projectId}/logs/cloudaudit.googleapis.com%2Factivity" AND
resource.labels.project_id="${projectId}" AND
protoPayload.methodName:"CreateProject" AND
timestamp>="2007-01-01T00:00:00Z"
EOF
            auditInfo=$(gcloud logging read "$logQuery" \
                                       --project="${projectId}" \
                                       --format=json \
                                       --limit=1 | \
                           jq -r '.[0].protoPayload |
                                    [
                                     .request.project.name,
                                       .request.project.createTime,
                                       .authenticationInfo.principalEmail
                                    ]
                                  | join(",")')
            echo "${projectId},$auditInfo" >> $AUDITED_JSON
        done
    fi
}

##### MAIN EXECUTION #####

# get a list of open/active billing accounts
get_active_billing_accounts

# get a list of current GCP project IDs
get_gcp_projects

# get a list of projects already audited (to skip)
get_audited_projects

# determine which projects to query for audit information
# (those that have not yet been queried)
get_to_audit

# query detailed project information and append CSV
# with audit details for each project
perform_audit

write_output "All results written to $AUDITED_JSON"
write_output ""
write_output "**END TIME**"
