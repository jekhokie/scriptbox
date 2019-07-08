#!/usr/bin/env python
#
# Create a class of type Animal having the following attributes:
#   - color
#   - weight
#
# Then create Animal sub-classes named:
#   - Alligator
#   - Zebra
#
# Create an instance of Alligator and Zebra, then print the Animal details.
#

class Animal():
    def __init__(self, color, weight):
        self.color = color
        self.weight = weight

    def __repr__(self):
        return "I'm an animal of type {} with color {} and weight {}".format(self.__class__.__name__, self.color, self.weight)

class Alligator(Animal):
    def __init__(self, color, weight, teeth):
        super(Alligator, self).__init__(color, weight)
        self.teeth = teeth

    def __repr__(self):
        ret_string = super().__repr__()
        ret_string += ", having {} teeth".format(self.teeth)
        return ret_string

class Zebra(Animal):
    def __init__(self, color, weight, stripes):
        super(Zebra, self).__init__(color, weight)
        self.stripes = stripes

    def __repr__(self):
        ret_string = super().__repr__()
        ret_string += ", having {} stripes".format(self.stripes)
        return ret_string

if __name__ == "__main__":
    alligator = Alligator("Blue", 175, 50)
    zebra = Zebra("White", 215, 15)

    print(alligator)
    print(zebra)
