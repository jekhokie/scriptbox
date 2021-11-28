#!/usr/bin/env python3

from math import floor, ceil

lines = []
with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

def get_val(line, start_pos, end_pos, lhalf, uhalf, uhalf_char):
  for x in line[start_pos:end_pos:]:
    if x == uhalf_char:  # take lower half
      uhalf -= ceil((uhalf - lhalf) / 2)
    else: # take upper half
      lhalf += ceil((uhalf - lhalf) / 2)

  if lhalf != uhalf:
    return Exception("Something went wrong: {} != {}".format(lhalf, uhalf))

  return uhalf

#--- challenge 1

seat_ids = []
for boarding_pass in lines:
  row = get_val(boarding_pass, 0, 7, 0, 127, 'F')
  column = get_val(boarding_pass, 7, 10, 0, 7, 'L')
  seat_ids.append(row * 8 + column)

print("Solution to challenge 1: {}".format(max(seat_ids)))

#--- challenge 2

seat_ids.sort()
missing_seat = ""
for x in range(seat_ids[0], seat_ids[-1]):
  if x not in seat_ids:
    missing_seat = x

print("Solution to challenge 2: {}".format(missing_seat))
