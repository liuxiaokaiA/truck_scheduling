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

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from scoop import futures


log = logging.getLogger('debug')


# 通用的遗传算法封装
# 只需要设定参数值，实现evaluate_gene函数
# 调用run_ga函数即可得到最后的最优gene
class DeapScoopGA(object):
    MAX = 10000000

    def __init__(self, max_=10, gene_len=100, pop_count=500, mutate=0.05,
                 NGEN=1, FREQ=1, NISLES=1, mutpb=0.2, cxpb=0.5):
        super(DeapScoopGA, self).__init__()
        # 每位变化最大值，包括
        self.max_ = max_
        # 基因长度
        self.gene_len = gene_len
        # 种群大小
        self.pop_count = pop_count
        self.mutate = mutate
        self.NISLES = NISLES
        self.NGEN = NGEN
        self.FREQ = FREQ
        self.mutpb = mutpb
        self.cxpb = cxpb

        self.pop = None
        self.islands = None

        self.toolbox = base.Toolbox()

    # 抽象函数，放到派生类中实现
    def evaluate_gene(self, individual):
        return sum(individual),
        # raise NotImplementedError

    def evaluate_gene_loop(self, individual):
        raise NotImplementedError

    def cxTwoPointCopy(self, ind1, ind2):
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
        else: # Swap the two cx points
            cxpoint1, cxpoint2 = cxpoint2, cxpoint1

        ind1[cxpoint1:cxpoint2], ind2[cxpoint1:cxpoint2] \
            = ind2[cxpoint1:cxpoint2].copy(), ind1[cxpoint1:cxpoint2].copy()

        return ind1, ind2

    def init_population(self):
        creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
        creator.create("Individual", numpy.ndarray, fitness=creator.FitnessMax)
        self.toolbox.register("attr_bool", random.randint, 0, self.max_)
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_bool, n=self.gene_len)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("evaluate", self.evaluate_gene)
        self.toolbox.register("mate", self.cxTwoPointCopy)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=self.mutate)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

        random.seed(64)
        self.islands = [self.toolbox.population(n=self.pop_count) for i in range(self.NISLES)]

        self.toolbox.unregister("attr_bool")
        self.toolbox.unregister("individual")
        self.toolbox.unregister("population")

        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)

    def migRing(self, populations, k, selection, replacement=None, migarray=None):
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

    def evolution_loop(self):
        # 注册map，调用scoop多进程进行计算
        # self.toolbox.unregister("evaluate")
        # self.toolbox.register("evaluate", self.evaluate_gene_loop)
        self.toolbox.register("map", futures.map)
        self.toolbox.register("algorithm", algorithms.eaSimple, toolbox=self.toolbox, cxpb=self.cxpb,
                              mutpb=self.mutpb, ngen=self.FREQ, verbose=False)
        for i in range(0, self.NGEN, self.FREQ):
            log.info('evolution loop times: %d' % i)
            results = self.toolbox.map(self.toolbox.algorithm, self.islands)
            self.islands = [pop for pop, logbook in results]
            self.migRing(self.islands, 15, tools.selBest)
            best = self.get_best_gene()
            if best is not None:
                log.info('best gene: %s' % str(best.fitness.values))
                # log.info('best gene: %s' % str(self.gene_to_plan(best)))

    def get_best_gene(self):
        bests = []
        for island in self.islands:
            bests += tools.selBest(island, 2, fit_attr="fitness")
        if bests:
            ind = tools.selBest(bests, 2, fit_attr="fitness")[0]
            if self.MAX < ind.fitness.values:
                return ind
            else:
                return None
        return None

    def run_ga(self):
        log.info('start to init population')
        self.init_population()
        log.info('start to evolution loop')
        self.evolution_loop()
        log.info('evolution loop end')
        return self.get_best_gene()


if __name__ == "__main__":
    max_ = 10
    gene_len = 100
    pop_count = 500
    base_ga = DeapScoopGA()
