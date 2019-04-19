# coding: utf-8
"""

物流调度算法
1. 本文件主要是与物流调度业务相关程序编写
2. 对于其他场景的调度，只需要继承底层封装好的 DeapScoopGA ，并且实现 evaluate_gene 函数
   即可通过调用 run_ga 实现分布式遗传算法
3. 不同场景的调度可以实现不同的基础算法，类似 DeapScoopGA ，业务类只需要继承不同的基础算法类即可

"""
import logging

from algorithm.base.basic_algorithm.deap_thread_ga import deap_scoop_ga
from algorithm.base.data.data import compute_data
from algorithm.base.model_process import ModelProcess


log = logging.getLogger('debug')


# 物流调度预处理类
class TruckPreProcess(ModelProcess):
    def __init__(self):
        super(TruckPreProcess, self).__init__()

    # 获取本网点，以及附近网点的所有订单
    # 并将dest作为key，order为value
    def __get_near_base_dest_order(self, base):
        dest_order = {}
        # 附近的所有网点,包含本身,前面已经加入了
        near_bases = compute_data.get_base_near_base(base)
        for base_ in near_bases:
            for order in compute_data.get_base_orders(base_):
                order_dest = compute_data.get_order_dest(order)
                if order_dest not in dest_order:
                    dest_order[order_dest] = set()
                dest_order[order_dest].add(order)
        return dest_order

    def __remove_dest_order(self, dest_order, del_order):
        # 删除dest_order中的orders
        for order_ in del_order:
            order_dest = compute_data.get_order_dest(order_)
            if order_dest in dest_order:
                dest_order[order_dest].remove(order_)

    # 异地等待车顺路返回接单
    def __get_truck_return(self):
        for base in compute_data.bases:
            # 附近目的地，订单
            dest_order = self.__get_near_base_dest_order(base)
            # other_truck 已经按照其滞留时间排好序
            other_truck = compute_data.get_other_truck(base)
            # log.info('base: %d, other_truck: %s' % (base, str(other_truck)))
            # log.info('%s' % str(self.bases[base]['other_truck']))
            for truck in other_truck:
                near_order = set()
                truck_base = compute_data.get_truck_base(truck)
                # 目的地附近4S
                dest_nears = compute_data.get_base_near_dest(truck_base)
                # 再遍历附近目的地
                for dest in dest_order:
                    # 周围网点订单
                    if dest in dest_nears:
                        near_order |= dest_order[dest]
                # 所有顺路order
                truck_type = compute_data.get_truck_type(truck)
                # if truck_type <= len(near_order):
                #     log.info('base: %d, near_order: %s' % (base, str(near_order)))
                near_order = compute_data.sort_order_by_delay(near_order)
                del_order = []
                if truck_type <= len(near_order):
                    del_order = near_order[:truck_type]
                if del_order:
                    result = self.truck_take_orders(truck, del_order)
                    if not result:
                        continue
                # log.info('dest_order : %s' % str(dest_order))
                self.__remove_dest_order(dest_order, del_order)

    # 附近订单，目的地相近，能拼成整车的拼单
    def __get_order_nearby(self):
        for base in compute_data.bases:
            # 附近目的地，订单
            dest_order = self.__get_near_base_dest_order(base)
            near_bases = compute_data.get_base_near_base(base)
            for dest in dest_order:
                all_order = set()
                # 目的地附近目的地,包含本dest
                dest_list = compute_data.get_dest_near_dest(dest)
                # 再遍历附近目的地
                for dest_near_id in dest_order:
                    # 是周围网点，但不是本网点
                    if dest_near_id in dest_list:
                        for order in dest_order[dest_near_id]:
                            all_order.add(order)
                # 所有顺路order
                temp = compute_data.sort_order_by_delay(all_order)
                if not temp:
                    continue
                first_order_base = compute_data.get_order_base(temp[0])
                if first_order_base in near_bases:
                    near_bases.remove(first_order_base)
                    near_bases.append(first_order_base)
                for base_near in near_bases[::-1]:
                    # try:
                    temp = self.get_truck_from_base(base_near, temp)
                    # except Exception as e:
                    #     print e
                    if len(temp) < compute_data.min_take:
                        break
                del_order = [o for o in all_order if o not in temp]
                self.__remove_dest_order(dest_order, del_order)

    # 物流调度预处理，包括：
    # __get_truck_return 异地等待车顺路返回接单
    # __get_order_nearby 附近订单拼单
    def run_pre_process(self):
        # log.info('bases: ' + str(self.bases))
        # log.info('destinations: ' + str(self.destinations))
        # log.info('trucks: ' + str(self.trucks))
        log.info('start to get_truck_return')
        self.__get_truck_return()
        log.info('start to get_order_nearby')
        self.__get_order_nearby()
        # log.info(str(self.bases))


# 物流调度的算法类，继承自TruckPreProcess和DeapScoopGA
# 不同场景的调度算法可以仿照TruckScheduling进行实现
# 设置ga的参数，实现evaluate_gene函数
# 调用run即可
class TruckScheduling(TruckPreProcess):
    def __init__(self):
        super(TruckScheduling, self).__init__()
        self.best_plan = {}

    def get_data(self):
        compute_data.set_data()

    def process_plan(self):
        for truck in self.best_plan:
            self.truck_take_orders(truck, self.best_plan[truck])

    def run(self):
        log.info('start to get data')
        self.get_data()
        log.info('start to run pre process')
        self.run_pre_process()
        log.info("start to run ga")
        self.best_plan = deap_scoop_ga()
        log.info("ga end")
        self.process_plan()

if __name__ == '__main__':
    # TruckScheduling().run()
    truck_scheduling = TruckScheduling()
    truck_scheduling.run()
