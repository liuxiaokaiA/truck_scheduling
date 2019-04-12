# coding: utf-8
import logging

from model.model_init import model_init
from utils.log import MyLogging
from algorithm.truck_scheduling import TruckScheduling
from log import MyLogging


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
    MyLogging()
    log = logging.getLogger('default')
    init()
    compute()
