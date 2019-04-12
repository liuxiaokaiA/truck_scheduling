# coding: utf-8
import logging

from algorithm.truck_scheduling import TruckScheduling
from log import MyLogging


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
