# coding: utf-8
import logging

from global_data import base_num, Bases, destination_num, Destinations, truck_num, Trucks
from model.base_model.base import Base
from model.base_model.destination import Destination
from model.base_model.truck import Truck
from utils.log import MyLogging
from algorithm.truck_scheduling import TruckScheduling


def init():
    pass


def compute():
    truck_scheduling = TruckScheduling()
    truck_scheduling.run()


def output():
    pass


if __name__ == "__main__":
    MyLogging()
    log = logging.getLogger('default')
