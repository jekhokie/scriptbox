#!/usr/bin/env python
#
# Simple micro project to refresh on modules, imports, and class inheritance.
#

from cls.randomfunc import random_func
from cls.animal import Animal
from cls.zebra import Zebra

def run():
    # general module import
    random_func()

    # class import
    animal = Animal()
    print(animal)

    # sub-class import
    zebra = Zebra()
    print(zebra)

if __name__ == '__main__':
    run()
