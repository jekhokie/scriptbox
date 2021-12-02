#!/usr/bin/env python3

import re

actions = []
with open('input.txt', 'r') as f:
  actions = f.read().splitlines()

#--- challenge 1

position = 0
depth = 0
for action in actions:
  (direction, distance) = re.findall(r'(\w+) (\d+)', action)[0]
  distance = int(distance)

  if direction == 'forward':
    position += distance
  elif direction == 'down':
    depth += distance
  elif direction == 'up':
    depth -= distance

print("Solution to challenge 1: {}".format(position * depth))

#--- challenge 2

position = 0
depth = 0
aim = 0
for action in actions:
  (direction, distance) = re.findall(r'(\w+) (\d+)', action)[0]
  distance = int(distance)

  if direction == 'forward':
    position += distance
    depth += (aim * distance)
  elif direction == 'down':
    aim += distance
  elif direction == 'up':
    aim -= distance

print("Solution to challenge 2: {}".format(position * depth))
