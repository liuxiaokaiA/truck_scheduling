# -*- encoding: utf-8 -*-
import threading

from model.base_model.base_.type import BASE, DESTINATION


# 自定义的初始数据
# 之后可以替换该类，用真实数据
class Init_data(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        # self.base_position = pd.read_csv('generate/base_position0315.csv')
        # self.shop_position = pd.read_csv('generate/city_position0315.csv')
        # self.distance = pd.read_csv('generate/distance0315.csv')
        # self.trunk = pd.read_csv("generate/trunk.csv")
        # self.base_to_index = pd.read_csv("generate/base_to_index.csv")
        # self.city_to_index = pd.read_csv("generate/city_to_index.csv")
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(Init_data, "_instance"):
            with Init_data._instance_lock:
                if not hasattr(Init_data, "_instance"):
                    Init_data._instance = object.__new__(cls)
        return Init_data._instance

    def get_position(self, type, id):
        if type == BASE:
            return 1, 1
        elif type == DESTINATION:
            return 2, 2
        else:
            pass
