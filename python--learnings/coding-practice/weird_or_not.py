#!/usr/bin/env python
#
# If n is:
#   odd, print Weird
#   even and 2 <= n <= 5, print Not Weird
#   even and 6 <= n <= 20, print Weird
#   even and > 20, print Not Weird
#

N = int(input())

if N % 2 != 0:
    print("Weird")
else:
    if N >= 2 and N <= 5:
        print("Not Weird")
    elif N >= 6 and N <= 20:
        print("Weird")
    elif N > 20:
        print("Not Weird")
