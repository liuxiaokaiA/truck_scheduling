# coding: utf-8
"""
本文件为 algorithm 对 model 的修改
调用 model.modify_model 的方法实现对 model 的修改
修改内容即：调度结果给 model 带来的变化
"""
import logging

from model.modify_model import model_truck_take_orders


log = logging.getLogger('debug')


class ModelProcess(object):
    def __init__(self):
        super(ModelProcess, self).__init__()
        self.count = 0

    def truck_take_orders(self, truck, del_order):
        result = model_truck_take_orders(truck, del_order)
        if not result:
            log.error('truck_take_orders error! truck: %d, orders: %s' % (truck, str(del_order)))
            return result
        base = self.get_truck_current_base(truck)
        # 删除操作应与model操作一致
        # 删除base中的truck
        # 函数在compute_data文件中
        self.remove_truck_in_base(base, truck)
        # 删除base中的order,可能不是truck的base
        self.remove_orders_in_base(del_order)

        log.info('count : %d , truck: %s, del_order: %s.' % (self.count, str(truck), str(del_order)))
        self.count += 1
        return result

    def __get_truck_to_work(self, base, type, all_orders):
        truck = self.get_truck_to_use(base)
        if truck is None:
            return False
        if type < len(all_orders):
            orders = all_orders[:type]
            self.truck_take_orders(truck, orders)
        else:
            self.truck_take_orders(truck, all_orders)
        return True

    def get_truck_from_base(self, base, orders):
        while 1:
            if len(orders) >= self.min_take:
                if self.__get_truck_to_work(base, self.min_take, orders):
                    orders = orders[self.min_take:]
                    # self.update_single_process(base)
                else:
                    break
            else:
                break
        return orders
