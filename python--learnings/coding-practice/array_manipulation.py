#!/usr/bin/env python
#
# Given length of zero-array and number of iterations in form min,max,val,
# find the maximum resulting value in an array if you add "val" to each position
# between "min" and "max" for all arrays provided.
#

import math
import os
import random
import re
import sys

# Complete the arrayManipulation function below.
def arrayManipulation(n, queries):
    arr = [0] * n

    for i in queries:
        mn, mx, val = i
        print("MIN: %s | MAX: %s | VAL: %s" % (mn, mx, val))
        for i in range(mn, mx+1):
            arr[i-1] += val

    return max(arr)

if __name__ == '__main__':
    nm = input().split()
    n = int(nm[0])
    m = int(nm[1])

    queries = []
    for _ in range(m):
        queries.append(list(map(int, input().rstrip().split())))

    result = arrayManipulation(n, queries)
