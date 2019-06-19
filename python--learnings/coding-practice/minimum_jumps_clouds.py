#!/usr/bin/env python
#
# Given a list of thunder/cirrus (1, 0) cloud array, determine minimum
# jumps to get across given you can only ever jump 1 or 2 spaces from
# previous cloud.
#

import math
import os
import random
import re
import sys

# Complete the jumpingOnClouds function below.
def jumpingOnClouds(c):
    pos = 0
    jumps = 0
    while pos < (len(c)-1):
        if (pos+2) < len(c) and c[pos+2] != 1:
            pos += 2
        else:
            pos += 1
        jumps += 1

    return jumps

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input())
    c = list(map(int, input().rstrip().split()))
    result = jumpingOnClouds(c)

    fptr.write(str(result) + '\n')
    fptr.close()
