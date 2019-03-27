# coding: utf-8


# 网点，4S店，车辆都有该属性，抽象出来
class Position(object):
    x = None
    y = None

    def __init__(self):
        pass


# truck的position基类
class Truck_Position(Position):
    speed = 0
    current_base = None

    def __init__(self):
        super(Truck_Position, self).__init__()

    def get_position(self):
        return self.x, self.y

    def set_position(self):
        pass
