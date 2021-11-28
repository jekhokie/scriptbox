#!/usr/bin/env python3

import re

rules = []
with open('input.txt', 'r') as f:
  rules = f.read().splitlines()

def build_mappings(rules):
  mappings = []
  for rule in rules:
    bag_color = re.findall(r'(.*) bags contain.*', rule)[0]
    contain_string = re.findall(r'.* bags contain (.*).', rule)[0]

    container = []
    if contain_string != 'no other bags':
      for val in contain_string.split(', '):
        (num_bags, bag_name) = re.findall(r'([0-9]*) (.*) bag.*', val)[0]
        container.append({bag_name: num_bags})
        
    mappings.append({bag_color: container})

  return mappings

def get_containing_bag(mappings, bag_name):
  for mapping in mappings:
    for bag, contents in mapping.items():
      found_bags = [[k for k,v in d.items() if bag_name == k] for d in contents]
      found_bags = list(filter(lambda x: x, found_bags))
      if len(found_bags) > 0:
        if bag not in matches:
          matches.append(bag)
          get_containing_bag(mappings, bag)

def tally_bag_count(mappings, bag_contents, containing_number):
  global bag_count

  for found_bag in bag_contents:
    num_bags = int(list(found_bag.values())[0])
    bag_color = list(found_bag.keys())[0]

    bags_contained.append(bag_color)
    bag_count += num_bags + (num_bags * containing_number)
    print("{} | {} -> {}".format(num_bags, bag_color, bag_count))

    for mapping in mappings:
      for bag, bag_contents in mapping.items():
        if bag == bag_color:
          tally_bag_count(mappings, bag_contents, num_bags)

  return bag_count

#--- challenge 1

mappings = build_mappings(rules)
matches = []
for rule in rules:
  if re.match(r'.*[1-9]* shiny gold bag.*', rule):
    containing_bag = re.findall(r'(.*) bags contain.*', rule)[0]
    matches.append(containing_bag)
    get_containing_bag(mappings, containing_bag)

print("Solution to challenge 1: {}".format(len(matches)))

#--- challenge 2

print("Solution to challenge 2: {}".format("UNKNOWN"))
