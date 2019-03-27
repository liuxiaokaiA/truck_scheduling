# coding: utf-8
from global_data import Destinations
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
        # 用中文名字做 id
        self.id = id
        # 其他变量

        Destinations[id] = self

    def get_id(self):
        return self.id
