# -*- encoding: utf-8 -*-
import sys
from itertools import permutations

from global_data import Orders, Destinations, Bases, Trucks
from model.base_model.base import Base
from model.base_model.truck import Truck
from model.base_model.base_.type import Truck_status
from model.base_model.destination import Destination
import logging

log = logging.getLogger("default")


class Path(object):
    def __init__(self):
        super(Path, self).__init__()
        self.bases = []
        self.destinations = []
        self.now = 0
        self.future_base = None

        # 以下三个必须对应起来
        # 保留该路线所有信息，经过的也保留起来
        self.path = []
        self.orders = []
        self.times = []

    @staticmethod
    def get_best_path(truck_id, order_ids):
        truck = Trucks[truck_id]
        order_list = []
        base_list = []
        destination_list = []
        position_list = []
        for order_id in order_ids:
            order_list.append(Orders[order_id])
        for order in order_list:
            base_list.append(Bases[order.base])
            destination_list.append(Destinations[order.destination])
        if base_list and Bases[truck.current_base] not in base_list:
            position_list.append(Bases[truck.current_base])
        position_list = position_list + base_list + destination_list
        all_list = []
        if len(position_list) < 11:
            for temp_list in permutations(position_list[1:]):
                all_list.append(position_list[0:1] + list(temp_list))
        min_cost = sys.maxint
        min_path = []
        for index, current_list in enumerate(all_list):
            if index > 10000:
                break
            current_cost = Path.calculate_cost_by_path(truck_id,current_list,order_list)
            if current_cost < min_cost:
                min_cost = current_cost
                min_path = current_list
        return min_path

    @staticmethod
    def calculate_cost_by_path(truck_id, position_list, order_list):
        truck = Trucks[truck_id]
        cost = 0
        temp_order_list = []
        for index, position in enumerate(position_list):
            if index > 0:
                cost += position_list[index-1].calculate_distance(position)*truck.truck_cost(len(temp_order_list))
            if isinstance(position, Base):
                for order in order_list:
                    if order.base == position.id:
                        if len(temp_order_list) < 8:
                            temp_order_list.append(order)
            else:
                for order in temp_order_list:
                    if order.destination == position.id:
                        temp_order_list.remove(order)
        if temp_order_list:
            log.error("there some order not arrive destination")
            return sys.maxint
        return cost

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
                cost += path[index - 1].calculate_distance(position) * Truck.truck_cost(
                    len(temp_order_list))
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
    def calculate_cost_by_id(truck_id, order_ids):
        truck = Trucks[truck_id]
        order_list = []
        base_list = []
        destination_list = []
        position_list = []
        for order_id in order_ids:
            order_list.append(Orders[order_id])
        for order in order_list:
            base_list.append(Bases[order.base])
            destination_list.append(Destinations[order.destination])
        if base_list and base_list[0].base != truck.current_base:
            position_list.append(Bases[truck.current_base])
        position_list = position_list + base_list + destination_list
        temp_order_list = []
        cost = 0
        for index, position in enumerate(position_list):
            if index > 0:
                cost += position_list[index-1].calculate_distance(position)*truck.truck_cost(len(temp_order_list))

            if isinstance(position, Base):
                for order in order_list:
                    if order.base == position.id:
                        if len(temp_order_list) < 8:
                            temp_order_list.append(order)
            else:
                for order in temp_order_list:
                    if order.destination == position.id:
                        temp_order_list.remove(order)
        if temp_order_list:
            log.error("there some order not arrive destination")
            return sys.maxint
        return cost








