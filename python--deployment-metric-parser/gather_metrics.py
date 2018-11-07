#!/usr/bin/env python
#
# Purpose: Parse Excel documents in the tests directory and produce
#          useful metrics for inspection.
#
# TODO: There are a lot of areas of improvement - specifically:
#    - Validate summary worksheet exists, named "Summary", with required fields/values
#    - Validate playbook worksheet exists, named "Playbook", with required columns
#    - Validate task States worksheet exists (drop-downs for "Status" fields)
#    - De-normalize playbook metrics - currently duplication for easily pulling data out/sorting

import glob
import os
import xlrd
import yaml
from datetime import datetime, timedelta
from enum import Enum
from jinja2 import Environment, FileSystemLoader

# load configuration settings
with open('config/settings.yml', 'r') as yml:
  config = yaml.load(yml)

# name of the HTML file to output when rendering graphs
input_html_j2 = "index.html.j2"
output_html_file = "html_output/index.html"

# classify each of the possible Excel Cell types
class ExcelCellType(Enum):
    empty = 0
    text = 1
    number = 2
    date = 3
    boolean = 4
    error = 5
    blank = 6

class ColNames(Enum):
    procstep = 0
    task = 1
    step = 2
    est_start_date = 3
    est_start = 4
    est_end = 5
    assignee = 6
    status = 7
    act_start_date = 8
    act_start = 9
    act_end = 10
    act_minutes = 11
    errors = 12
    notes = 13

# store the expected columns in the Excel document
EXPECTED_COLS = [ "process step", "task", "step", "estimated start date", "estimated start time", "estimated end time", "assignee",
                  "status", "actual start date", "actual start time", "actual end time", "actual duration (minutes)", "errors", "additional notes" ]

# array for storing the metrics about each deployment
pb = []

# validate that the playbook has the required columns and ordering required
def validate_columns(sheet):
    cols = sheet.row_slice(rowx=0, start_colx=0, end_colx=None)

    # ensure the number of columns expected match
    if len(cols) != len(EXPECTED_COLS):
        raise(Exception("Number of columns required does not match document."))

    # check each column name for validity/order
    i = 0
    for cell in cols:
        if EXPECTED_COLS[i] != cell.value.lower().replace('\n', ' ').replace('\r', ' '):
            raise(Exception("Column '{}' in position {} does not match expected column '{}'".format(cell.value.lower(), i, EXPECTED_COLS[i])))
        i += 1

# convert what is the Excel time into a time-formatted object for the
# purposes of calculating metrics - Excel reports "fraction of a day"
# when retrieving a time cell, which needs to be converted into respective
# hours, minutes, and seconds
#
# NOTE: Eventually explore xldate_as_tuple - will condense entire function
def excel_time_to_datetime(t):
    if t.ctype == ExcelCellType.text:
        return datetime.strptime("".join(t.value.split()), "%I:%M%p")
    elif t.ctype == ExcelCellType.date:
        # should never happen (as this would mean the time reflects more than 1 day)
        # but good defensive coding just in case
        if t.value > 1:
            t.value = t.value % 1

        # convert respective components to hours and minutes (don't care about seconds
        # as that is likely too granular to start - will just add percent error that will
        # only be significant much later in the metric gathering)
        seconds = round(t.value * 86400)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)

        return datetime.strptime("%d:%d" % (hours, minutes), "%H:%M")
    else:
        raise(Exception("Expecting {} to be either a text or date type - received {} type".format(t.value, t.ctype)))

# parse all playbooks in directory - exclude tilde-starting files indicating
# the file may be open for editing (not a valid use case)
for file in [f for f in glob.glob("tests/*") if not os.path.basename(f).startswith('~')]:
    # output for troubleshooting
    print("Processing: {}".format(file))

    # open the file and get the summary and playbook worksheets
    wb = xlrd.open_workbook(file)
    summary = wb.sheet_by_name("Summary")
    sheet = wb.sheet_by_name("Playbook")

    # pull metadata out of the worksheets
    customer = summary.cell(0, 1).value
    cust_env = summary.cell(1, 1).value
    start_date = datetime(*xlrd.xldate_as_tuple(summary.cell(2, 1).value, wb.datemode))
    started = start_date.strftime("%m/%d/%y")
    installer_version = summary.cell(4, 1).value
    lead_installer = summary.cell(5, 1).value

    # create a deployment object for metric storage
    current_pb = { 'customer': customer,
                   'env': cust_env,
                   'installer': installer_version,
                   'lead': lead_installer,
                   'started': started,
                   'steps': { } }

    # parse each step in the playbook
    for i in range(0, sheet.nrows):
        try:
            # validate columns before proceeding
            if i == 0:
                validate_columns(sheet)
                continue

            # gather row metrics
            actual_vals = sheet.row_slice(rowx=i, start_colx=0, end_colx=None)

            try:
                # get process step and initialize metrics
                pmap = actual_vals[ColNames.procstep]
                if pmap.ctype in {ExcelCellType.blank, ExcelCellType.empty}:
                    # if there is no process map step specified, skip this row
                    continue
                else:
                    pmap = pmap.value.lower()
                    if pmap not in current_pb['steps']:
                        current_pb['steps'][pmap] = {'occurs': 1, 'cum_time': 0, 'min_time': None, 'min_step_number': '',
                                                     'max_time': None, 'max_step_number': '', 'avg_time': 0, 'errors': '', 'notes': ''}
                    else:
                        current_pb['steps'][pmap]['occurs'] += 1

                # get actual start and end times OR duration
                start_time = actual_vals[ColNames.act_start]
                end_time = actual_vals[ColNames.act_end]
                actual_minutes = actual_vals[ColNames.act_minutes]

                # determine whether to use minutes or timeframes
                t_delta = 0
                if start_time.ctype in {ExcelCellType.blank, ExcelCellType.empty} or end_time.ctype in {ExcelCellType.blank, ExcelCellType.empty}:
                    if actual_minutes.ctype in {ExcelCellType.blank, ExcelCellType.empty}:
                        raise(Exception("No start/end time or duration (minutes)"))
                    else:
                        t_delta = actual_minutes.value
                else:
                    t_start = excel_time_to_datetime(actual_vals[ColNames.act_start])
                    t_end = excel_time_to_datetime(actual_vals[ColNames.act_end])

                    # handle when day rolls over to next day
                    if t_end < t_start:
                        t_end += timedelta(days=1)

                    # calculate time delta for step
                    t_delta = (t_end - t_start).total_seconds() / 60.0

                # easier variables
                step = current_pb['steps'][pmap]
                task_number = actual_vals[ColNames.task].value

                # add cumulative time, errors, and notes
                step['cum_time'] += t_delta
                ct = actual_vals[ColNames.errors].ctype
                if ct not in {ExcelCellType.empty, ExcelCellType.blank}:
                    step['errors'] += ">" + actual_vals[ColNames.errors].value

                # if time delta is greater than last known delta, specify this as longest
                if t_delta > step['max_time'] or step['max_time'] is None:
                    step['max_time'] = t_delta
                    step['max_step_number'] = task_number

                # if time delta is less than last known delta, specify this as shortest
                if t_delta < step['min_time'] or step['min_time'] is None:
                    step['min_time'] = t_delta
                    step['min_step_number'] = task_number

                # update the average duration
                step['avg_time'] = step['cum_time'] / step['occurs']
            except Exception, e:
                raise(Exception("Error on row {}: {}".format(i+1, e)))
        except Exception, e:
            raise(Exception("ERROR: {} has error: {}".format(file, e.message)))

    # store metrics for current deployment
    pb.append(current_pb)

# before we do a data presentation, let's sort our deployments
pb = sorted(pb, key=lambda k: k['started'])

##################
# OUTPUT RESULTS #
##################
for deploy in pb:
    print("---------------------------------------------------")
    print("CUSTOMER:      {0:<s}".format(deploy['customer']))
    print("ENVIRONMENT:   {0:<s}".format(deploy['env']))
    print("DATE:          {0:<s}".format(deploy['started']))
    print("INSTALLER VER: {0:<s}".format(str(deploy['installer'])))
    print("LEAD:          {0:<s}".format(deploy['lead']))
    print("TIMINGS (IN MINUTES):")
    for key in sorted(deploy['steps']):
        p = deploy['steps'][key]
        print("  - {0:s} | CUM: {1:>4.0f} | AVG: {2:>4.0f} | MIN: {2:>4.0f} | MAX: {3:>4.0f}".format(key, p['cum_time'], p['avg_time'], p['min_time'], p['max_time']))
    print("---------------------------------------------------")

######################
# OUTPUT HTML GRAPHS #
######################
# create colors for random use
colors = [ 'rgb(255, 99, 132)',
           'rgb(255, 159, 64)',
           'rgb(255, 205, 86)',
           'rgb(75, 192, 192)',
           'rgb(54, 162, 235)',
           'rgb(153, 102, 255)',
           'rgb(201, 203, 207)' ]

# create labels for the last 30 days of calendar from end date
end_date = datetime.strptime(config['end_date'], "%m/%d/%y")
date_labels = [(end_date + timedelta(days=-x)).strftime("%m/%d/%y") for x in range(config['graph_days'], 0, -1)]

# parse each step into an object for both date-focused as well as step-focused
data_by_date = {}
data_by_step = {}
for d in pb:
    # add a date dict to store metrics if not already there
    if d['started'] not in data_by_date:
        data_by_date[d['started']] = {'process_steps': {}, 'deployments': 0}

    # record an increase in the number of deployments for this date
    d_date_data = data_by_date[d['started']]
    d_date_data['deployments'] += 1
    d_date_data = d_date_data['process_steps']

    # add the process map step metrics to the date
    for step in d['steps']:
        cumulative_time = d['steps'][step]['cum_time']
        occurs = d['steps'][step]['occurs']

        # first, add the metrics to the data for the particular date
        if step not in d_date_data:
            d_date_data[step] = {'cumulative_time': 0, 'occurs': 0}

        d_date_data[step]['cumulative_time'] += cumulative_time
        d_date_data[step]['occurs'] += occurs

        # next, add the metrics to the data for the particular step
        if step not in data_by_step:
            data_by_step[step] = {'cumulative_time': 0, 'occurs': 0}

        data_by_step[step]['cumulative_time'] += cumulative_time
        data_by_step[step]['occurs'] += occurs

# METADATA: PROVIDE SOME BASIC METADATA ABOUT THE GRAPH DATA
total_minutes = sum(data_by_step[d]['cumulative_time'] for d in data_by_step)
metadata = {
             'total_days': config['graph_days'],
             'total_minutes': total_minutes,
             'total_hours': total_minutes / 60,
             'average_minutes': total_minutes / len(pb),
             'average_hours': total_minutes / 60 / len(pb),
             'total_deploys': len(pb)
           }

# GRAPH 1: PIE CHART WITH BREAKDOWN OF PER-PROCESS-STEP TOTAL MINUTES
# GRAPH 3: "AVERAGES" ON A POLAR CHART FOR EACH PROCESS STEP
pie_data = []
pie_colors = []
pie_labels = []
polar_data = []
polar_colors = []
polar_labels = []
for i, step_name in enumerate(sorted(data_by_step)):
    step_data = data_by_step[step_name]

    # save the cumulative time for the pie chart
    pie_data.append(step_data['cumulative_time'])
    pie_colors.append(colors[(i % len(colors))])
    pie_labels.append(" {}".format(str(step_name)))

    # save the average time for the polar chart
    polar_data.append("%.2f" % (step_data['cumulative_time'] / step_data['occurs']))
    polar_colors.append(colors[(i % len(colors))])
    polar_labels.append(" {}".format(str(step_name)))

# GRAPH 2: BAR GRAPH WITH STACKED PROCESS STEP MINUTES PER DATE
stacked_ds = []

# add the number of deployments line data
num_deployments = {
                    'label': '# Deployments',
                    'fill': 'false',
                    'backgroundColor': '#006600',
                    'borderColor': '#006600',
                    'borderDash': [5, 5],
                    'type': 'line',
                    'yAxisID': 'yAxisRight',
                    'data': []
                  }
stacked_ds.append(num_deployments)

# add the respective process steps
for i, step in enumerate(sorted(data_by_step.keys())):
    stacked_ds.append({
                        'label': str(step),
                        'backgroundColor': colors[(i % len(colors))],
                        'yAxisID': 'yAxisLeft',
                        'data': []
                      })

for d in date_labels:
    if d in data_by_date:
        for s in stacked_ds:
            if s['label'] in data_by_date[d]['process_steps']:
                s['data'].append(data_by_date[d]['process_steps'][s['label']]['cumulative_time'])
            elif s['label'] != '# Deployments':
                s['data'].append(0)

        num_deployments['data'].append(data_by_date[d]['deployments'])

    else:
        for s in stacked_ds:
            s['data'].append(0)

# GRAPH 4: TREND OF DAILY TIME PER UPGRADE FOR TOP 5 PROCESS STEPS
sorted_cum_time = sorted(data_by_step, key=lambda x: data_by_step[x]['cumulative_time'])
line_chart = []
for i in [-5, -4, -3, -2, -1]:
    data = []
    process_to_plot = sorted_cum_time[i]
    data = {
             'label': str(process_to_plot),
             'fill': 'false',
             'backgroundColor': colors[(i % len(colors))],
             'borderColor': colors[(i % len(colors))],
             'lineTension': 0,
             'data': data
           }

    # find all occurrences of the process step to plot
    for d in date_labels:
        if d in data_by_date:
            if process_to_plot in data_by_date[d]['process_steps']:
                data['data'].append(data_by_date[d]['process_steps'][process_to_plot]['cumulative_time'] / data_by_date[d]['deployments'])
            else:
                data['data'].append('NaN')
        else:
            data['data'].append('NaN')

    line_chart.append(data)

# output HTML with data
j2_env = Environment(loader=FileSystemLoader("templates"), trim_blocks=True)
template = j2_env.get_template(input_html_j2)
with open(output_html_file, "wb") as fh:
    fh.write(template.render(metadata=metadata,
                             pie_labels=pie_labels, pie_data=pie_data, pie_colors=pie_colors,
                             stacked_labels=date_labels, stacked_ds=stacked_ds,
                             polar_data=polar_data, polar_colors=polar_colors, polar_labels=polar_labels,
                             line_chart=line_chart))
