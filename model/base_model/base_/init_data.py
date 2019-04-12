# -*- encoding: utf-8 -*-
import json
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
        self.order_info = json.load(open('model/base_model/base_/base_data/orders.txt', 'r'))
        self.base_num = self.__calculate_base_num()
        self.destination_num = self.__calculate_destination_num()
        self.truck_num = self.__calculate_truck_num()

    def __new__(cls, *args, **kwargs):
        if not hasattr(Init_data, "_instance"):
            with Init_data._instance_lock:
                if not hasattr(Init_data, "_instance"):
                    Init_data._instance = object.__new__(cls)
        return Init_data._instance

    def get_base_num(self):
        """
        :return: 网点数目
        """
        return self.base_num

    def get_destination_num(self):
        """
        :return: 4s店数目
        """
        return self.destination_num

    def get_truck_num(self):
        """
        :return: 板车的数目
        """
        return self.truck_num

    def __calculate_base_num(self):
        """
        :return: 网点数目
        """
        return len(self.base_to_index)

    def __calculate_destination_num(self):
        """
        :return: 4s店数目
        """
        return len(self.city_to_index)

    def __calculate_truck_num(self):
        """
        :return: 板车的数目
        """
        return len(self.truck)
