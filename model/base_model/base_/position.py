# coding: utf-8


# 网点，4S店，车辆都有该属性，抽象出来
from math import sqrt


class Position(object):
    x = None
    y = None

    def __init__(self):
        super(Position, self).__init__()

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def calculate_distance(self, position):
        return sqrt(pow(self.x - position.x, 2) + pow(self.y - position.y, 2))
