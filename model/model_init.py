# coding: utf-8
import json

from global_data import Bases, Destinations, Trucks, Orders
from model.base_model.base import Base
from model.base_model.base_.data_inquiry import DataInquiry
from model.base_model.base_.init_data import Init_data
from model.base_model.destination import Destination
from model.base_model.order import Order
from model.base_model.truck import Truck


def init_order():
    data = json.load(open('model/base_model/base_/base_data/orders.txt', 'r'))
    for order_ in data:
        id_, base, destination, delay_time, class_of_delay_time = order_
        new_order = Order(id_, base, destination, delay_time)
        Orders[id_] = new_order
    return data


def model_init():
    init_data = Init_data()
    base_num = init_data.get_base_num()
    destination_num = init_data.get_destination_num()
    truck_num = init_data.get_truck_num()

    for index in range(base_num):
        temp_base = Base(index)
        Bases[index] = temp_base

    for index in range(destination_num):
        temp_destination = Destination(index+base_num)
        Destinations[index+base_num] = temp_destination

    for index in range(truck_num):
        temp_truck = Truck(index)
        Trucks[index] = temp_truck

    init_order()
    for base in Bases.values():
        base.update_base_info(order_list=Orders, truck_list=Trucks)
    for truck in Trucks.values():
        truck.set_data(Bases)
