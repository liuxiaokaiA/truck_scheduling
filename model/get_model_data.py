# coding: utf-8

from global_data import SUCCESS, FAILED
# 本文件封装模型数据的获取，供algorithm/data/compute_data.py调用
# 提供模型的对外接口
# 其他模块不会调用base_model文件夹内的任何东西
# 其他模块均通过本文件来获取模型的数据
# 获取数据都是基本数据，不涉及对象
# 一下给出的均为数据的格式，具体函数、对象或者全局变量均未定


# trucks和bases里的truck对应上
# 只给可用运力即可
from global_data import Bases, Destinations, Orders, Trucks
from model.base_model.base_.path import Path


def __get_trucks():
    trucks = {}
    for truck in Trucks.values():
        truck_info = {
            'base': truck.base,
            'current_base': truck.current_base,
            'type': truck.capacity,
            'delay_time': truck.day,
            'near_base': truck.near_base,
        }
        trucks[truck.id] = truck_info
    return trucks


# trucks和bases里的truck对应上
# 只给可用运力即可
# orders只给未运订单
def __get_bases():
    bases = {}
    for base in Bases.values():
        base_info = {
            'near_base': base.near_base,
            'near_dest': base.near_destination,
            'other_truck': base.other_truck,
            'local_truck': base.local_truck,
            'orders': [order.id for order in base.orders]
        }
        bases[base.id] = base_info
    return bases


# orders只给未运订单
def __get_orders():
    orders = {}
    for order in Orders.values():
        order_info = {
            'base': order.base,
            'destination': order.destination,
            'delay_time': order.delay_time
        }
        orders[order.id] = order_info
    return orders


def __get_destinations():
    destinations = {}
    for destination in Destinations.values():
        destination_info = {
            'near_dest': destination.near_destination
        }
        destinations[destination.id] = destination_info
    return destinations


def update_data():
    for base in Bases.values():
        base.update_base_info(Trucks, Orders)
    for truck in Trucks.values():
        truck.update()


def get_compute_data():
    trucks = __get_trucks()
    bases = __get_bases()
    orders = __get_orders()
    destinations = __get_destinations()
    return trucks, bases, orders, destinations


def model_is_near(truck_id, base, d):
    result = SUCCESS
    if Trucks[truck_id].calculate_distance(Bases[base]) > d:
        result = FAILED
    return result


def model_truck_take_orders_cost(truck, orders):
    cost = Path.get_cost_trunk_in_order_dest(truck, orders)
    return cost
