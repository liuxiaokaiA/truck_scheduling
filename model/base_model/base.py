# coding: utf-8
from global_data import Bases
from model.base_model.base_.init_data import Init_data
from model.base_model.base_.type import BASE
from model.base_model.base_.inquiry_api import InquiryAPI
from model.base_model.base_.position import Position


# base类，继承自Position，Inquiry
# Position保存该base位置信息变量
# Inquiry封装位置查询的方法
class Base(Position, InquiryAPI):
    type = BASE

    def __init__(self, id):
        super(Base, self).__init__()
        self.id = id
        self.set_position(self.get_city_position())
        self.name = self.get_city_name()
        self.near_base = self.get_near_base()
        self.near_destination = self.get_near_destination()
        self.local_truck = []
        self.other_truck = []
        self.orders = []

    def update_base_info(self, truck_list, order_list):
        self.local_truck, self.other_truck = self.get_in_order_truck(truck_list)
        for order in order_list:
            if order.base == self.id:
                self.orders.append(order)

