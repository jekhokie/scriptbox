#!/usr/bin/env python
#
# Determine if a number (or list of numbers) is/are prime.
#

import math
import os
import random
import re
import sys

# Complete the primality function below.
def primality(n):
    if n == 2:
        return 'Prime'
    elif n == 1 or n % 2 == 0:
        return 'Not prime'

    for x in range(2, math.ceil(math.sqrt(n)) + 1):
        if n % x == 0:
            return 'Not prime'

    return 'Prime'

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    p = int(input())

    for p_itr in range(p):
        n = int(input())
        result = primality(n)
        fptr.write(result + '\n')

    fptr.close()
