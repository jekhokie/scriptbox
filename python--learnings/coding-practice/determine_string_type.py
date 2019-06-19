#!/usr/bin/env python
#
# Determine if a string has alphanumeric, digit, lowercase, uppercase characters.
#

if __name__ == '__main__':
    s = input()

    print("True") if any(x.isalnum() for x in s) else print("False")
    print("True") if any(x.isalpha() for x in s) else print("False")
    print("True") if any(x.isdigit() for x in s) else print("False")
    print("True") if any(x.islower() for x in s) else print("False")
    print("True") if any(x.isupper() for x in s) else print("False")
