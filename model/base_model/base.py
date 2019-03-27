# coding: utf-8
from global_data import Bases
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
        # 用中文名字做 id
        self.id = id
        # 其他变量

        Bases[id] = self

    def get_id(self):
        return self.id
