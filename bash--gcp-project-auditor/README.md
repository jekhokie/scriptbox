# GCP Project Auditor

GCP projects can become unwieldly, especially if the GSuite integration is not managed properly
(where GSuite API interaction results in projects being created under the same organization as
your GCP infrastructure projects). This script attempts to get a list of all projects and, using
the project ID, iteratively query stackdriver to obtain information about who created each project
(and a timestamp of when it was created). Additionally, this script only incrementally updates
information since project creation is an atomic operation and only new projects need to be updated
in the resulting JSON.

## Requirements

The person or service account running this script *must* be a GCP Organization owner (or similar
permissions), and have access to view all billing accounts for the Organization in order to
successfully get information about the entire landscape of the GCP account being audited. In
addition, this script expects the environment of the user/service running the script to
be adequately configured to run `gcloud` commands and interact with GCP at this level. In a future
state, this script should likely be converted into more of a library-based interaction with GCP
using API credentials rather than human/service account credentials over `gcloud` commands.

## Prerequisites

The only prerequisite for this script to function is the presence/availability of the `jq` binary.

## Usage

Simply execute the script and the GCP organization (and respective projects) will be queried, with
information about each appended to the JSON file `project_audit.json`. Note that the very first run
of this script is likely to take some time based on needing to build out the entire list, but as
time goes on (and this is run more frequently), only incremental updates to the JSON will be made.

```bash
$ ./audit_projects.sh
```

You can also pass the following command-line switches:

* `--test-local`: Use the local test files rather than interacting with GCP directly (good for local
debugging/troubleshooting).
* `--debug`: Print extra debug information helpful during development and troubleshooting.

## Limitations

This script has some serious limitations but is sufficient for the immediate need. Specifically:

1. **DRY Code**: The code between test cases/local dev and actual GCP interaction is not DRY.
2. **Efficiency**: There are multiple areas for improvement (array searching, etc.) where brute-force
was used to accomplish the task.
3. **Deleted projects**: This script does not currently support updating the audited project list
to remove deleted projects (i.e. if you delete a project in GCP and incrementally update your audit
list, the deleted project will simply remain in the resulting CSV file).
4. **Stackdriver APIs**: The script does not handle enabling Stackdriver APIs in the projects being
queried (you will be prompted to enable logging on each project you wish to query). This is purposeful
given it may not be desirable to enable the logging APIs.
5. **Billing-Associated Accounts**: By default, the script only queries those projects that have an
associated active billing account (said more succinctly, it will only query active billing account
associated projects).
6. **Slow**: Given the search range historically, queries against Stackdriver logging can take a long
time to return the initial/first log. The project-based querying may appear to "hang" - give it a few
minutes and you should see the response and the script moving on to the next project.
