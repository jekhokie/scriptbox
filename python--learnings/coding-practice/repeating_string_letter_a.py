#!/usr/bin/env python
#
# Given a string repeated X times, count number of letter 'a's in string.
#
import math
import os
import random
import re
import sys

# Complete the repeatedString function below.
def repeatedString(s, n):
    occurs = n // len(s)
    remain_letters =  n % len(s)

    original_str_as = s.count('a')

    complete_as = original_str_as * occurs
    remaining_as = s[0:remain_letters].count('a')

    return complete_as + remaining_as

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    s = input()
    n = int(input())
    result = repeatedString(s, n)

    fptr.write(str(result) + '\n')
    fptr.close()
