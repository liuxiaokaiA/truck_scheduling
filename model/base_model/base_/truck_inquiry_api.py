# -*- encoding: utf-8 -*-
from .data_inquiry import DataInquiry


# 封装truck查询方法
# 主要是对业务逻辑提供查询接口
# 继承自DataInquiry
# DataInquiry封装了基本的数据查询方法
class TruckInquiryAPI(DataInquiry):
    id = None

    def __init__(self):
        super(TruckInquiryAPI, self).__init__()
        self.base, self.current_base, self.license, self.day, self.fleet = self.get_truck_info(self.id)