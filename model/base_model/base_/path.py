# -*- encoding: utf-8 -*-
from global_data import Orders, Destinations, Bases


class Path(object):
    def __init__(self):
        self.bases = []
        self.destinations = []
        self.now = 0
        self.future_base = None

        # 以下三个必须对应起来
        # 保留该路线所有信息，经过的也保留起来
        self.path = []
        self.orders = []
        self.times = []

    def get_the_best_path(self, truck, orders):
        if orders and orders[0].base != truck.current_base:
            self.bases.append(truck.current_base)
        for order in orders:
            self.bases.append(order.base)
            self.destinations.append(order.destination)
        self.path = self.bases + self.destinations
        if orders and Destinations[orders[-1].destination].calculate_distance(Bases[truck.base]) < 200:
            self.future_base = truck.base
            self.path.append(truck.base)
        elif orders:
            self.future_base = self.path[-1]





