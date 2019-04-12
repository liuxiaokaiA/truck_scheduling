#    coding: utf-8
"""
本文件是对 deap + Scoop 分布式遗传算法的封装
业务调度类只需要继承 DeapScoopGA， 实现 evaluate_gene 函数，修改参数，调用 run_ga 即可

如果业务需要其他调度算法，可以依照 DeapScoopGA 进行类似的封装，放到 basic_algorithm 目录下
业务类继承对应调度算法即可
"""
import random
import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from scoop import futures


# 通用的遗传算法封装
# 只需要设定参数值，实现evaluate_gene函数
# 调用run_ga函数即可得到最后的最优gene
class DeapScoopGA(object):
    MAX = 10000000

    def __init__(self, max_=10, gene_len=100, pop_count=500, mutate=0.05,
                 NGEN=40, FREQ=5, NISLES=5, mutpb=0.2, cxpb=0.5):
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
        self.toolbox.register("mutate", self.tools.mutFlipBit, indpb=self.mutate)
        self.toolbox.register("select", self.tools.selTournament, tournsize=3)

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
        self.toolbox.register("algorithm", algorithms.eaSimple, toolbox=self.toolbox, cxpb=self.cxpb,
                              mutpb=self.mutpb, ngen=self.FREQ, stats=stats, verbose=False)

    def evolution_loop(self):
        # 注册map，调用scoop多进程进行计算
        self.toolbox.register("map", futures.map)
        for i in range(0, self.NGEN, self.FREQ):
            results = self.toolbox.map(self.toolbox.algorithm, self.islands)
            self.islands = [pop for pop, logbook in results]
            tools.migRing(self.islands, 15, tools.selBest)

    def get_best_gene(self):
        bests = []
        for island in self.islands:
            bests += tools.selBest(island, 2, fit_attr="fitness")
        if bests:
            ind = tools.selBest(bests, 2, fit_attr="fitness")[0]
            if MAX < ind.fitness.values:
                return ind
            else:
                return None
        return None

    def run_ga(self):
        self.init_population()
        self.evolution_loop()
        return self.get_best_gene()


if __name__ == "__main__":
    max_ = 10
    gene_len = 100
    pop_count = 500
    base_ga = DeapScoopGA()
