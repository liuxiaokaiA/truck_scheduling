# coding: utf-8
from global_data import Destinations
from model.base_model.base_.init_data import Init_data
from model.base_model.base_.type import DESTINATION
from model.base_model.base_.inquiry_api import InquiryAPI
from model.base_model.base_.position import Position


# Destination类，继承自Position，Inquiry
# Position保存位置信息变量
# Inquiry封装位置查询的方法
class Destination(Position, InquiryAPI):
    type = DESTINATION

    def __init__(self, id):
        super(Destination, self).__init__()
        self.id = id
        temp_x, temp_y = self.get_city_position()
        self.set_position(temp_x,temp_y)
        self.name = self.get_city_name()
        self.near_destination = self.get_near_destination()
        self.nearest_base = self.get_nearest_base()
