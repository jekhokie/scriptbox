#!/usr/bin/env python
#
# Given an input string and max width, wrap the string to max_width
# and print the result.
#

import textwrap

def wrap(string, max_width):
    return "\n".join(textwrap.wrap(string, max_width))

if __name__ == '__main__':
    string, max_width = input(), int(input())
    result = wrap(string, max_width)
    print(result)
