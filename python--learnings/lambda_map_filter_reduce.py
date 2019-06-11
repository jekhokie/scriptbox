#!/usr/bin/env python
#
# Topics:     Lambdas, Maps, Filters, Reduce
#
# Background: Lambda examples and functionality, including maps, filters, and reduces.
#
# Sources:
#   - https://www.python-course.eu/lambda.php

import unittest
from functools import reduce

# test functionality
class TestMethods(unittest.TestCase):
    def test_lambda(self):
        '''Anonymous function creation'''

        l_function = lambda x: "name: {}".format(x)

        self.assertEqual(l_function('Joe'), 'name: Joe')

    def test_map(self):
        '''Injects all values in list into function provided'''

        names = ['Joe', 'Sally']
        adjusted_names = map(lambda x: "name: {}".format(x), names)

        self.assertEqual(list(adjusted_names), ['name: Joe', 'name: Sally'])

    def test_filter(self):
        '''Captures values in provided list based on function provided'''

        vals = ['a', 'b', 'a', 'c']
        filtered_vals = filter(lambda x: x == 'a', vals)

        self.assertEqual(list(filtered_vals), ['a', 'a'])

    def test_reduce(self):
        '''Continuously runs function over all values provided.'''

        vals = [1, 2, 3]
        sum_of_vals = reduce(lambda x, y: x + y, vals)

        self.assertEqual(sum_of_vals, 6)

# main execution
if __name__ == '__main__':
    unittest.main()
