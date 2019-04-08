# coding: utf-8
# 本文件封装模型数据的获取，供algorithm/data/compute_data.py调用
# 提供模型的对外接口
# 其他模块不会调用base_model文件夹内的任何东西
# 其他模块均通过本文件来获取模型的数据
# 获取数据都是基本数据，不涉及对象
# 一下给出的均为数据的格式，具体函数、对象或者全局变量均未定


# trucks和bases里的truck对应上
# 只给可用运力即可
def __get_trucks():
    trucks = {
        u'京A1111': {
            'base': u'北京',
            'type': 8,
            'delay_time': 10,
        },
    }
    return trucks


# trucks和bases里的truck对应上
# 只给可用运力即可
# orders只给未运订单
def __get_bases():
    bases = {
        u'北京': {
            'near_base': [],
            'near_dest': [],
            'other_truck': [],
            'local_truck': [],
            'orders': [],
        },
    }
    return bases


# orders只给未运订单
def __get_orders():
    orders = {
        '1': {
            'base': u'北京',
            'destination': u'天津',
            'delay_time': 10,
        }
    }
    return orders


def __get_destinations():
    destinations = {
        u'天津': {
            'near_dest': [],
        }
    }
    return destinations


def update_data():
    pass


def get_compute_data():
    trucks = __get_trucks()
    bases = __get_bases()
    orders = __get_orders()
    destinations = __get_destinations()
    return trucks, bases, orders, destinations
