import enum
from collections import namedtuple

class Player(enum.Enum):#using an enum to represent players
    black = 1
    white = 2

    @property
    def other(self):
        return Player.black if self == Player.white else Player.white


class Point(namedtuple('Point', 'row col')):
    #named tupple allows us to access our points by point.row or point.col instead of point[0], point[1]
    #I really like this code - and didn't know about the named tuple funcs

    def neighbors(self):
        return[
            Point(self.row - 1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1),

        ]