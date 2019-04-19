# coding: utf-8
import logging

from model.model_init import model_init
from algorithm.truck_scheduling import TruckScheduling
from log import MyLogging
from model.output import write_excel

log = logging.getLogger("debug")


def init():
    log.info('model init start')
    model_init()
    log.info('model init end')


def compute():
    log.info("compute start")
    truck_scheduling = TruckScheduling()
    truck_scheduling.run()
    log.info("compute end")


def update():
    pass


def output():
    write_excel(0)


if __name__ == "__main__":
    MyLogging()
    log = logging.getLogger('default')
    init()
    compute()
    output()
