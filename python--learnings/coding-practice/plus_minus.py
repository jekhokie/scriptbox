#!/usr/bin/env python
#
# Given an array, calculate the ratio of positive/negative/zero numbers.
#

import math
import os
import random
import re
import sys

# Complete the plusMinus function below.
def plusMinus(arr):
    arr_len = len(arr)
    pos = [x for x in arr if x > 0]
    neg = [x for x in arr if x < 0]
    zer = [x for x in arr if x == 0]

    print("{:06f}".format((len(pos) / arr_len)))
    print("{:06f}".format((len(neg) / arr_len)))
    print("{:06f}".format((len(zer) / arr_len)))

if __name__ == '__main__':
    n = int(input())
    arr = list(map(int, input().rstrip().split()))
    plusMinus(arr)
