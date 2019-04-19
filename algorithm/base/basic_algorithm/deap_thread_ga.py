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
import os

from collections import deque
from multiprocessing import Event, Pipe, Process

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from algorithm.base.data.data import compute_data


log = logging.getLogger('debug')
truck_data, order_data, key_order = {}, {}, {}
MAX = 1000000
creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
creator.create("Individual", numpy.ndarray, fitness=creator.FitnessMax)
pipe_main = None

toolbox = base.Toolbox()


def cxTwoPointCopy(ind1, ind2):
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


def migPipe(deme, k, pipein, pipeout, selection, replacement=None):
    emigrants = selection(deme, k)
    if replacement is None:
        # If no replacement strategy is selected, replace those who migrate
        immigrants = emigrants
    else:
        # Else select those who will be replaced
        immigrants = replacement(deme, k)

    pipeout.send(emigrants)
    buf = pipein.recv()
    indx = 0
    for place, immigrant in zip(immigrants, buf):
        # indx = deme.index(place)
        deme[indx] = immigrant
        indx += 1


def get_best_gene(pops):
    bests = tools.selBest(pops, 2, fit_attr="fitness")
    return bests[0]


def set_data():
    # 获取调度用的trucks，以及其最大运载量
    global truck_data, order_data, key_order
    truck_max_order = compute_data.get_empty_truck_for_ga()

    # truck_order为truck可搭载order
    truck_order = compute_data.get_orders_truck_can_take(truck_max_order)

    # truck_data的key为truck空位，value为truck_id
    # order_data为未运订单可选择truck空位
    truck_data, order_data = compute_data.get_orders_list(truck_max_order, truck_order)
    # log.info('ga data: %s' % str(order_data))
    log.info('gene length: %d' % len(order_data))

    key_order = list(order_data)


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
    # print 'key_order: ' + str(key_order)
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
        # print 'truck: ', truck, 'is_must ', is_must, ' len(orders): ', len(orders)
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
            # print 'return 1'
            return MAX,
        value += get_truck_take_orders(truck, plan[truck])
        if value >= MAX:
            # print 'return 2'
            return value,
    value += get_order_cost(individual)
    # print 'return 3'
    # print value
    # import time
    # time.sleep(0.5)
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


def main(procid, pipein, pipeout, sync, seed=None):
    random.seed(seed)
    toolbox.register("migrate", migPipe, k=5, pipein=pipein, pipeout=pipeout,
                     selection=tools.selBest, replacement=random.sample)
    MU = 300
    NGEN = 40
    CXPB = 0.5
    MUTPB = 0.2
    MIG_RATE = 5
    pid = os.getpid()
    # print('woker: pid %s' % str(pid))
    # print pipein, pipeout

    deme = toolbox.population(n=MU)
    # hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    logbook = tools.Logbook()
    logbook.header = "gen", "deme", "evals", "std", "min", "avg", "max"

    for ind in deme:
        ind.fitness.values = toolbox.evaluate(ind)
    record = stats.compile(deme)
    logbook.record(gen=0, deme=procid, evals=len(deme), **record)

    if procid == 0:
        # Synchronization needed to log header on top and only once
        log.info(logbook.stream)
        sync.set()
    else:
        logbook.log_header = False  # Never output the header
        sync.wait()
        log.info(logbook.stream)

    for gen in range(1, NGEN):
        deme = toolbox.select(deme, len(deme))
        deme = algorithms.varAnd(deme, toolbox, cxpb=CXPB, mutpb=MUTPB)

        invalid_ind = [ind for ind in deme if not ind.fitness.valid]
        for ind in invalid_ind:
            ind.fitness.values = toolbox.evaluate(ind)

        # hof.update(deme)
        record = stats.compile(deme)
        logbook.record(gen=gen, deme=procid, evals=len(deme), **record)
        log.info(logbook.stream)

        if gen % MIG_RATE == 0 and gen > 0:
            toolbox.migrate(deme)
        # best_plan_t = get_best_gene(deme)
        # print best_plan_t.fitness.values[0]

    best_plan_t = get_best_gene(deme)
    # print best_plan_t.fitness.values[0]
    if procid == 0:
        pipe_main[1].send(best_plan_t)


def deap_scoop_ga():
    # creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
    # creator.create("Individual", numpy.ndarray, fitness=creator.FitnessMax)
    set_data()
    max_, gene_len, pop_count = get_parameter()
    toolbox.register("attr_bool", random.randint, 0, max_)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, gene_len)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate_gene)
    toolbox.register("mate", cxTwoPointCopy)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    toolbox.register("algorithm", algorithms.eaSimple, toolbox=toolbox, cxpb=0.5,
                     mutpb=0.05, ngen=5, verbose=False)

    random.seed(64)

    NBR_DEMES = 3

    pipes = [Pipe(False) for _ in range(NBR_DEMES)]
    pipes_in = deque(p[0] for p in pipes)
    pipes_out = deque(p[1] for p in pipes)
    # print pipes
    global pipe_main
    pipe_main = Pipe(False)
    pipes_in.rotate(1)
    pipes_out.rotate(-1)

    e = Event()
    # pid = os.getpid()
    # print('master: pid %s' % str(pid))

    processes = [Process(target=main, args=(i, ipipe, opipe, e, random.random()))
                 for i, (ipipe, opipe) in enumerate(zip(pipes_in, pipes_out))]

    for proc in processes:
        proc.start()

    for proc in processes:
        proc.join()

    best_gene = pipe_main[0].recv()
    best_plan = gene_to_plan(best_gene)
    log.info("best gene value is %d." % best_gene.fitness.values[0])
    return best_plan


if __name__ == "__main__":
    deap_scoop_ga()
