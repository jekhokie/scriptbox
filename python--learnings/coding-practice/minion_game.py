#!/usr/bin/env python
#
# Given a string, enumerate all unique strings from this string.
#

def minion_game(string):
    vowels = ['A', 'E', 'I', 'O', 'U']
    stuart_word_list = []
    stuart_score = 0
    kevin_word_list = []
    kevin_score = 0

    for size in range(len(string)):
        for pos in range(len(string)):
            fragment = string[pos:(pos + size + 1)]

            if fragment[0] in vowels and fragment not in kevin_word_list:
                kevin_word_list.append(fragment)
            if fragment[0] not in vowels and fragment not in stuart_word_list:
                stuart_word_list.append(fragment)

    print("DONE WORD LIST")
    for word in stuart_word_list:
        for pos in range(len(string)):
            if string[pos:(pos + len(word))] == word:
                stuart_score += 1

    for word in kevin_word_list:
        for pos in range(len(string)):
            if string[pos:(pos + len(word))] == word:
                kevin_score += 1

    if stuart_score > kevin_score:
        print("Stuart %s" % stuart_score)
    elif stuart_score < kevin_score:
        print("Kevin %s" % kevin_score)
    else:
        print("Draw")

if __name__ == '__main__':
    s = input()
    minion_game(s)
