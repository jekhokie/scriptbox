#!/usr/bin/env python
#
# Purpose: Parse Excel documents in the tests directory and produce
#          useful metrics for inspection.
#

import glob
import os
import xlrd
from datetime import datetime, timedelta
from enum import Enum

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
    est_start = 3
    est_end = 4
    assignee = 5
    status = 6
    act_start = 7
    act_end = 8
    notes = 9

# store the expected columns in the Excel document
EXPECTED_COLS = ["process step", "task", "step", "estimated start time", "estimated end time", "assignee",
                 "status", "actual start time", "actual end time", "notes" ]

# validate that the playbook has the required columns and ordering required
def validate_columns(sheet):
    cols = sheet.row_slice(rowx=0, start_colx=0, end_colx=None)

    # ensure the number of columns expected match
    if len(cols) != len(EXPECTED_COLS):
        raise(Exception("Number of columns required does not match document."))

    # check each column name for validity/order
    i = 0
    for cell in cols:
        if EXPECTED_COLS[i] != cell.value.lower():
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
    # TODO: Validation for format expectations:
    #    - Summary worksheet exists, named "Summary", with required fields/values
    #    - Playbook worksheet exists, named "Playbook", with required columns
    #    - Task States worksheet exists (drop-downs for "Status" fields)

    # open the file and get the summary and playbook worksheets
    wb = xlrd.open_workbook(file)
    summary = wb.sheet_by_name("Summary")
    pb = {'customer': summary.cell(0, 1).value, 'date': summary.cell(1, 1).value, 'steps': {}}
    sheet = wb.sheet_by_name("Playbook")

    # get metadata about the deployment
    pb['customer'] = summary.cell(0, 1).value
    pb['environment'] = summary.cell(1, 1).value
    start_date = datetime(*xlrd.xldate_as_tuple(summary.cell(2, 1).value, wb.datemode))
    pb['date'] = start_date.strftime("%m/%d/%y")
    pb['installer'] = summary.cell(5, 1).value
    pb['lead'] = summary.cell(6, 1).value

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
                if pmap.ctype == ExcelCellType.blank or pmap.ctype == ExcelCellType.empty:
                    # if there is no process map step specified, skip this row
                    continue
                else:
                    pmap = pmap.value.lower()
                    if pmap not in pb['steps']:
                        pb['steps'][pmap] = {'occurs': 1, 'cum_time': 0, 'min_time': None, 'min_step_number': '',
                                       'max_time': None, 'max_step_number': '', 'avg_time': 0, 'notes': ''}
                    else:
                        pb['steps'][pmap]['occurs'] += 1

                # get actual start and end times
                t_start = excel_time_to_datetime(actual_vals[ColNames.act_start])
                t_end = excel_time_to_datetime(actual_vals[ColNames.act_end])

                # handle when day rolls over to next day
                if t_end < t_start:
                    t_end += timedelta(days=1)

                # calculate time delta for step
                t_delta = (t_end - t_start).total_seconds() / 60.0

                # easier variables
                step = pb['steps'][pmap]
                task_number = actual_vals[ColNames.task].value

                # add cumulative time and notes
                step['cum_time'] += t_delta
                ct = actual_vals[ColNames.notes].ctype
                if ct != ExcelCellType.empty and ct != ExcelCellType.blank:
                    step['notes'] += ">" + actual_vals[ColNames.notes].value

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

                # calculate actual duration for step
                print("[{}] -- {} - {} -- [{}]".format(pmap, t_start.strftime("%I:%M %p"), t_end.strftime("%I:%M %p"), t_delta))
            except Exception, e:
                raise(Exception("Error on row {}: {}".format(i+1, e)))
        except Exception, e:
            raise(Exception("ERROR: {} has error: {}".format(file, e.message)))

    # output the final metrics
    print("---------------------------------------------------")
    print("CUSTOMER:    {0:<s}".format(pb['customer']))
    print("ENVIRONMENT: {0:<s}".format(pb['environment']))
    print("DATE:        {0:<s}".format(pb['date']))
    print("INSTALLER:   {0:<s}".format(pb['installer']))
    print("LEAD:        {0:<s}".format(pb['lead']))
    print("TIMINGS (IN MINUTES):")
    for key in sorted(pb['steps']):
        p = pb['steps'][key]
        print("  - {0:s} | CUM: {1:>4.0f} | AVG: {2:>4.0f} | MIN: {2:>4.0f} | MAX: {3:>4.0f}".format(key, p['cum_time'], p['avg_time'], p['min_time'], p['max_time']))
    print("---------------------------------------------------")
