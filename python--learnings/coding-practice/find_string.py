#!/usr/bin/env python
#
# Find the total number of occurrences of a string within a string.
#

def count_substring(string, sub_string):
    substr = (1 for i in range(len(string)) if string.startswith(sub_string, i))
    return sum(substr)

if __name__ == '__main__':
    string = input().strip()
    sub_string = input().strip()

    count = count_substring(string, sub_string)
    print(count)
