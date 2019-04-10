# coding: utf-8
import logging

from global_data import base_num, Bases, destination_num, Destinations, truck_num, Trucks
from model.base_model.base import Base
from model.base_model.destination import Destination
from model.base_model.truck import Truck
from utils.log import MyLogging


def init():
    for index in range(base_num):
        temp_base = Base(index)
        Bases.append(temp_base)

    for index in range(destination_num):
        temp_destination = Destination(index)
        Destinations.append(temp_destination)

    for index in range(truck_num):
        temp_trunk = Truck(index)
        Trucks.append(temp_trunk)


if __name__ == "__main__":
    MyLogging()
    log = logging.getLogger('debug')
