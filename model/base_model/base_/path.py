# -*- encoding: utf-8 -*-
import sys
from itertools import permutations

from global_data import Orders, Destinations, Bases, Trucks
from model.base_model.base import Base
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
        self.path = self.sort_position_list(truck, self.path, orders)

    def sort_position_list(self, truck, position_list, orders):
        if len(position_list) == 1:
            return position_list
        base_list = []
        destination_list = []
        all_list = []
        if len(position_list) < 11:
            for temp_list in permutations(position_list[1:]):
                if isinstance(list(temp_list)[-1], Destination):
                    all_list.append(position_list[0:1] + list(temp_list))
        else:
            for index in range(len(position_list)):
                if isinstance(position_list[index], Destination):
                    base_list = position_list[0:index]
                    destination_list = position_list[index:]
                    break
            for temp1 in permutations(destination_list):
                if base_list:
                    for temp2 in permutations(base_list[1:]):
                        all_list.append(base_list[0:1] + list(temp2 + temp1))
                else:
                    all_list.append(list(temp1))
        nearest_list = position_list
        nearest_distance = sys.maxint

        if truck.status == Truck_status.TRUCK_IN_ORDER:
            for current_index, current_list in enumerate(all_list):
                if current_index > 10000:
                    break
                last_position_id = current_list[-1].nearest.base
                # last_distance = current_list[-1].calculate_distance(Bases[last_position_id])
                sum_distance = self.calculate_cost(truck, orders, current_list, last_position_id)
                if sum_distance < nearest_distance:
                    nearest_list = current_list
                    nearest_distance = sum_distance
        elif truck.status == Truck_status.TRUCK_IN_ORDER_DESTINATION:
            for current_index, current_list in enumerate(all_list):
                sum_distance = self.calculate_cost(truck, orders, current_list, truck.base)
                if current_index > 10000:
                    break
                if sum_distance < nearest_distance:
                    nearest_list = current_list
                    nearest_distance = sum_distance
                # current_list.remove(current_list[0])

        elif truck.status == Truck_status.TRUCK_ON_ROAD:
            pass
            # for current_list in all_list:
            #     last_position, last_distance = self.inquiry_info.inquiry_nearest_base_station(current_list[-1].d_id)
            #     sum_distance = last_distance
            #     sum_distance += self.trunk_position.get_position_distance(current_list[0].position)
            #     for index in range(len(current_list) - 1):
            #         sum_distance += self.inquiry_info.inquiry_distance(current_list[index], current_list[index + 1])
            #     if sum_distance < nearest_distance:
            #         nearest_list = current_list
            #         nearest_distance = sum_distance

        for index in range(len(nearest_list) - 1):
            if isinstance(nearest_list[index], Base) and isinstance(nearest_list[index + 1], Destination):
                base_name = truck.get_id_to_base(nearest_list[index].id)
                city_name = truck.get_id_to_city(nearest_list[index + 1].id)
                if base_name == city_name:
                    nearest_list[index], nearest_list[index + 1] = nearest_list[index + 1], nearest_list[index]
        return nearest_list

    def calculate_cost(self, truck, order_list, position_list, last_position_id, current_low_cost=sys.maxint):
        if not position_list:
            print "position_list is null"
            return
        temp_order_list = []
        if len(position_list) > 1 and isinstance(position_list[-1], Base):
            return sys.maxint
        cost = 0
        for index, position in enumerate(position_list):
            if index > 0:
                cost += position_list[index - 1].calculate_ditance(position) * truck.trunk_cost(
                    len(temp_order_list))
            if isinstance(position, Base):
                for order in order_list:
                    if order.base == position.id:
                        if len(temp_order_list) < 8:
                            temp_order_list.append(order)
            else:
                for order in temp_order_list:
                    if order.destination == position.d_id:
                        temp_order_list.remove(order)
        if len(temp_order_list) > 0:
            return sys.maxint
        cost += position_list[-1].calculate_distance(Bases[last_position_id]) * truck.trunk_cost(
            len(temp_order_list))
        return cost

    @staticmethod
    def new_get_best_python(truck_id, order_ids):
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
        if base_list and Bases[truck.base] not in base_list:
            position_list.append(Bases[truck.base])
        position_list = position_list + base_list + destination_list
        all_list = []
        if len(position_list) < 11:
            for temp_list in permutations(position_list[1:]):
                all_list.append(position_list[0:1] + list(temp_list))
        min_cost = sys.maxint
        min_path = []
        for current_list in all_list:
            current_cost = Path.calculate_cost_by_road(truck_id,current_list,order_list)
            if current_cost < min_cost:
                min_cost = current_cost
                min_path = current_list
        return min_path


    @staticmethod
    def calculate_cost_by_road(truck_id, position_list, order_list):
        truck = Trucks[truck_id]
        cost = 0
        temp_order_list = []
        for index, position in enumerate(position_list):
            if index > 0:
                cost += position_list[index-1].calculate_ditance(position)*truck.trunk_cost(len(temp_order_list))
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
        return cost





    @staticmethod
    def get_cost_trunk_in_order_dest(truck, orders):
        path = []
        if Orders[orders[0]].base != Trucks[truck].current_base:
            path.append(Bases[Trucks[truck].current_base])
        temp_base = []
        temp_dest = []
        for order in orders:
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
                cost += path[index - 1].calculate_ditance(position) * truck.trunk_cost(
                    len(temp_order_list))
            if isinstance(position, Base):
                for order in orders:
                    if order.base == position.id:
                        if len(temp_order_list) < 8:
                            temp_order_list.append(order)
            else:
                for order in temp_order_list:
                    if order.destination == position.d_id:
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
        if base_list and base_list[0].base != truck.base:
            position_list.append(Bases[truck.base])
        position_list = position_list + base_list + destination_list
        temp_order_list = []
        cost = 0
        for index, position in enumerate(position_list):
            if index > 0:
                cost += position_list[index-1].calculate_ditance(position)*truck.trunk_cost(len(temp_order_list))

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
        return cost








