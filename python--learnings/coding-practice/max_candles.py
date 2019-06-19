#!/usr/bin/env python
#
# Given an array of candle heights, calculate how many candles can be blown out
# if you can only blow out the tallest ones.
#

import math
import os
import random
import re
import sys

# Complete the birthdayCakeCandles function below.
def birthdayCakeCandles(ar):
    return ar.count(max(ar))

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    ar_count = int(input())
    ar = list(map(int, input().rstrip().split()))
    result = birthdayCakeCandles(ar)

    fptr.write(str(result) + '\n')
    fptr.close()
