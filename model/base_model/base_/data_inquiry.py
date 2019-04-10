# -*- encoding: utf-8 -*-
import threading

from model.base_model.base_.init_data import Init_data

# position_data是base/destination等初始数据，以及
from model.base_model.base_.type import DESTINATION, BASE
import logging

log = logging.getLogger('default')
init_data = Init_data()


# 封装基础的数据查询方法，提供基础的查询
# 查询数据为：init_data
class DataInquiry(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.init_data = Init_data()
        self.base_num = self.__calculate_base_num()
        self.destination_num = self.__calculate_destination_num()
        self.truck_num = self.__calculate_truck_num()

    def __new__(cls, *args, **kwargs):
        if not hasattr(DataInquiry, "_instance"):
            with DataInquiry._instance_lock:
                if not hasattr(DataInquiry, "_instance"):
                    DataInquiry._instance = object.__new__(cls)
        return DataInquiry._instance

    def get_position(self, type, id):
        """
        用于初始化网点和4S店的位置信息
        :param type: BASE, DESTINATION分别表示网点和4S店
        :param id: 网点或4S店id信息
        :return: x，y坐标信息
        """
        if type == BASE:
            return self.init_data.base_position['x'][id], self.init_data.base_position['y'][id]
        elif type == DESTINATION:
            return self.init_data.destination_position['x'][id], self.init_data.destination_position['y'][id]
        else:
            log.error("Init_data get_position : wrong type")
            return 0, 0

    def get_distance(self, base_id_1=None, base_id_2=None, destination_id_1=None, destination_id_2=None):
        """
        用于初始化网点和4S店的距离信息，查询网点和4S店信息时，只能输入base_id_1和destination_id_1
        :param base_id_1: 网点 1 的id
        :param base_id_2: 网点 2 的id
        :param destination_id_1: 4S店 1 的id
        :param destination_id_2: 4S店 2 的id
        :return: 返回距离
        """
        if base_id_1 and base_id_2 and base_id_1 < self.base_num and base_id_2 < self.base_num:
            return self.init_data.distance.values[base_id_1, base_id_2]
        elif destination_id_1 and destination_id_2 and destination_id_1 < self.destination_num and destination_id_2 < self.destination_num:
            return self.init_data.distance.values[destination_id_1 + 60, destination_id_2 + 60]
        elif base_id_1 and destination_id_1 and base_id_1 < self.base_num and destination_id_1 < self.destination_num:
            return self.init_data.distance.values[base_id_1, destination_id_1 + 60]
        else:
            log.error('Init_data, get_distance : Error id')
            return 0

    def get_truck_info(self, id):
        """
        :param id: 板车id
        :return: base 归属网点id
                 current_base 车辆处于等计划状态时候，为板车当前所在网点id
                license 车牌号
                day 板车异地等计划天数
                fleet 板车归属车队

        """
        base = self.get_base_to_id(self.init_data.truck.loc[id]['base'])
        current_base = self.get_base_to_id(self.init_data.truck.loc[id]['current'])
        license = self.init_data.truck.loc[id]['license']
        day = self.init_data.truck.loc[id]['day']
        fleet = self.init_data.truck.loc[id]['fleet']
        return base, current_base, license, day, fleet

    def get_base_to_id(self, base_name):
        """
        :param base_name: 网点中文字符串
        :return: 网点id
        """
        try:
            return (self.init_data.base_to_index[self.init_data.base_to_index['city'] == base_name]).index[0]
        except:
            log.warning("Init_data get_base_to_id : no id match base_name")
            return None

    def get_city_to_id(self, city_name):
        """
        :param city_name: 4S店中文字符串
        :return: 4S店的id
        """
        try:
            return (self.init_data.city_to_index[self.init_data.city_to_index['city'] == city_name]).index[0]
        except:
            return None

    def get_id_to_base(self, id):
        """
        :param id: 网点id
        :return: 网点中文字符串
        """
        return self.init_data.base_to_index.values[id][0]

    def get_id_to_city(self, id):
        """
        :param id:4s店id
        :return: 4s店中文字符串
        """
        return self.init_data.city_to_index.values[id][0]

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
        return len(self.init_data.base_to_index) - 1

    def __calculate_destination_num(self):
        """
        :return: 4s店数目
        """
        return len(self.init_data.city_to_index) - 1

    def __calculate_truck_num(self):
        """
        :return: 板车的数目
        """
        return len(self.init_data.truck) - 1

