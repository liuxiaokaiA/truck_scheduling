# coding: utf-8

BASE = 1
DESTINATION = 2


# 车辆状态
class Truck_status:
    # 初始状态
    TRUCK_IN_ORDER = 0
    # 行驶状态
    TRUCK_ON_ROAD = 1
    # 请假状态
    TRUCK_NOT_USE = 2
    # 不在自己本身网点的状态
    TRUCK_IN_ORDER_DESTINATION = 3
    # 正在赶往一个网点拉货，不可调度
    TRUCK_ON_ROAD_NOT_USE = 4

