#!/usr/bin/env python3

# lists are slow - use a dict of value/index
puzzle_input = [6, 4, 12, 1, 20, 0, 16]
puzzle_input = [0,3,6]
puzzle_dict = {}

def find_value_max_index(value, current_index):
  if value in puzzle_dict and puzzle_dict[value] != current_index:
    return puzzle_dict[value]
  else:
    return None

def write_to_dict(value, index):
  puzzle_dict[value]['prev'] = puzzle_dict[value]['last']
  puzzle_dict[value]['last'] = index

def get_nth_value(nth):
  z = 0
  last_val = puzzle_input[-1]
  for i in range(len(puzzle_input)-1, (nth - 1)):
    print("---")
    print("TURN {}({}) -> {} | {}".format((i+2), i, last_val, puzzle_dict))
    if last_val in puzzle_dict:
#      if puzzle_dict[last_val]['last'] is not None:
#        print("FOUND LAST VAL")
#        dist = (i - puzzle_dict[last_val]['last'])
#
#        puzzle_dict[last_val]['prev'] = puzzle_dict[last_val]['last']
#        puzzle_dict[last_val]['last'] = (i+1)
#        last_val = dist
      if puzzle_dict[last_val]['prev'] is not None:
        print("FOUND FIRST VAL")
        dist = (i - puzzle_dict[last_val]['prev'])

        puzzle_dict[last_val]['prev'] = puzzle_dict[last_val]['last']
        puzzle_dict[last_val]['last'] = (i+1)
        last_val = dist
      else:
        print("FOUND NONE")
        if 0 in puzzle_dict:
          puzzle_dict[0]['prev'] = puzzle_dict[0]['last']
          puzzle_dict[0]['last'] = (i+1)
        else:
          puzzle_dict[0] = {'prev': None, 'last': (i+1)}
        last_val = 0
    else:  # value not found
      puzzle_dict[last_val] = {'prev': None, 'last': 0}
      last_val = 0

    z += 1
    if z == 10:
      break

  return last_val

# conver to dict (faster)
for i, val in enumerate(puzzle_input):
  puzzle_dict[val] = {'prev': None, 'last': i}

#--- challenge 1

print("Solution to challenge 1: {}".format(get_nth_value(2020)))

#--- challenge 2

# this is somewhat slow, but it works and is faster than using a list
#print("Solution to challenge 2: {}".format(get_nth_value(30000000)))
