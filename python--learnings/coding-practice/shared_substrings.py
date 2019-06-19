#!/usr/bin/env python
#
# Given 2 strings, determine if they share any common substrings.
#

import math
import os
import random
import re
import sys

# Complete the twoStrings function below.
def twoStrings(s1, s2):
    set1 = set([x for x in s1])
    set2 = set([y for y in s2])
    if set1.intersection(set2):
        return "YES"
    else:
        return "NO"

if __name__ == '__main__':
    s1 = "hello"
    s2 = "world"
    result = twoStrings(s1, s2)
    print(result)
'''
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    q = int(input())
    for q_itr in range(q):
        s1 = input()
        s2 = input()
        result = twoStrings(s1, s2)

        fptr.write(result + '\n')

    fptr.close()
'''
