#!/usr/bin/env python
#
# Given a budget and an array of prices, find max number of toys that can be purchased.
#

import math
import os
import random
import re
import sys

# Complete the maximumToys function below.
def maximumToys(prices, k):
    toys = []
    while k > 0:
        cheapest = min(prices)
        if k > cheapest:
            toys.append(cheapest)
            prices.remove(cheapest)
            k -= cheapest
        else:
            break

    return len(toys)

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    nk = input().split()
    n = int(nk[0])
    k = int(nk[1])
    prices = list(map(int, input().rstrip().split()))
    result = maximumToys(prices, k)

    fptr.write(str(result) + '\n')
    fptr.close()
