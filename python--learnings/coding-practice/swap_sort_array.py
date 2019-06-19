#!/usr/bin/env python
#
# Given an array of elements, determine how many pair-swaps (minimum) are needed
# to get array in sorted ascending order.
#

#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the minimumSwaps function below.
def minimumSwaps(arr):
    swaps = 0
    for i in range(len(arr) - 1):
        cur_val = i + 1
        # swap needed
        if arr[i] != cur_val:
            swaps += 1
            arr[arr.index(cur_val)] = arr[i]
            arr[i] = cur_val

    return swaps
        

if __name__ == '__main__':
    n = int(input())
    arr = list(map(int, input().rstrip().split()))

    res = minimumSwaps(arr)

    print(res)
