# coding: utf-8
import logging

from global_data import base_num, Bases, destination_num, Destinations, truck_num, Trucks
from model.base_model.base import Base
from model.base_model.destination import Destination
from model.base_model.truck import Truck
from model.model_init import model_init
from utils.log import MyLogging
from algorithm.truck_scheduling import TruckScheduling


def init():
    print ('model init start')
    model_init()
    print ('model init end')


def compute():
    print("compute start")
    truck_scheduling = TruckScheduling()
    truck_scheduling.run()
    print("compute end")


def output():
    pass


if __name__ == "__main__":
    # MyLogging()
    # log = logging.getLogger('default')
    init()
    compute()
