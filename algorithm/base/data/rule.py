# coding: utf-8
"""
调度规则，将 model/rule.py 中的规则转换为算法需要的数据
"""
from model.rule import rules, levels


class Rule(object):
    def __init__(self):
        self.order_level = {
            rules['order_level']['level']: (rules['order_level']['start'],
                                            rules['order_level']['end'])
        }
        self.order_mast_take = {
            'level': rules['must_take_order_level'][0],
            'start': rules['must_take_order_level'][1],
        }
        self.min_take = rules['truck_take_order_min'],
        self.truck_max_delay = rules['truck_delay_max']
        self.max_distance = rules['max_distance']

        self.compute_order = levels
