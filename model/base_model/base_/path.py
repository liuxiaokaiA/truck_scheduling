# -*- encoding: utf-8 -*-
import sys
from itertools import permutations

from global_data import Orders, Destinations, Trucks, Bases
from model.base_model.base import Base
import logging

from model.base_model.base_.type import Truck_status
from model.base_model.destination import Destination

log = logging.getLogger("default")


def calculate_cost_by_path(truck_id, position_list, order_list):
    truck = Trucks[truck_id]
    cost = 0
    temp_order_list = []
    for index, position in enumerate(position_list):
        if index > 0:
            cost += position_list[index - 1].calculate_ditance(position) * truck.truck_cost(len(temp_order_list))
        if isinstance(position, Base):
            for order in order_list:
                if order.base == position.id:
                    if len(temp_order_list) < 8:
                        temp_order_list.append(order)
        else:
            for order in temp_order_list:
                if order.destination == position.d_id:
                    temp_order_list.remove(order)
    if temp_order_list:
        log.error("there some order not arrive destination")
        return sys.maxint
    if truck.status == Truck_status.TRUCK_IN_ORDER:
        future_base = position_list[-1].nearest_base
        cost += position_list[-1].calculate_ditance(Bases[future_base]) * truck.truck_cost(0)
    elif truck.status == Truck_status.TRUCK_IN_ORDER_DESTINATION:
        future_base = position_list[-1].nearest_base
        cost_return_base = cost + position_list[-1].calculate_ditance(Bases[truck.base]) * truck.truck_cost(0)
        cost_go_near = cost + position_list[-1].calculate_ditance(future_base) * truck.truck_cost(0)
        if cost_return_base < 1.3 * cost_go_near:
            cost = cost_return_base
            future_base = truck.base
        else:
            cost = cost_go_near
    else:
        future_base = None
        cost = sys.maxint
    return future_base, cost


class Path(object):
    def __init__(self):
        super(Path, self).__init__()
        self.bases = []
        self.destinations = []
        self.now = 0
        self.future_base = None

        self.speed = 100
        self.capacity = 8

        # 以下三个必须对应起来
        # 保留该路线所有信息，经过的也保留起来
        self.path = []
        self.orders = []
        self.times = []

    def get_best_path(self, truck_id, order_ids):
        truck = Trucks[truck_id]
        self.orders = []
        base_list = []
        destination_list = []
        position_list = []
        for order_id in order_ids:
            self.orders.append(Orders[order_id])
        for order in self.orders:
            base_list.append(Bases[order.base])
            destination_list.append(Destinations[order.destination])
        if Bases[truck.current_base] not in base_list:
            position_list.append(Bases[truck.current_base])
        position_list = position_list + base_list + destination_list
        self.path = position_list
        self.future_base = position_list[-1].nearest_base
        all_list = []
        if len(position_list) < 11:
            for temp_list in permutations(position_list[1:]):
                if isinstance(temp_list[-1], Destination):
                    all_list.append(position_list[0:1] + list(temp_list))
        min_cost = self.calculate_cost_by_path(truck_id, position_list)
        min_path = position_list
        for current_list in all_list:
            future_base, current_cost = self.calculate_cost_by_path(truck_id, current_list)
            if current_cost < min_cost:
                min_cost = current_cost
                min_path = current_list
                self.future_base = future_base
        self.path = min_path
        self.calculate_truck_time()

    def calculate_truck_time(self):
        self.times = []
        print self.future_base, self.path
        for index, position in enumerate(self.path):
            if index == 0:
                self.times.append(self.now)
            else:
                self.times.append(self.times[-1] + position.calculate_distance(self.path[index - 1]) / self.speed)
        self.times.append(self.path[-1].calculate_distance(Bases[self.future_base]))

    def calculate_cost_by_path(self, truck_id, position_list):
        """
        需要最后去哪
        :param truck_id:
        :param position_list:
        :return:
        """
        cost = 0
        temp_order_list = []
        for index, position in enumerate(position_list):
            if index > 0:
                cost += position_list[index - 1].calculate_distance(position) * Path.truck_cost(len(temp_order_list))
            if isinstance(position, Base):
                for order in self.orders:
                    if order.base == position.id:
                        if len(temp_order_list) < 8:
                            temp_order_list.append(order)
            else:
                for order in temp_order_list:
                    if order.destination == position.id:
                        temp_order_list.remove(order)

        future_base = position_list[-1].nearest_base
        if temp_order_list:
            log.error("there some order not arrive destination")
            return future_base, sys.maxint
        cost += position_list[-1].calculate_distance(Bases[future_base]) * Path.truck_cost(car_number=0)
        return future_base, cost

    @staticmethod
    def truck_cost(car_number):
        return 1.0 * (1 + car_number * 0.05)

    @staticmethod
    def get_cost_truck_in_order_dest(truck_id, order_ids):
        path = []
        order_list = []
        for order_id in order_ids:
            order_list.append(Orders[order_id])

        if truck_id is not None:
            truck = Trucks[truck_id]
            if order_list[0].base != truck.current_base:
                path.append(Bases[truck.current_base])
        temp_base = []
        temp_dest = []
        for order in order_list:
            temp_base.append(Bases[order.base])
            temp_dest.append(Destinations[order.destination])
        path += temp_base
        path += temp_dest
        temp_order_list = []
        if len(path) > 1 and isinstance(path[-1], Base):
            return sys.maxint
        cost = 0
        for index, position in enumerate(path):
            if index > 0:
                cost += path[index - 1].calculate_distance(position) * Path.truck_cost(len(temp_order_list))

            if isinstance(position, Base):
                for order in order_list:
                    if order.base == position.id:
                        if len(temp_order_list) < 8:
                            temp_order_list.append(order)
            else:
                for order in temp_order_list:
                    if order.destination == position.id:
                        temp_order_list.remove(order)
        return cost

    @staticmethod
    def get_cost_truck_in_order_dest_simple(truck_id, order_ids):
        path = []
        order_list = []
        for order_id in order_ids:
            order_list.append(Orders[order_id])

        if truck_id is not None:
            truck = Trucks[truck_id]
            if order_list[0].base != truck.current_base:
                path.append(Bases[truck.current_base])
        temp_base = []
        temp_dest = []
        for order in order_list:
            temp_base.append(Bases[order.base])
            temp_dest.append(Destinations[order.destination])
        path += temp_base
        path += temp_dest
        temp_order_list = []
        if len(path) > 1 and isinstance(path[-1], Base):
            return sys.maxint
        cost = 0
        for index, position in enumerate(path):
            cost += path[index - 1].calculate_distance(position) * Path.truck_cost(len(temp_order_list))
        return cost
