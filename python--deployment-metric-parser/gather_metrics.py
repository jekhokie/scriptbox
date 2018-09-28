#!/usr/bin/env python
#
# Purpose: Parse Excel documents in the tests directory and produce
#          useful metrics for inspection.
#

import glob
import xlrd

# default vars for parsing metrics
steps = {}

# parse all playbooks in directory
for file in glob.glob("tests/*"):
    print(file)
    wb = xlrd.open_workbook(file)
    sheet = wb.sheet_by_index(0)

    # parse each step in the playbook
    for i in range(1, sheet.nrows):
        pmap = sheet.cell_value(i, 0)
        if pmap not in steps:
            steps[pmap] = {'occurs': 1, 'min_time': 0, 'max_time': 0, 'avg_time': 0}
        else:
            steps[pmap]['occurs'] += 1


# output the final metrics
for key in sorted(steps):
    print "%s %s" % (key, steps[key])
