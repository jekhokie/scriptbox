#!/usr/bin/env python
#
# Print the decimal, octal, capitalized hexidecimal, and binary values of input.
#

def print_formatted(number):
    col_width = len("{0:b}".format(number))
    print(col_width)

    for i in range(1, number + 1):
        binval = "{:b}".format(i)
        octval = "{:o}".format(i)
        hexval = "{:X}".format(i)
        decval = "{:d}".format(i)
        print("{0:>{width}} {1:>{width}} {2:>{width}} {3:>{width}}".format(decval, octval, hexval, binval, width=col_width))

if __name__ == '__main__':
    n = int(input())
    print_formatted(n)
