# coding: utf-8
from base_.path import Path
from base_.position import Position
from base_.type import Truck_status

from global_data import Trucks
from model.base_model.base_.truck_inquiry_api import TruckInquiryAPI


class Truck(Path, Position, TruckInquiryAPI):
    def __init__(self, id):
        super(Truck, self).__init__()
        self.inquiry = TruckInquiryAPI()
        # 板车id
        self.id = id
        #

        # 板车归属base
        self.base = self.inquiry.get_truck_info()
        # 板车当前状态
        self.status = Truck_status.TRUCK_IN_ORDER
        # 板车容量
        self.capacity = 8
        # 板车当前所在网点
        self.current_base = None
        # 板车车队信息
        self.fleet = None
        # 板车历史信息
        self.history = {}
        # 板车顺数订单信息
        self.orders = []
        # 板车运输路线信息
        self.city_list = []

    def get_id(self):
        return self.id
