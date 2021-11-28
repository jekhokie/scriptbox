#!/usr/bin/env python3

#--- challenge 1

look_for = 2020
with open('input.txt', 'r') as f:
  inputs = [int(x) for x in f]

for x in inputs:
  if (2020 - x) in inputs:
    print("Solution to challenge 1: {}".format(x * (2020 - x)))
    break

#--- challenge 2

jump_out = 0
for i in range(len(inputs) - 1):
  for j in range(len(inputs) - 2):
    if (2020 - inputs[i] - inputs[j]) in inputs:
      print("Solution to challenge 2: {}".format(inputs[i] * inputs[j] * (2020 - inputs[i] - inputs[j])))
      jump_out = 1
      break

  if jump_out == 1:
    break
