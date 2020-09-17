
# We will provide our class for pointmodel.
# Classes for other rules will be dynamically generated.
class Point(object):
    def __init__(self, parent, x, y):
        self.parent = parent
        self.x = x
        self.y = y

    def __str__(self):
        return "{},{}".format(self.x, self.y)

    def __add__(self, other):
        return Point(self.parent, self.x + other.x, self.y + other.y)