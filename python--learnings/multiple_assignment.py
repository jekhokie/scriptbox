#!/usr/bin/env python
#
# Topics:     Multiple Assignment/Tuple Unpacking/Iterable Unpacking
#
# Background: Assignment of multiple variables at the same time in a single line of code.
#
# Sources:
#   - https://treyhunner.com/2018/03/tuple-unpacking-improves-python-code-readability/

import unittest

# test functionality
class TestMethods(unittest.TestCase):
    def test_assignments(self):
        a, b = 5, 10

        self.assertEqual(a, 5)
        self.assertEqual(b, 10)

    def test_unpacking(self):
        people = {'name': 'Joe'}

        for k, v in people.items():
            self.assertEqual(k, 'name')
            self.assertEqual(v, 'Joe')

    def test_failed_assignment_count(self):
        with self.assertRaises(ValueError):
            (x, y) = 'a'

    def test_remaining_assignments(self):
        first, *rest = [1, 2, 3, 4]

        self.assertEqual(first, 1)
        self.assertEqual(rest, [2, 3, 4])

# main execution
if __name__ == '__main__':
    unittest.main()
