# -*- encoding: utf-8 -*-
import threading
import pandas as pd
import logging
from model.base_model.base_.type import BASE, DESTINATION

log = logging.getLogger('default')


# 自定义的初始数据
# 之后可以替换该类，用真实数据
class Init_data(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.base_position = pd.read_csv('model/base_model/base_/base_data/base_position.csv')
        self.destination_position = pd.read_csv('model/base_model/base_/base_data/city_position.csv')
        self.distance = pd.read_csv('model/base_model/base_/base_data/distance.csv')
        self.truck = pd.read_csv('model/base_model/base_/base_data/truck.csv')
        self.base_to_index = pd.read_csv('model/base_model/base_/base_data/base_to_index.csv')
        self.city_to_index = pd.read_csv('model/base_model/base_/base_data/city_to_index.csv')
        self.order = pd.read_csv()

    def __new__(cls, *args, **kwargs):
        if not hasattr(Init_data, "_instance"):
            with Init_data._instance_lock:
                if not hasattr(Init_data, "_instance"):
                    Init_data._instance = object.__new__(cls)
        return Init_data._instance
