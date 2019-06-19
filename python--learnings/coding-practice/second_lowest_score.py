#!/usr/bin/env python
#
# Given name/grade inputs, print (alphabetically) names of second to lowest score.
#

if __name__ == '__main__':
    students = []
    for _ in range(int(input())):
        name = input()
        score = float(input())
        students.append([name, score])

    students.sort(key=lambda x: x[1])
    second_lowest = [s[1] for s in students if s[1] != students[0][1]][0]
    second_list = sorted([s[0] for s in students if s[1] == second_lowest])

    for n in second_list:
        print(n)
