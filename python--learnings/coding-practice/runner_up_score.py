#!/usr/bin/env python
#
# Given a list, print the runner-up score (highest-1).
#

if __name__ == '__main__':
    n = int(input())
    arr = map(int, input().split())

    sort_list = sorted(list(arr), reverse=True)
    runner_up = [s for s in sort_list if s != sort_list[0]][0]

    print(runner_up)
