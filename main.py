# coding: utf-8
import logging

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
