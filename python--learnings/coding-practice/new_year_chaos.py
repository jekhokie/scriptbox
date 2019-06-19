#!/usr/bin/env python
#
# Given a list of people sort-ordered, determine how many "bribes" needed
# to occur for positions to get to their new position, with any one person
# bribing > 2 bribes being "Too Chaotic".
#

import math
import os
import random
import re
import sys

# Complete the minimumBribes function below.
def minimumBribes(q):
    bribes = 0
    chaotic = False

    for i in reversed(range(len(q))):
        if q[-1] == (i + 1):
            q.pop(-1)
        elif len(q) > 1 and q[-2] == (i + 1):
            q.pop(-2)
            bribes += 1
        elif len(q) > 2 and q[-3] == (i + 1):
            q.pop(-3)
            bribes += 2
        else:
            chaotic = True
            break

    if chaotic:
        print("Too haotic")
    else:
        print(bribes)

if __name__ == '__main__':
    q = [1, 3, 2, 5, 4]
    minimumBribes(q)

'''
    #t = int(input())

    for t_itr in range(t):
        n = int(input())
        n = 1

        q = list(map(int, input().rstrip().split()))

        minimumBribes(q)
'''
