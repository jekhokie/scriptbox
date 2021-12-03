#!/usr/bin/env python3

import re
from enum import Enum

diags = []
with open('input.txt', 'r') as f:
  diags = f.read().splitlines()

#--- challenge 1

gamma = ""
for i in range(0, len(diags[0])):
  zeros = len([x for x in diags if x[i] == "0"])
  ones = len([x for x in diags if x[i] == "1"])

  gamma += "0" if zeros > ones else "1"

gamma = int(gamma, 2)
epsilon = gamma ^ 0b111111111111

print("Solution to challenge 1: {}".format(gamma * epsilon))

#--- challenge 2

class Rating(Enum):
  OXYGEN = 0
  CO2 = 1

def get_val(diags, rating):
  for i in range(0, len(diags[0])):
    zeros = len([x for x in diags if x[i] == "0"])
    ones = len(diags) - zeros

    if rating == Rating.OXYGEN:
      check_val = "0" if zeros > ones else "1"
    else:
      check_val = "0" if zeros <= ones else "1"

    diags = [x for x in diags if x[i] != check_val]
    if len(diags) == 1:
      return int(diags[0], 2)

oxygen = get_val(diags, Rating.OXYGEN)
co2 = get_val(diags, Rating.CO2)

print("Solution to challenge 2: {}".format(oxygen * co2))
