#!/usr/bin/env python
#
# Given an input string, convert the third letter to uppercase
# and print the new string.
#

def convert_third_upper(my_str):
      if len(my_str) < 3:
          print(my_str)
          return

      letter = my_str[2]
      new_str = my_str[0:2] + letter.upper()
      if len(my_str) >= 3:
          new_str += my_str[3:]

      print(new_str)

if __name__ == '__main__':
    convert_third_upper('hello')
    convert_third_upper('he')
    convert_third_upper('hel')
