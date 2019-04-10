# -*- encoding: utf-8 -*-
from model.base_model.base_.type import BASE, DESTINATION, Truck_status
from .data_inquiry import DataInquiry
import logging

log = logging.info("default")


# 封装查询方法，比如查询附近的trucks等
# 主要是对业务逻辑提供查询接口
# 继承自DataInquiry
# DataInquiry封装了基本的数据查询方法
# 如果base/destination查询结果是一样的，那就只封装一个类
# 否则，封装成两个类
class InquiryAPI(DataInquiry):
    type = None
    id = None

    def __init__(self, type):
        super(InquiryAPI, self).__init__()
        self.type = type

    def get_city_position(self):
        return self.get_position(self.type, self.id)

    def get_city_name(self):
        if type == BASE:
            return self.get_id_to_base(self.id)
        elif type == DESTINATION:
            return self.get_id_to_city(self.id)
        else:
            return None

    def get_near_base(self, distance=200):
        base_list = []
        if self.type == BASE:
            for i in range(self.base_num):
                if self.get_distance(base_id_1=self.id, base_id_2=i) < distance and i != id:
                    base_list.append(i)
        elif self.type == DESTINATION:
            for i in range(self.base_num):
                if self.get_distance(base_id_1=i, destination_id_1=self.id) < distance:
                    base_list.append(i)
        else:
            log.error("DataInquiry get_near_base : wrong type")
        return base_list

    def get_near_destination(self, distance=200):
        destination_list = []
        if self.type == BASE:
            for i in range(self.destination_num):
                if self.get_distance(base_id_1=self.id, destination_id_1=i) < distance:
                    destination_list.append(i)
        elif self.type == DESTINATION:
            for i in range(self.destination_num):
                if self.get_distance(destination_id_1=self.id, destination_id_2=i) < distance and id != i:
                    destination_list.append(i)
        return destination_list

    def get_in_order_truck(self, truck_list):
        local_truck = []
        other_truck = []
        if type != BASE:
            return local_truck, other_truck
        for truck in truck_list:
            if truck.status == Truck_status.TRUCK_IN_ORDER and truck.base == self.id:
                local_truck.append(truck.id)
            elif truck.status == Truck_status.TRUCK_IN_ORDER_DESTINATION and truck.current_base == self.id:
                other_truck.append(truck.id)
        return local_truck, other_truck

    def get_near_truck(self, truck_list, distance=200):
        pass
