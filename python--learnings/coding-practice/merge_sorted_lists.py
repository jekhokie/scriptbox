#!/usr/bin/env python
#
# Given 2 sorted lists, merge them in sequential order using least
# number of iterations/compute power.
#

l1 = [1, 3, 6, 7, 15, 22]
l2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100]

len1 = len(l1)
len2 = len(l2)

i,j = 0, 0
merged = []

while i < len1 and j < len2:
    if l1[i] < l2[j]:
        if l1[i] not in merged:
            merged.append(l1[i])
        i += 1
    else:
        if l2[j] not in merged:
            merged.append(l2[j])
        j += 1

merged = merged + l1[i:] + l2[j:]
print(merged)
