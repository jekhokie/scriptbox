#!/usr/bin/env python
#
# Given a space-separated list of numbers and "n" indicating how many rotations,
# rotate and return the list of numbers by n positions.
#

import math
import os
import random
import re
import sys

# Complete the rotLeft function below.
def rotLeft(a, d):
    rotated = []

    if len(a) < d:
        d -= len(a)

    rotated.extend(a[d:])
    rotated.extend(a[:d])
    return rotated

if __name__ == '__main__':
    nd = input().split()

    n = int(nd[0])

    d = int(nd[1])

    a = list(map(int, input().rstrip().split()))

    result = rotLeft(a, d)
    print(result)
