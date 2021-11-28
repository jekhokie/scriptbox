#!/usr/bin/env python3

import re

#--- challenge 1

valid_passwords = 0
with open('input.txt', 'r') as f:
  for line in f:
    [lower, upper, letter, password] = re.findall(r'(\d+)-(\d+) ([a-z]): (.*)', line.strip('\n'))[0]
    lower = int(lower)
    upper = int(upper)

    occurrences = password.count(letter)
    if occurrences >= lower and occurrences <= upper:
      valid_passwords += 1

print("Solution to challenge 1: {}".format(valid_passwords))

#--- challenge 2

valid_passwords = 0
with open('input.txt', 'r') as f:
  for line in f:
    [pos1, pos2, letter, password] = re.findall(r'(\d+)-(\d+) ([a-z]): (.*)', line.strip('\n'))[0]
    pos1 = int(pos1) - 1
    pos2 = int(pos2) - 1

    if (password[pos1] == letter) ^ (password[pos2] == letter):
      valid_passwords += 1

print("Solution to challenge 2: {}".format(valid_passwords))
