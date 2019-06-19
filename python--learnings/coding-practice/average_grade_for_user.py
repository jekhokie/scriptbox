#!/usr/bin/env python
#
# Given a key/value list of users and associated grades, calculate average of
# requested user.
#

if __name__ == '__main__':
    n = int(input())
    student_marks = {}
    for _ in range(n):
        name, *line = input().split()
        scores = list(map(float, line))
        student_marks[name] = scores
    query_name = input()

    scores = student_marks[query_name]
    avg_score = float(sum(scores)) / float(len(scores))
    print("%.2f" % avg_score)

