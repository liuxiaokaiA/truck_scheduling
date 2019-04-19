#    coding: utf-8
"""
本文件是对 deap + Scoop 分布式遗传算法的封装
业务调度类只需要继承 DeapScoopGA， 实现 evaluate_gene 函数，修改参数，调用 run_ga 即可

如果业务需要其他调度算法，可以依照 DeapScoopGA 进行类似的封装，放到 basic_algorithm 目录下
业务类继承对应调度算法即可
"""
import random
import numpy
import logging
import copy
import time

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from scoop import futures

from algorithm.base.data.data import compute_data


log = logging.getLogger('debug')
truck_data, order_data, key_order, best_plan = {}, {}, {}, {}
MAX = 1000000
creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
creator.create("Individual", numpy.ndarray, fitness=creator.FitnessMax)


def cxTwoPointCopy(ind1, ind2):
    """Execute a two points crossover with copy on the input individuals. The
    copy is required because the slicing in numpy returns a view of the data,
    which leads to a self overwritting in the swap operation. It prevents
    ::

        # >>> import numpy
        # >>> a = numpy.array((1,2,3,4))
        # >>> b = numpy.array((5.6.7.8))
        # >>> a[1:3], b[1:3] = b[1:3], a[1:3]
        # >>> print(a)
        # [1 6 7 4]
        # >>> print(b)
        # [5 6 7 8]
    """
    size = len(ind1)
    cxpoint1 = random.randint(1, size)
    cxpoint2 = random.randint(1, size - 1)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else:  # Swap the two cx points
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    ind1[cxpoint1:cxpoint2], ind2[cxpoint1:cxpoint2] \
        = ind2[cxpoint1:cxpoint2].copy(), ind1[cxpoint1:cxpoint2].copy()

    return ind1, ind2


def migRing(populations, k, selection, replacement=None, migarray=None):
    nbr_demes = len(populations)
    if migarray is None:
        migarray = range(1, nbr_demes) + [0]

    immigrants = [[] for i in xrange(nbr_demes)]
    emigrants = [[] for i in xrange(nbr_demes)]

    for from_deme in xrange(nbr_demes):
        emigrants[from_deme].extend(selection(populations[from_deme], k))
        if replacement is None:
            # If no replacement strategy is selected, replace those who migrate
            immigrants[from_deme] = emigrants[from_deme]
        else:
            # Else select those who will be replaced
            immigrants[from_deme].extend(replacement(populations[from_deme], k))

    for from_deme, to_deme in enumerate(migarray):
        for i, immigrant in enumerate(immigrants[to_deme]):
            # indx = populations[to_deme].index(immigrant)
            populations[to_deme][i] = emigrants[from_deme][i]


def get_best_gene(islands):
    count = 0
    max_ind = (0, None)
    for island in islands:
        bests = tools.selBest(island, 2, fit_attr="fitness")
        print('islands: %d ' % count)
        count += 1
        for ind in bests:
            print(str(ind.fitness.values[0]))
            if ind.fitness.values[0] > max_ind[0]:
                max_ind = (ind.fitness.values[0], ind)
    return max_ind[1]


def set_data():
    # 获取调度用的trucks，以及其最大运载量
    global truck_data, order_data, key_order, best_plan
    truck_max_order = compute_data.get_empty_truck_for_ga()

    # truck_order为truck可搭载order
    truck_order = compute_data.get_orders_truck_can_take(truck_max_order)

    # truck_data的key为truck空位，value为truck_id
    # order_data为未运订单可选择truck空位
    truck_data, order_data = compute_data.get_orders_list(truck_max_order, truck_order)
    # log.info('ga data: %s' % str(order_data))
    log.info('gene length: %d' % len(order_data))

    key_order = list(order_data)
    best_plan = {}


def get_parameter():
    max_len = 0
    for order in key_order:
        if len(order_data[order]) > max_len:
            max_len = len(order_data[order])
    max_len *= 2
    max_ = max_len
    gene_len = len(order_data)
    # self.pop_count = self.gene_len * 3
    pop_count = gene_len
    return max_, gene_len, pop_count


def get_truck_count(truck_list, index_truck, truck_count_set):
    length = len(truck_list)
    for i in range(length):
        index = (index_truck + i) % length
        truck_count = truck_list[index]
        if truck_count not in truck_count_set:
            return truck_count
    return 0


# 基因转换为具体方案
def gene_to_plan(individual, is_loop=False):
    plan = {}
    data = copy.deepcopy(order_data)
    print 'key_order: ' + str(key_order)
    truck_count_set = set()
    for index in range(len(key_order)):
        gene_num = individual[index]
        order_ = key_order[index]
        truck_list = data[order_]
        index_truck = gene_num % len(truck_list)
        if not is_loop:
            truck_count = get_truck_count(truck_list, index_truck, truck_count_set)
        else:
            truck_count = truck_list[index_truck]
        # id为0，则无truck
        if not truck_count:
            continue
        truck_count_set.add(truck_count)
        truck = truck_data[truck_count]
        if truck not in plan:
            plan[truck] = []
        plan[truck].append(order_)
    return plan


def get_truck_take_orders(truck, orders):
    bases = {}
    is_must = 0
    for order_id in orders:
        if compute_data.get_order_delay_time(order_id) >= compute_data.order_mast_take['start']:
            is_must = 1
        order_base = compute_data.get_order_base(order_id)
        if order_base not in bases:
            bases[order_base] = []
        bases[order_base].append(order_id)
    if not is_must and len(orders) not in (0, compute_data.min_take):
        return MAX
    return compute_data.truck_take_orders_cost(truck, orders)


def get_order_cost(individual):
    sum_cost = 0
    for index in range(len(key_order)):
        gene_num = individual[index]
        order_ = key_order[index]
        truck_list = order_data[order_]
        truck = truck_list[gene_num % len(truck_list)]
        # id为0，则无truck
        if not truck:
            sum_cost += compute_data.truck_take_orders_cost(None, [order_])
            # sum_cost += truck_penalty_cost(0.1)+order.delay_time * 10
            if compute_data.get_order_delay_time(order_) >= compute_data.order_mast_take['start']:
                return MAX
    return sum_cost


# 实现基因评估函数
def evaluate_gene(individual):
    plan = gene_to_plan(individual)
    value = 0
    for truck in plan:
        if not plan[truck] or len(plan[truck]) == 0:
            continue
        if len(plan[truck]) > compute_data.get_truck_type(truck):
            print 'return 1'
            time.sleep(10)
            return MAX,
        value += get_truck_take_orders(truck, plan[truck])
        if value >= MAX:
            print 'return 2'
            time.sleep(10)
            return value,
    value += get_order_cost(individual)
    print(str(plan))
    print(str(value))
    time.sleep(10)
    return value,


# 实现基因评估函数
def evaluate_gene_loop(individual):
    plan = gene_to_plan(individual, is_loop=True)
    value = 0
    for truck in plan:
        if not plan[truck] or len(plan[truck]) == 0:
            continue
        if len(plan[truck]) > compute_data.get_truck_type(truck):
            return MAX,
        value += get_truck_take_orders(truck, plan[truck])
        if value >= MAX:
            return value,
    value += get_order_cost(individual)
    return value,


def deap_scoop_ga():
    # creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
    # creator.create("Individual", numpy.ndarray, fitness=creator.FitnessMax)
    set_data()
    max_, gene_len, pop_count = get_parameter()
    toolbox = base.Toolbox()
    toolbox.register("attr_bool", random.randint, 0, max_)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, gene_len)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate_gene)
    toolbox.register("mate", cxTwoPointCopy)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)
    random.seed(64)
    islands = [toolbox.population(n=pop_count) for i in range(5)]

    toolbox.unregister("attr_bool")
    toolbox.unregister("individual")
    toolbox.unregister("population")

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    toolbox.register("map", futures.map)
    toolbox.register("algorithm", algorithms.eaSimple, toolbox=toolbox, cxpb=0.5,
                     mutpb=0.05, ngen=5, verbose=False)
    for i in range(0, 40, 5):
        print('evolution loop times: %d' % i)
        results = toolbox.map(toolbox.algorithm, islands)
        islands = [pop for pop, logbook in results]
        migRing(islands, 15, tools.selBest)
        get_best_gene(islands)
    best = get_best_gene(islands)
    return gene_to_plan(best)


if __name__ == "__main__":
    deap_scoop_ga()
