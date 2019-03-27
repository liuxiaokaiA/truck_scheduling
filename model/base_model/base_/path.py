# -*- encoding: utf-8 -*-


class Path(object):
    def __init__(self):
        self.bases = []
        self.destinations = []
        self.now = 0
        self.future_base = None

        # 以下三个必须对应起来
        # 保留该路线所有信息，经过的也保留起来
        self.path = []
        self.orders = []
        self.times = []

    def get_the_best_path(self):
        pass
