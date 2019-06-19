#!/usr/bin/env python
#
# Print all numbers to N using no string methods.
#

if __name__ == '__main__':
    n = int(input())

    for i in range(1, n+1):
        print("{}".format(i), end="")
