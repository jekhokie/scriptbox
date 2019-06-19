#!/usr/bin/env python
#
# Given a Player name and score, design a comparator to print order as:
#   - First descending by score, then
#   - Ascending by name (where scores are equal)
#

from functools import cmp_to_key
class Player:
    def __init__(self, name, score):
        self.name = name
        self.score = score
                    
    def __repr__(self):
        return "%s %s" % (self.name, self.score)

    def comparator(a, b):
        print("A: %s, %s | B: %s, %s" % (a.name, a.score, b.name, b.score))
        print(a.score > b.score)
        if a.score > b.score:
            return -1
        elif a.score < b.score:
            return 1
        else:
            if a.name > b.name:
                return 1
            else:
                return -1

n = int(input())
data = []
for i in range(n):
    name, score = input().split()
    score = int(score)
    player = Player(name, score)
    data.append(player)
    
data = sorted(data, key=cmp_to_key(Player.comparator))
for i in data:
    print(i.name, i.score)
