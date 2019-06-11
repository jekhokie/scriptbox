#!/usr/bin/env python
#
# Topics:     Generators and Iterators
#
# Background: Generators are a way to create iterators where one does not exist for an existing data
#             type/structure. They are functions that include yield statements that result in returning
#             data to the requestor but not terminating the function (meaning they hold/maintain state
#             until the caller executes the `next()` function on the iterator itself).
#
# Sources:
#   - https://www.programiz.com/python-programming/generator

import unittest

# function to test
def my_generator():
    '''Generator function which enables iterator functionality'''
    local_var = 1
    yield local_var

    local_var = 2
    yield local_var

# test functionality
class TestMethods(unittest.TestCase):
    def test_sequence(self):
        my_iterator = my_generator()

        # test functionality, with automatic StopIteration
        self.assertEqual(my_iterator.__next__(), 1)
        self.assertEqual(my_iterator.__next__(), 2)
        self.assertRaises(StopIteration, my_iterator.__next__)

# main execution
if __name__ == '__main__':
    unittest.main()
