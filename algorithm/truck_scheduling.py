# coding: utf-8
"""

物流调度算法
1. 本文件主要是与物流调度业务相关程序编写
2. 对于其他场景的调度，只需要继承底层封装好的 DeapScoopGA ，并且实现 evaluate_gene 函数
   即可通过调用 run_ga 实现分布式遗传算法
3. 不同场景的调度可以实现不同的基础算法，类似 DeapScoopGA ，业务类只需要继承不同的基础算法类即可

"""
from algorithm.base.basic_algorithm.deap_scoop_ga import DeapScoopGA
from algorithm.base.data.data import Data
from algorithm.base.data.rule import Rule
from algorithm.base.model_process import ModelProcess


# 物流调度预处理类
class TruckPreProcess(ModelProcess, Data, Rule):
    def __init__(self):
        super(TruckPreProcess, self).__init__()

    # 获取本网点，以及附近网点的所有订单
    # 并将dest作为key，order为value
    def __get_near_base_dest_order(self, base):
        dest_order = {}
        # 附近的所有网点,包含本身,前面已经加入了
        near_bases = self.get_base_near_base(base)
        for base_ in near_bases:
            for order in self.get_base_orders(base_):
                order_dest = self.get_order_dest(order)
                if order_dest not in dest_order:
                    dest_order[order_dest] = set()
                dest_order[order_dest].add(order)
        return dest_order

    def __remove_dest_order(self, dest_order, del_order):
        # 删除dest_order中的orders
        for order_ in del_order:
            order_dest = self.get_order_dest(order_)
            if order_dest in dest_order:
                dest_order[order_dest].remove(order_)

    # 异地等待车顺路返回接单
    def __get_truck_return(self):
        for base in self.bases:
            # 附近目的地，订单
            dest_order = self.__get_near_base_dest_order(base)
            # other_truck 已经按照其滞留时间排好序
            other_truck = self.get_other_truck(base)
            for truck in other_truck:
                near_order = set()
                truck_base = self.get_truck_base(truck)
                # 目的地附近4S
                dest_nears = self.get_base_near_dest(truck_base)
                # 再遍历附近目的地
                for dest in dest_order:
                    # 周围网点订单
                    if dest in dest_nears:
                        near_order |= dest_order[dest]
                # 所有顺路order
                near_order = self.sort_order_by_delay(near_order)
                del_order = []
                truck_type = self.get_truck_type(truck)
                if truck_type <= len(near_order):
                    del_order = near_order[:truck_type]
                if del_order:
                    truck.is_return = True
                    result = self.truck_take_orders(truck, del_order)
                    if not result:
                        continue
                self.__remove_dest_order(dest_order, del_order)

    # 附近订单，目的地相近，能拼成整车的拼单
    def __get_order_nearby(self):
        for base in self.bases:
            # 附近目的地，订单
            dest_order = self.__get_near_base_dest_order(base)
            near_bases = self.get_base_near_base(base)
            for dest in dest_order:
                all_order = set()
                # 目的地附近目的地,包含本dest
                dest_list = self.get_dest_near_dest(dest)
                # 再遍历附近目的地
                for dest_near_id in dest_order:
                    # 是周围网点，但不是本网点
                    if dest_near_id in dest_list:
                        for order in dest_order[dest_near_id]:
                            all_order.add(order)
                # 所有顺路order
                temp = self.sort_order_by_delay(all_order)
                if not temp:
                    continue
                first_order_base = self.get_order_base(temp[0])
                if first_order_base in near_bases:
                    near_bases.remove(first_order_base)
                    near_bases.append(first_order_base)
                for base_near in near_bases[::-1]:
                    try:
                        temp = self.get_truck_from_base(base_near, temp)
                    except Exception as e:
                        print e
                    if len(temp) < self.min_take:
                        break
                del_order = [o for o in all_order if o not in temp]
                self.__remove_dest_order(dest_order, del_order)

    # 物流调度预处理，包括：
    # __get_truck_return 异地等待车顺路返回接单
    # __get_order_nearby 附近订单拼单
    def run_pre_process(self):
        self.__get_truck_return()
        self.__get_order_nearby()


# 物流调度的算法类，继承自TruckPreProcess和DeapScoopGA
# 不同场景的调度算法可以仿照TruckScheduling进行实现
# 设置ga的参数，实现evaluate_gene函数
# 调用run即可
class TruckScheduling(TruckPreProcess, DeapScoopGA):
    def __init__(self):
        super(TruckScheduling, self).__init__()
        self.data = {}
        self.key_order = []
        self.best_plan = {}

    def __set_data(self):
        # 获取调度用的trucks，以及其最大运载量
        truck_max_order = self.get_empty_truck_for_ga()
        
        # truck_order为truck可搭载order
        truck_order = self.get_orders_truck_can_take(truck_max_order)
        
        # truck_data的key为truck空位，value为truck_id
        # order_data为未运订单可选择truck空位
        truck_data, order_data = self.get_orders_list(truck_max_order, truck_order)

        self.truck_data = truck_data
        self.data = order_data

        self.key_order = list(self.data)
        self.best_plan = {}

    def __set_parameter(self):
        max_len = 0
        for order in self.key_order:
            if len(self.data[order]) > max_len:
                max_len = len(self.data[order])
        max_len *= 2
        self.max_ = max_len
        self.gene_len = len(self.data)
        self.pop_count = self.gene_len * 3

    # 基因转换为具体方案
    def __gene_to_plan(self, individual):
        plan = {}
        for index in range(len(self.key_order)):
            gene_num = individual[index]
            order_ = self.key_order[index]
            truck_list = self.data[order_]
            truck_count = truck_list[gene_num % len(truck_list)]
            # id为0，则无truck
            if not truck_count:
                continue
            truck = self.truck_data[truck_count]
            if truck not in plan:
                plan[truck] = []
            plan[truck].append(order_)
        return plan

    def __get_truck_take_orders(self, truck, orders):
        bases = {}
        is_must = 0
        for order_id in orders:
            if self.get_order_delay_time(order_id) >= self.order_mast_take['start']:
                is_must = 1
            order_base = self.get_order_base(order_id)
            if order_base not in bases:
                bases[order_base] = []
            bases[order_base].append(order_id)
        if not is_must and len(orders) not in (0, self.min_take):
            return self.MAX
        return self.truck_take_orders_cost(truck, orders)

    def __get_order_cost(self, individual):
        sum_cost = 0
        for index in range(len(self.key_order)):
            gene_num = individual[index]
            order_ = self.key_order[index]
            truck_list = self.data[order_]
            truck = truck_list[gene_num % len(truck_list)]
            # id为0，则无truck
            if not truck:
                sum_cost += self.truck_take_orders_cost(None, [order_])
                # sum_cost += truck_penalty_cost(0.1)+order.delay_time * 10
                if self.get_order_delay_time(order_) >= self.order_mast_take['start']:
                    return self.max_
        return sum_cost

    def __process_plan(self):
        for truck in self.best_plan:
            self.truck_take_orders(truck, self.best_plan[truck])

    # 实现基因评估函数
    def evaluate_gene(self, individual):
        plan = self.__gene_to_plan(individual)
        value = 0
        for truck in plan:
            if not plan[truck] or len(plan[truck]) == 0:
                continue
            if len(plan[truck]) > self.get_truck_type(truck):
                return self.MAX
            value += self.__get_truck_take_orders(truck, plan[truck])
            if value >= self.MAX:
                return value
        value += self.__get_order_cost(individual)
        return value

    def run(self):
        self.run_pre_process()
        self.__set_data()
        self.__set_parameter()
        best_ind = self.run_ga()
        self.best_plan = self.__gene_to_plan(best_ind)
        self.__process_plan()


if __name__ == '__main__':
    # TruckScheduling().run()
    truck_scheduling = TruckScheduling()
    truck_scheduling.run()
