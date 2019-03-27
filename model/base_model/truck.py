# coding: utf-8
from base_.path import Path
from base_.position import Truck_Position
from base_.type import Truck_status

from global_data import Trucks
from model.base_model.base_.truck_inquiry_api import TruckInquiryAPI


class Truck(Path, Truck_Position, TruckInquiryAPI):
    def __init__(self, id):
        super(Truck, self).__init__()
        # id为其车牌号
        self.id = id
        self.type = Truck_status.TRUNK_IN_ORDER
        # 其他基本信息

        # 保存板车历史运输信息
        # key为发车起始时间，value待定
        self.history = {}

        Trucks[id] = self

    def get_id(self):
        return self.id
