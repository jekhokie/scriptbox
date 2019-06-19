#!/usr/bin/env python
#
# Given an input, convert to binary, flip all 0/1 to correlary, convert back to
# unsigned int, print.
#

import math
import os
import random
import re
import sys

# Complete the flippingBits function below.
def flippingBits(n):
    swapped = [1 if x is '0' else 0 for x in "{:032b}".format(n)]
    swapped_str = ''.join(str(x) for x in swapped)
    i = int(swapped_str, 2)
    return i

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    q = int(input())
    for q_itr in range(q):
        n = int(input())
    result = flippingBits(n)

    fptr.write(str(result) + '\n')
    fptr.close()
