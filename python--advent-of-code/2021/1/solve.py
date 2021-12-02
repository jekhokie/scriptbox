#!/usr/bin/env python3

import re

depths = []
with open('input.txt', 'r') as f:
  depths = f.read().splitlines()

increase_pos = []
decrease_pos = []
for i in range(1, len(depths)):
  if int(depths[i]) > int(depths[i-1]):
    increase_pos.append(i)

sliding_increase_pos = []
for i in range(1, (len(depths) - 3)):
  window1 = int(depths[i]) + int(depths[i+1]) + int(depths[i+2])
  window2 = int(depths[i+1]) + int(depths[i+2]) + int(depths[i+3])
  if window2 > window1:
    sliding_increase_pos.append(i)

#--- challenge 1

print("Solution to challenge 1: {}".format(len(increase_pos)))

#--- challenge 2

print("Solution to challenge 2: {}".format(len(sliding_increase_pos)))
