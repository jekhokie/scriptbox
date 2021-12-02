#!/usr/bin/env python3

import re

movements = []
with open('input.txt', 'r') as f:
  movements = f.read().splitlines()

coords = {"ew": 0, "ns": 0}
facing = 90
for move in movements:
  (action, value) = re.findall(r'^([A-Z])([0-9]*)$', move)[0]
  value = int(value)

  if action == 'N':
    coords['ns'] += value
  elif action == 'S':
    coords['ns'] -= value
  elif action == 'E':
    coords['ew'] += value
  elif action == 'W':
    coords['ew'] -= value
  elif action == 'L':
    facing = (facing - value) % 360
  elif action == 'R':
    facing = (facing + value) % 360
  elif action == 'F':
    if facing == 0 or facing == 360:
      coords['ns'] += value
    elif facing == 90:
      coords['ew'] += value
    elif facing == 180:
      coords['ns'] -= value
    elif facing == 270:
      coords['ew'] -= value

manhattan_dist = abs(coords['ew']) + abs(coords['ns'])

#--- challenge 1

print("Solution to challenge 1: {}".format(manhattan_dist))
