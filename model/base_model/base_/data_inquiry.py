# -*- encoding: utf-8 -*-
from model.base_model.base_.init_data import Init_data

# position_data是base/destination等初始数据，以及
init_data = Init_data()


# 封装基础的数据查询方法，提供基础的查询
# 查询数据为：init_data
class DataInquiry(object):
    def __init__(self):
        pass

    def set_position(self):
        x, y = init_data.get_position(self.type, self.id)
        self.x = x
        self.y = y
