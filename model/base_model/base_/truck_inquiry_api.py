# -*- encoding: utf-8 -*-
from .data_inquiry import DataInquiry


# 封装truck查询方法
# 主要是对业务逻辑提供查询接口
# 继承自DataInquiry
# DataInquiry封装了基本的数据查询方法
class TruckInquiryAPI(DataInquiry):

    def __init__(self, id):
        self.id = id
        super(TruckInquiryAPI, self).__init__()
        self.base, self.current_base, self.license, self.day, self.fleet = self.get_truck_info(self.id)

    # 封装truck调用的查询函数
    def get_near_base_station(self, distance=200):

