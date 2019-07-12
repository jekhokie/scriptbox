class Animal:
    def __init__(self):
        self.name = "Animal"

    def __repr__(self):
        return "I am an animal with name {}".format(self.name)
