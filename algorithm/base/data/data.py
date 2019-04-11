# coding: utf-8
"""

本文件封装物流调度模型的数据
将 model 与 algorithm 分隔开, 本文件只存储 algorithm 需要的数据
算法只需使用获取之后的数据计算即可，不用关系模型的具体信息
模型修改不会影响到算法，只需修改数据获取函数即可
本文件只调用 model/get_model_data.py 的接口，不用关心模型的结构

"""
import copy

from model.get_model_data import get_compute_data, model_is_near, model_truck_take_orders_cost


class Base(object):
    bases = {}

    def get_base_near_base(self, base):
        near_base = copy.deepcopy(self.bases[base]['near_base'])
        if base not in near_base:
            near_base.append(base)
        return near_base

    def get_base_orders(self, base):
        return self.bases[base]['orders']

    def get_base_near_dest(self, base):
        return self.bases[base]['near_dest']

    # def get_other_truck(self, base):
    #     return self.bases[base]['other_truck']

    def get_local_truck(self, base):
        return self.bases[base]['local_truck']

    def get_other_truck(self, base):
        other_truck = self.bases[base]['other_truck']
        other_truck = sorted(list(other_truck), key=lambda truck: self.trucks[truck]['delay_time'], reverse=True)
        return other_truck

    def remove_orther_truck_in_base(self, base, truck):
        if truck in self.bases[base]['other_truck']:
            self.bases[base]['other_truck'].remove(truck)

    def remove_orders_in_base(self, base, del_order):
        for order in del_order:
            if order in self.bases[base]['orders']:
                self.bases[base]['orders'].remove(order)

    def get_base_truck(self, base, count):
        trucks = []
        local = self.get_local_truck(base)
        if local:
            trucks += local
        other = self.get_other_truck(base)
        if other:
            trucks += other
        if count < trucks:
            trucks = trucks[:count]
        return trucks


class Truck(object):
    trucks = {}

    def get_truck_base(self, truck):
        return self.trucks[truck]['base']

    def get_truck_type(self, truck):
        return self.trucks[truck]['type']

    def get_truck_near_base(self, truck):
        return self.trucks[truck]['near_base']


class Order(object):
    orders = {}

    def get_order_dest(self, order):
        return self.orders[order]['destination']

    def get_order_base(self, order):
        return self.orders[order]['base']

    def get_order_delay_time(self, order):
        return self.orders[order]['delay_time']

    def sort_order_by_delay(self, orders):
        return sorted(list(orders), key=lambda o: self.orders[o]['delay_time'], reverse=True)


class Destination(object):
    destinations = {}

    # 目的地附近目的地,包含本dest
    def get_dest_near_dest(self, dest):
        near_dest = copy.deepcopy(self.destinations[dest]['near_dest'])
        if dest not in near_dest:
            near_dest.add(dest)
        return near_dest


class Data(Base, Truck, Order, Destination):
    def __init__(self):
        super(Data, self).__init__()

    def set_data(self):
        trucks, bases, orders, destinations = get_compute_data()
        self.bases = bases
        self.trucks = trucks
        self.orders = orders
        self.destinations = destinations

    def get_truck_to_use(self, base):
        local_truck = self.get_local_truck(base)
        if local_truck:
            return local_truck[0]
        other_truck = self.get_other_truck(base)
        if other_truck:
            return other_truck[0]
        return None

    def truck_take_orders_cost(self, truck, orders):
        return model_truck_take_orders_cost(truck, orders)

    def is_near(self, truck_id, base, d):
        return model_is_near(truck_id, base, d)

    # 获取调度用的trucks，以及其最大运载量
    def get_empty_truck_for_ga(self):
        truck_max_order = {}
        for base in self.bases:
            order_num = len(self.get_base_orders(base))
            trucks = self.get_base_truck(base, (order_num/self.min_take)+2)
            for truck_id in trucks:
                truck_max_order[truck_id] = self.get_truck_type(truck_id)
        return truck_max_order

    # 返回truck可搭载order的数据
    def get_orders_truck_can_take(self, truck_max_order):
        truck_order = {}
        order_must_take = []
        # 获取所有大于10天的order
        for base in self.bases:
            orders = self.get_base_orders(base)
            for order in orders:
                if self.get_order_delay_time(order) >= self.order_mast_take['start']:
                    order_must_take.append(order)
        # truck附近的网点的订单
        for truck_id in truck_max_order:
            # print 'truck_id: %d' % truck_id
            bases = self.get_truck_near_base(truck_id)
            if truck_id not in truck_order:
                truck_order[truck_id] = []
            for base in bases:
                # print 'base: %d' % base_id
                orders = self.get_base_orders(base)
                for order in orders:
                    truck_order[truck_id].append(order)
            # 大于10天，1000公里内的运
            for order in order_must_take:
                base = self.get_order_base(order)
                if self.is_near(truck_id, base, self.max_distance):
                    truck_order[truck_id].append(order)
        return truck_order

    # 以truck空位为单位，进行排列
    # truck_data的key为truck空位，value为truck_id
    # order_data为未运订单可选择truck空位
    def get_orders_list(self, truck_max_order, data):
        truck_data = {}
        order_data = {}
        truck_count = 1
        for truck_id in data:
            for i in range(truck_max_order[truck_id]):
                truck_data[truck_count] = truck_id
                for order_id in data[truck_id]:
                    if order_id not in order_data:
                        order_data[order_id] = [0]
                    order_data[order_id].append(truck_count)
                truck_count += 1
        return truck_data, order_data
