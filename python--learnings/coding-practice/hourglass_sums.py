#!/usr/bin/env python
#
# Given a 6x6 array, find sum of all hourglass values where an hourglass is:
#    X X X
#      X
#    X X X
#

import math
import os
import random
import re
import sys

# Complete the hourglassSum function below.
def hourglassSum(arr):
    sum_vals = []
    for x in range(1, 5):
        for y in range(1, 5):
            vals = [arr[x-1][y-1], arr[x-1][y], arr[x-1][y+1], arr[x][y], arr[x+1][y-1], arr[x+1][y], arr[x+1][y+1]]
            sum_vals.append(sum(vals))
                
    return max(sum_vals)

if __name__ == '__main__':
    arr = []
    for _ in range(6):
        arr.append(list(map(int, input().rstrip().split())))

    result = hourglassSum(arr)
    print(result)
