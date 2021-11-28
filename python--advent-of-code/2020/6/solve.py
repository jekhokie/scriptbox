#!/usr/bin/env python3

groups = []
with open('input.txt', 'r') as f:
  groups = f.read().split('\n\n')

def get_group_answers(groups):
  group_yes = []
  for group_val in groups:
    group_yes.append(len(list(set(''.join(group_val.split('\n'))))))

  return group_yes

# this is waaaay ugly, but it works
def get_consistent_group_answers(groups):
  group_yes = []
  for group in groups:
    group_items = set(list(filter(None, group.split('\n'))))
    consensus = []
    for person_answers in group_items:
      if len(group_items) == 1:
        consensus.extend(list(person_answers))
      else:
        for val in person_answers:
          exists = True
          if val not in consensus:
            for check_group in group_items:
              if val not in check_group:
                exists = False
                break
  
            if exists == True:
              consensus.append(val)

    group_yes.append(len(consensus))

  return group_yes

#--- challenge 1

group_answers = get_group_answers(groups)
print("Solution to challenge 1: {}".format(sum(group_answers)))

#--- challenge 2

group_yes = get_consistent_group_answers(groups)
print("Solution to challenge 2: {}".format(sum(group_yes)))
