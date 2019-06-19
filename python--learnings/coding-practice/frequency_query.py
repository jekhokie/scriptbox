#!/usr/bin/env python
#
# Given key/value pairs, perform operations:
#  - 1X: Insert X into array
#  - 2Y: Delete one occurrence of Y from array
#  - 3Z: Print 1 if any integer occurs Z times, else print 0
#

import math
import os
import random
import re
import sys

# Complete the freqQuery function below.
def freqQuery(queries):
    results = {}
    returned_results = []
    for pair in queries:
        op = pair[0]
        v = pair[1]

        # insert
        if op == 1:
            if v in results.keys():
                results[v] += 1
            else:
                results[v] = 1
        # delete 1 occurrence
        elif op == 2:
            if v in results.keys() and results[v] > 0:
                results[v] -= 1
        # check if any integer present number of times
        elif op == 3:
            returned_results.append(1 if v in results.values() else 0)

    return returned_results

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    q = int(input().strip())
    queries = []
    for _ in range(q):
        queries.append(list(map(int, input().rstrip().split())))
    ans = freqQuery(queries)

    fptr.write('\n'.join(map(str, ans)))
    fptr.write('\n')
    fptr.close()
