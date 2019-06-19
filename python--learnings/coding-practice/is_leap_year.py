#!/usr/bin/env python
#
# Determine if a given year is a leap year.
#

def is_leap(year):
    leap = False

    if year % 4 == 0 and year >= 1900 and year <= (10 ** 5):
        if (year % 100) == 0 and (year % 400) == 0:
            leap = True
        elif (year % 100) != 0:
            leap = True

    return leap

year = int(input())
l = is_leap(year)
print(l)
