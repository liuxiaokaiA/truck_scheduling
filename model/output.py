# coding: utf-8
# 模块状态信息的输出
from global_data import Bases
import numpy as np

from model.base_model.base import Base
from model.base_model.order import Order
from model.base_model.base_.data_record import Writer


def write_base(writer, day):
    base_title = [u'网点ID', u'网点名称', u'地理位置（建模坐标）', u'未发车辆（本地）', u'未发车辆（外地）', u'今天发车（本地）',
                  u'今天发车（外地）', u'压板订单（1-5）', u'压板订单（5-10）',
                  u'压板订单（10-?）', u'网点可调度车', u'周边200公里网点', u'周边200公里可调用车数量']
    writer.write_title('base', base_title)
    l = []
    for id, base in Bases:
        name = base.name
        position = '(' + str(np.around(base.x, decimals=1)) + ',' + str(
            np.around(base.y, decimals=1)) + ')'
        trunk_num_1 = len(base.local_truck)
        trunk_num_2 = len(base.other_truck)
        trunk_num_3 = 0
        trunk_num_4 = 0
        delay_1 = 0
        delay_2 = 0
        delay_3 = 0
        for order in base.orders:
            if order.class_of_delay_time == 1:
                delay_1 += 1
            elif order.class_of_delay_time == 2:
                delay_2 += 1
            elif order.class_of_delay_time == 3:
                delay_3 += 1
        dispatch_trunk_num = trunk_num_1 + trunk_num_2
        around_base = str(base.near_base)
        trunk_id_list_1 = len(base)
        temp_list = [id, name, position, trunk_num_1, trunk_num_2, trunk_num_3, trunk_num_4, delay_1,
                     delay_2, delay_3, dispatch_trunk_num, around_base, trunk_id_list_1]
        l.append(temp_list)
    writer.write_data('base', l)


def write_truck(write, day):
    pass


def write_order(write, day):
    pass


def write_statistic(writer, day):
    pass


def write_excel(day):
    writer = Writer(day)
    write_base(writer, day)
    write_truck(writer, day)
    write_order(writer, day)
    write_statistic(writer, day)

    writer.save()
