#!/usr/bin/env python
#
# Print integer and floating point division results.
#

if __name__ == '__main__':
    a = int(input())
    b = int(input())
    int_divide = a // b
    float_divide = float(a) / float(b)
    print(int_divide)
    print("%f" % float_divide)
