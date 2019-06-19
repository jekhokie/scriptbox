#!/usr/bin/env python
#
# Count the number of deletions to ensure no repeat characters next
# to each other.
#

import math
import os
import random
import re
import sys

# Complete the alternatingCharacters function below.
def alternatingCharacters(s):
    deletions = 0

    for i, val in enumerate(s):
        if i < len(s)-1 and val == s[i+1]:
            deletions += 1

    return deletions

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    q = int(input())
    for q_itr in range(q):
        s = input()
        result = alternatingCharacters(s)
        fptr.write(str(result) + '\n')

    fptr.close()
