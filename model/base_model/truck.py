# coding: utf-8
from base_.path import Path
from base_.position import Position
from base_.type import Truck_status

from global_data import Trucks
from model.base_model.base_.truck_inquiry_api import TruckInquiryAPI


class Truck(Path, Position, TruckInquiryAPI):
    def __init__(self, id):
        # 板车id
        self.id = id
        super(Truck, self).__init__()
        # 板车当前状态
        self.status = Truck_status.TRUCK_IN_ORDER
        # 板车容量
        self.capacity = 8
        # 板车历史信息
        self.history = {}
        # 板车顺数订单信息
        self.orders = []
        # 板车运输路线信息
        self.city_list = []
        # 板车预计到达时间
        self.time_list = []

    def update(self):
        pass

    def add_orders(self, order_list):
        self.orders = order_list
        self.status = Truck_status.TRUCK_ON_ROAD
        self.add_paths()

    def add_paths(self):
        if not self.orders:
            return

    def calculate_cost(self, orders):
        pass

    @staticmethod
    def truck_cost(car_number):
        return 1.0 * (1 + car_number * 0.05)
