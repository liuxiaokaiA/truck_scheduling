# coding: utf-8
from global_data import Orders, Bases, Destinations


# 订单类，成员变量都换成object
class Order(object):
    def __init__(self, id, base, destination, delay_time):
        self.id = id
        self.base = base
        self.destination = destination
        self.delay_time = delay_time
        self.class_of_delay_time = 0
        self.truck = None
        self.not_to_send = False
        self.set_delay_time()

    def update(self):
        self.delay_time = self.delay_time + 1
        self.set_delay_time()

    def set_delay_time(self):
        if self.delay_time <= 5:
            self.class_of_delay_time = 1
        elif 5 < self.delay_time <= 10:
            self.class_of_delay_time = 2
        elif self.delay_time > 10:
            self.class_of_delay_time = 3
        else:
            print('delay_time error!!,order id: %s' % str(self.id))
