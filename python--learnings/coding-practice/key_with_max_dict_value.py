#!/usr/bin/env python
#
# Find and print the dictionary key with the maximum same value.
#

def largest_value(my_dict):
    print(max(my_dict.items(), key=lambda x: x[1])[0])

if __name__ == '__main__':
    print("Should print: {}".format(1))
    largest_value({1: 5, 2: 3, 3: 2})

    print("Should print: {}".format(6))
    largest_value({2: 1, 3: 2, 6: 15, 9: 7})
