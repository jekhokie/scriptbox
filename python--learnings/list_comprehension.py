#!/usr/bin/env python
#
# Topics:     List Comprehension
#
# Background: List comprehension examples and functionality.
#
# Sources:
#   - https://treyhunner.com/2015/12/python-list-comprehensions-now-in-color/

import unittest

# test functionality
class TestMethods(unittest.TestCase):
    def test_loop(self):
        my_items = ['a', 'b', 'a', 'c']
        adjusted_items = [x for x in my_items if x == 'a']

        self.assertEqual(adjusted_items, ['a', 'a'])

    def test_nested_loop(self):
        '''
        How to transpose nested loops:

        names = []
        for person in people:                   # (1)
            for (key, val) in person.items():   # (2)
                names.append(val)               # (3)

        Into:
        
        names = [(3)val (1)for person in people (2)for (key,val) in person.items()]
        '''

        people = [{'name': 'joe'}, {'name': 'sally'}]
        names = [val for person in people for (key,val) in person.items()]

        self.assertEqual(names, ['joe', 'sally'])

# main execution
if __name__ == '__main__':
    unittest.main()
