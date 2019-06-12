#!/usr/bin/env python
#
# Topics:     Classes, Inheritance, and Related
#
# Background: Use of classes, including inheritance, instance variables, etc.
#
# Sources:
#   - https://www.python-course.eu/object_oriented_programming.php
#   - https://realpython.com/python3-object-oriented-programming

import unittest

class Account:
    routing = "123"

    def __init__(self, first_name="NOTSET"):
        self.first_name = first_name
        pass

    def details(self):
        return "{}|{}".format(self.__class__.routing, self.first_name)

class CheckingAccount(Account):
    def details(self):
        return "Checking|{}|{}".format(self.__class__.routing, self.first_name)

# test functionality
class TestClass(unittest.TestCase):
    account = None

    @classmethod
    def setUpClass(cls):
        cls.account = Account(first_name="Joe")
        cls.checking_account = CheckingAccount(first_name="Joe")

    def test_class_constructor(self):
        self.assertIsInstance(self.account, Account)

    def test_class_attribute(self):
        self.assertEqual(self.account.routing, "123")

    def test_instance_method(self):
        self.assertEqual(self.account.details(), "123|Joe")

    def test_class_inheritance(self):
        self.assertIsInstance(self.checking_account, CheckingAccount)
        self.assertIsInstance(self.checking_account, Account)

    def test_class_override(self):
        self.assertEqual(self.checking_account.details(), "Checking|123|Joe")

    def test_class_public_var(self):
        self.assertEqual(self.account.first_name, "Joe")

# main execution
if __name__ == '__main__':
    unittest.main()
