#!/usr/bin/env python
#
# Purpose: Query a configured Jira API and run some calculations to map
# resulting issues to an output CSV and print out useful metrics/info.
#

import argparse
import csv
import pandas as pd
import pickle
import yaml
from datetime import datetime, timedelta
from os.path import exists
from jira import JIRA

# load configs
with open('config/settings.yml', 'r') as yml:
    config = yaml.load(yml, Loader=yaml.FullLoader)

# parse user-defined arguments
parser = argparse.ArgumentParser(description='Parse Jira project for useful statistics')
parser.add_argument('-f', action='store_true', default=False, dest='force_jira', help='Force a Jira lookup even if there is a local serialized copy of the last run data - this method is slower due to the round-trip Jira network call')
parser.add_argument('-v', action='store_true', default=False, dest='print_json', help='Pretty-print resulting dictionary of Jira attributes to screen')
args = parser.parse_args()

def get_resolved_date(issue):
    '''
    Get the resolved date, where resolved date could be the actual resolutiondate field
    if the issue was resolved correctly, or the last updated date field if the issue is in
    a 'Done' status but not resolved.
    '''

    res_date = issue.fields.updated
    if issue.fields.resolutiondate:
        res_date = issue.fields.resolutiondate

    return res_date

def get_jira_issues():
    '''
    Get Jira issues whether it be from a local cached serialized copy, or through the Jira API
    '''

    # take local serialized/cached data if available for speedier development,
    # or force Jira lookup if switch to force is provided
    cached_issues = "cache/jira_issues.pickle"
    issues = []
    if exists(cached_issues) and args.force_jira == False:
        print("Getting issues from cached local file...")
        with open(cached_issues, "rb") as infile:
            issues = pickle.load(infile)
    else:
        print("Getting issues from Jira (no cached/local copy)...")
        jira = JIRA(config['jira_server'], basic_auth=(config['jira_user'], config['jira_pass']))
        jira_query = 'project={} AND type={}'.format(config['jira_project'], config['jira_issue_type'])
        issues = jira.search_issues(jira_query, maxResults=-1)
        with open(cached_issues, "wb") as outfile:
            pickle.dump(issues, outfile)

    return issues

def map_jira_issues(issues):
    '''
    Map the gathered Jira issues to a custom dictionary for parsing
    '''

    issue_dict = []
    for issue in issues:
        # determine time to close - don't care about time zone, so strip that out
        created_date = datetime.strptime(issue.fields.created.split(".")[0], '%Y-%m-%dT%H:%M:%S')
        closed_date = datetime.strptime(get_resolved_date(issue).split(".")[0], '%Y-%m-%dT%H:%M:%S')
        time_to_close = closed_date - created_date

        # get the creator and assignee if available
        reporter = '' if issue.fields.reporter is None else issue.fields.reporter.displayName
        assignee = '' if issue.fields.assignee is None else issue.fields.assignee.displayName

        # append to custom dict structure
        issue_dict.append({'key': issue.key,
                           'link': issue.self,
                           'reporter': reporter,
                           'assignee': assignee,
                           'summary': issue.fields.summary,
                           'status': "{}".format(issue.fields.status),
                           'created': created_date.strftime('%Y-%m-%dT%H:%M:%S'),
                           'closed': closed_date.strftime('%Y-%m-%dT%H:%M:%S'),
                           'time_to_close': str(time_to_close)})

    return issue_dict

def print_jira_issue_stats(issues):
    '''
    Print some basic information about the Jira issues (how many total, open, closed, how long
    it took on average to close issues, etc.)
    '''

    # create a dataframe from the issue list
    # NOTE: This is overkill for current calculation methods, but sets a good groundwork for
    #       more complex future work that can be done with the dataframe
    df_issues = pd.DataFrame.from_dict(issues)
    df_issues['created'] = pd.to_datetime(df_issues['created'], format='%Y-%m-%dT%H:%M:%S')
    df_issues['closed'] = pd.to_datetime(df_issues['closed'], format='%Y-%m-%dT%H:%M:%S')

    # calculate stats
    open_issues = df_issues[df_issues['status'] != 'Done']
    closed_issues = df_issues[df_issues['status'] == 'Done']
    avg_close_time = (df_issues.closed - df_issues.created).mean()

    # tally montly summaries for per-month metrics
    monthly_summary = pd.DataFrame()
    monthly_summary['created'] = df_issues['key'].groupby(df_issues['created'].dt.to_period('M')).count()
    monthly_summary['closed'] = df_issues[df_issues['status'] == 'Done']['key'].groupby(df_issues['closed'].dt.to_period('M')).count()
    avg_closed_per_month = round(monthly_summary['closed'].mean())
    avg_opened_per_month = round(monthly_summary['created'].mean())

    # print resulting stats
    print("  ISSUE STATS:")
    print("  ~~~~~~~~~~~~")
    print("    Total:                {}".format(len(issues)))
    print("    Open:                 {}".format(len(open_issues)))
    print("    Closed:               {}".format(len(closed_issues)))
    print("    Avg. Opened/Month:    {}".format(avg_opened_per_month))
    print("    Avg. Closed/Month:    {}".format(avg_closed_per_month))
    print("    Avg. Time to Resolve: {}".format(avg_close_time))
    print("  ~~~~~~~~~~~~")

def write_jira_issues_to_csv(issues, result_file):
    '''
    Dump the resulting custom dictionary of Jira issues to a CSV file
    '''

    # write the issues to a CSV file if there are issues in the array
    if len(issues) > 0:
        with open(result_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=issues[0].keys())
            writer.writeheader()
            writer.writerows(issues)

def main():
    '''
    Main execution method
    '''

    # get the Jira issues either from local cache or Jira API
    issues = get_jira_issues()

    # map the Jira fields to the custom structure
    issue_dict = map_jira_issues(issues)

    # output some basic statistics about the data set
    print_jira_issue_stats(issue_dict)

    # print resulting JSON if user requested it
    if args.print_json == True:
        import json
        print(json.dumps(issue_dict, indent=4, sort_keys=True))

    # write the resulting custom structure to a CSV file
    result_file = 'output/results.csv'
    write_jira_issues_to_csv(issue_dict, result_file)
    print("Results stored in {}".format(result_file))

if __name__ == '__main__':
    main()
