#!/usr/bin/env python
#
# Capitalize the first letter of each word if they start with a letter.
#

def solve(s):
    prev_space = False
    new_string = ""

    for pos, i in enumerate(s):
        if i == " ":
            new_string += i
            prev_space = True
            continue
        
        if i.isalpha():
            if prev_space == True or pos == 0:
                new_string += i.upper()
            else:
                new_string += i

            prev_space = False
        else:
            new_string += i
            prev_space = False

    return new_string

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    s = input()
    result = solve(s)

    fptr.write(result + '\n')
    fptr.close()
