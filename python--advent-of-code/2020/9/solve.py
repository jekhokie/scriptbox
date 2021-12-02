#!/usr/bin/env python3

numbers = []
with open('input.txt', 'r') as f:
  numbers = f.read().splitlines()

tgt_num = 0
tgt_num_pos = 0

#--- challenge 1

for pos in range(25, len(numbers)):
  found = False
  tgt_num = int(numbers[pos])

  for i in range((pos-25), pos):
    for j in range((pos-24), pos):
      first = int(numbers[i])
      second = int(numbers[j])

      # easy skips to prevent loop iterations
      if i == j: continue
      if first > tgt_num or second > tgt_num: continue

      if (first + second) == tgt_num:
        found = True
        break

    if found == True: break

  if found == False:
    tgt_num_pos = pos
    break

print("Solution to challenge 1: {}".format(tgt_num))

#--- challenge 2

sum_vals = 0
lower = 0
upper = 0
vals = []
for i in range(0, (tgt_num_pos-1)):
  vals = [int(numbers[i])]

  for j in range((i+1), (tgt_num_pos-1)):
    vals.append(int(numbers[j]))

    if sum(vals) == tgt_num:
      lower = i
      upper = j
      found = True
      break

  if found == True: break

print("Solution to challenge 2: {}".format(min(vals) + max(vals)))
