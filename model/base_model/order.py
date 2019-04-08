# coding: utf-8
from global_data import Orders, Bases, Destinations


# 订单类，成员变量都换成object
class Order(object):
    def __init__(self, id, base_id, dest_id):
        super(Order, self).__init__()
        # id 格式为：20190326_00001
        self.id = id

        # 其他变量
        self.base = Bases[base_id]
        self.destination = Destinations[dest_id]

        self.truck = None

        # 起始距离目的地小于50公里，置为True
        self.not_to_send = False

        Orders[id] = self

    def get_id(self):
        return self.id
