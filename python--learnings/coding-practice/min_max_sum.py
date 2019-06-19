#!/usr/bin/env python
#
# Given an array of 5 integers, calculate min and max of sum of 4/5 integers.
#

import math
import os
import random
import re
import sys

# Complete the miniMaxSum function below.
def miniMaxSum(arr):
    arr.sort()
    print("{} {}".format(sum(arr[0:4]), sum(arr[1:])))

if __name__ == '__main__':
    arr = list(map(int, input().rstrip().split()))
    miniMaxSum(arr)

