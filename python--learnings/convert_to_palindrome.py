#!/usr/bin/env python
#
# Convert a string of random characters into a palindrome, or
# return -1 if it is not possible.
#

def convert_to_palindrome(my_str):
    my_hash = {}
    if len(my_str) == 1:
        print(my_str)
    elif len(my_str) == 2:
        if my_str[0] == my_str[1]:
            print(my_str)
            return
        else:
            print("False")
    else:
        for i in range(0, len(my_str)):
            if my_str[i] in my_hash:
                my_hash[my_str[i]] += 1
            else:
                my_hash[my_str[i]] = 1

        ones = sum(x for x in my_hash.values() if x == 1)
        non_twos = sum(1 for x in my_hash.values() if (x % 2) != 0 and x != 1)

        palindrome = ""
        if ones > 1 or non_twos > 0:
            print("False")
        else:
            sorted_dict = sorted(my_hash.items(), key=lambda x: x[1], reverse=True)
            for (k,v) in sorted_dict:
                palindrome += k * int(v/2)
            print(palindrome + palindrome[::-1])

if __name__ == '__main__':
    print("\nShould be: {}".format("abccba"))
    convert_to_palindrome("aabbcc")

    print("\nShould be: {}".format("bdcacdb"))
    convert_to_palindrome("abdcbdc")

    print("\nShould be: {}".format("abddba"))
    convert_to_palindrome("abdbad")

    print("\nShould be: {}".format("bbbaddabbb"))
    convert_to_palindrome("abbbbbdbad")

    print("\nShould be: {}".format("False"))
    convert_to_palindrome("aaabcde")

    print("\nShould be: {}".format("False"))
    convert_to_palindrome("eeddabcc")

    print("\nShould be: {}".format("a"))
    convert_to_palindrome("a")

    print("\nShould be: {}".format("bb"))
    convert_to_palindrome("bb")

    print("\nShould be: {}".format("False"))
    convert_to_palindrome("bc")
