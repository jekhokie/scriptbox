#!/usr/bin/env python3

lines = []
with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

#--- challenge 1

def get_trees(lines, right, down):
  trees = 0
  pos = 0
  
  line_len = len(lines[0])
  for line in lines[down::down]:
    if (pos + right) >= line_len:
      pos = right - (line_len - pos)
    else:
      pos += right

    if line[pos] == '#':
      trees += 1
  
  return trees

trees = get_trees(lines, 3, 1)
print("Solution to challenge 1: {}".format(trees))

#--- challenge 2

tree_list = []
sequences = [[1,1], [3,1], [5,1], [7,1], [1,2]]
for check in sequences:
  tree_list.append(get_trees(lines, check[0], check[1]))

product = 1
for trees in tree_list:
  product *= trees

print("Solution to challenge 2: {}".format(product))
