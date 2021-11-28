#!/usr/bin/env python3

import re

instructions = []
with open('input.txt', 'r') as f:
  instructions = f.read().splitlines()

instruction_set = []
for instruction in instructions:
  (action, value) = re.findall(r'^([a-z]+) ([+-][0-9]*)$', instruction)[0]
  instruction_set.append({"action": action, "value": int(value), "hits": 0})

pos = 0
accum_val1 = 0
while True:
  instruction = instruction_set[pos]
  if instruction['hits'] == 0:
    instruction['hits'] += 1

    if instruction['action'] == 'jmp':
      pos += instruction['value']
    elif instruction['action'] == 'nop':
      pos += 1
    elif instruction['action'] == 'acc':
      accum_val1 += instruction['value']
      pos += 1
  else:
    break

def clear_hits():
  for instruction in instruction_set:
    instruction['hits'] = 0

def try_run_program():
  global accum_val2
  accum_val2 = 0
  pos = 0
  prog_length = len(instruction_set)

  while True:
    if pos == prog_length:
      return True
    else:
      instruction = instruction_set[pos]
      if instruction['hits'] == 0:
        instruction['hits'] += 1
    
        if instruction['action'] == 'jmp':
          pos += instruction['value']
        elif instruction['action'] == 'nop':
          pos += 1
        elif instruction['action'] == 'acc':
          accum_val2 += instruction['value']
          pos += 1
      else:
        break

#--- challenge 1

print("Solution to challenge 1: {}".format(accum_val1))

#--- challenge 2

switch_pos = 0
success = False
accum_val2 = 0
while success == False:
  for instruction in instruction_set:
    action = instruction['action']
    if action == 'nop' or action == 'jmp':
      if action == 'nop':
        instruction['action'] = 'jmp'
      else:
        instruction['action'] = 'nop'

      clear_hits()
      if try_run_program():
        success = True
        break
      else:
        instruction['action'] = action

print("Solution to challenge 2: {}".format(accum_val2))
