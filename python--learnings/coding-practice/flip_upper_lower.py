#!/usr/bin/env python
#
# Flip all uppercase to lowercase, lowercase to uppercase.
#

def swap_case(s):
    new_string = ""
    for l in s:
        new_string += (l.lower() if l.isupper() else l.upper())
    return new_string

if __name__ == '__main__':
    s = input()
    result = swap_case(s)
    print(result)
