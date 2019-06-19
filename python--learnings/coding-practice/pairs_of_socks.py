#!/usr/bin/env python
#
# Given an array of integers, count how many pairs of socks exist.
#

import math
import os
import random
import re
import sys

# Complete the sockMerchant function below.
def sockMerchant(n, ar):
    keys = set(ar)
    vals = [ar.count(i) for i in keys]
    socks = dict(zip(keys, vals))
    pairs = [(i // 2) for i in socks.values()]
    return(sum(pairs))

if __name__ == '__main__':
    n = 10
    ar = [10, 20, 20, 10, 10, 30, 50, 10, 20]
    result = sockMerchant(n, ar)
    print(result)
'''
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input())
    ar = list(map(int, input().rstrip().split()))
    result = sockMerchant(n, ar)

    fptr.write(str(result) + '\n')
    fptr.close()
'''
