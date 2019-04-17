# -*- encoding: utf-8 -*-
import threading

from model.base_model.base_.init_data import Init_data

# position_data是base/destination等初始数据，以及
from model.base_model.base_.type import DESTINATION, BASE
import logging

log = logging.getLogger('default')


# 封装基础的数据查询方法，提供基础的查询
# 查询数据为：init_data
class DataInquiry(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        super(DataInquiry, self).__init__()
        self.init_data = Init_data()
        self.base_num = self.init_data.get_base_num()
        self.destination_num = self.init_data.get_destination_num()
        self.truck_num = self.init_data.get_truck_num()

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
            id = id - self.base_num
            return self.init_data.destination_position['x'][id], self.init_data.destination_position['y'][id]
        else:
            log.error("DataInquiry get_position : wrong type")
            return 0, 0

    def get_distance(self, id_1=None, id_2=None):
        """
        用于初始化网点和4S店的距离信息，查询网点和4S店信息时，只能输入base_id_1和destination_id_1
        :return: 返回距离
        """
        if id_1 is not None and id_2 is not None:
            return self.init_data.distance.values[id_1, id_2]
        else:
            log.error('DataInquiry, get_distance : Error id')
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
            log.warning("DataInquiry get_base_to_id : no id match base_name")
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
        id -= self.base_num
        return self.init_data.city_to_index.values[id][0]


