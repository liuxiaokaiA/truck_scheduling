# coding: utf-8
# 模块状态信息的输出
from global_data import Bases, Trucks, Orders, Destinations
import numpy as np

from model.base_model.base import Base
from model.base_model.base_.type import Truck_status
from model.base_model.order import Order
from model.base_model.truck import Truck
from model.base_model.base_.data_record import Writer, model_time_to_date_time
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def write_base(writer, day):
    base_title = [u'网点ID', u'网点名称', u'地理位置（建模坐标）', u'未发车辆（本地）', u'未发车辆（外地）', u'今天发车（本地）',
                  u'今天发车（外地）', u'压板订单（1-5）', u'压板订单（5-10）',
                  u'压板订单（10-?）', u'网点可调度车', u'周边200公里网点']
    writer.write_title('base', base_title)
    l = []
    for id, base in Bases.items():
        name = base.name
        position = '(' + str(np.around(base.x, decimals=1)) + ',' + str(
            np.around(base.y, decimals=1)) + ')'
        truck_num_1 = len(base.local_truck)
        truck_num_2 = len(base.other_truck)
        truck_num_3 = 0
        truck_num_4 = 0
        delay_1 = 0
        delay_2 = 0
        delay_3 = 0
        for order in base.orders:
            if order.trunk_id is not None:
                continue
            if order.class_of_delay_time == 1:
                delay_1 += 1
            elif order.class_of_delay_time == 2:
                delay_2 += 1
            elif order.class_of_delay_time == 3:
                delay_3 += 1
        dispatch_truck_num = truck_num_1 + truck_num_2
        around_base = str(base.near_base)
        temp_list = [id, name, position, truck_num_1, truck_num_2, truck_num_3, truck_num_4, delay_1,
                     delay_2, delay_3, dispatch_truck_num, around_base]
        l.append(temp_list)
    writer.write_data('base', l)


def write_truck(writer, day):
    truck_title = [u'板车ID', u'所属车队', u'所属网点', u'板车状态', u'当前位置（建模坐标）',
                   u'目的地编号   ', u'预计到达时间    ', u'订单编号1     ', u'订单编号2     ', u'订单编号3     ',
                   u'订单编号4     ', u'订单编号5     ', u'订单编号6     ', u'订单编号7     ', u'订单编号8     ',
                   u'订单编号9     ', u'订单编号10     ', u'订单编号11     ', u'订单编号12     ', u'订单编号13     ',
                   u'订单编号14     ']
    writer.write_title('truck', truck_title)
    l = []
    for index, truck in Trucks.items():
        all_list = []
        id = truck.license
        fleet = truck.fleet
        truck_base = Bases[truck.base].name
        target_position = ''
        target_time = ''
        orders = [''] * 15

        if truck.status in (Truck_status.TRUCK_IN_ORDER, Truck_status.TRUCK_IN_ORDER_DESTINATION):
            if truck.status == Truck_status.TRUCK_IN_ORDER:
                truck_state = u'本地等计划'
            else:
                truck_state = u'异地等计划'
            position = Bases[truck.current_base].name
            temp_list = [id, fleet, truck_base, truck_state, position, target_position, target_time, orders[0],
                         orders[1],
                         orders[2], orders[3], orders[4], orders[5], orders[6], orders[7], orders[8], orders[9],
                         orders[10],
                         orders[11], orders[12], orders[13], orders[14]]
            all_list.append(temp_list)
        elif truck.status == Truck_status.TRUCK_ON_ROAD:
            for index_position in range(len(truck.path) + 2):
                if index_position == 0:
                    truck_state = u'运输中(提货)'
                    position = Bases[truck.path[0].id].name
                    target_position = ''
                    target_time = ''
                    for order_index, order in enumerate(truck.orders):
                        orders[order_index] = order.id
                    temp_list = [id, fleet, truck_base, truck_state, position, target_position, target_time, orders[0],
                                 orders[1], orders[2], orders[3], orders[4], orders[5], orders[6], orders[7], orders[8],
                                 orders[9], orders[10], orders[11], orders[12], orders[13], orders[14]]
                    all_list.append(temp_list)
                if 0 < index_position < len(truck.path) + 1:
                    orders = [u''] * 15
                    if isinstance(truck.path[index_position - 1], Base):
                        flag = False
                        for order in truck.orders:
                            if order.base == truck.path[index_position - 1].id:
                                flag = True
                        if flag:
                            target_position = u'提货网点 : ' + truck.path[index_position - 1].name
                        else:
                            target_position = u'出发网点 : ' + truck.path[index_position - 1].name
                        for i, order in enumerate(truck.orders):
                            if order.base == truck.path[index_position - 1].id:
                                orders[i] = u"装车"
                    else:
                        target_position = u'交货4S店 : ' + truck.path[index_position - 1].name
                        for order_index, order in enumerate(truck.orders):
                            if order.destination == truck.path[index_position - 1].id:
                                orders[order_index] = u"卸载"
                    target_time = model_time_to_date_time(day, truck.times[index_position - 1])
                    temp_list = ['', '', '', '', '', target_position, target_time, orders[0],
                                 orders[1], orders[2], orders[3], orders[4], orders[5], orders[6], orders[7], orders[8],
                                 orders[9], orders[10], orders[11], orders[12], orders[13], orders[14]]
                    all_list.append(temp_list)
                if index_position == (len(truck.path) + 1):
                    target_position = u"入库网点 : " + Bases[truck.future_base].name
                    target_time = model_time_to_date_time(day, truck.times[-1])
                    orders = [u''] * 15
                    temp_list = ['', '', '', '', '', target_position, target_time, orders[0],
                                 orders[1], orders[2], orders[3], orders[4], orders[5], orders[6], orders[7], orders[8],
                                 orders[9], orders[10], orders[11], orders[12], orders[13], orders[14]]
                    all_list.append(temp_list)

        l += all_list
    writer.write_data('truck', l)


def write_order(writer, day):
    order_title = [u'订单ID       ', u'发运部编号', u'目的编号',
                   u'压板数量', u'压板天数', u'滞留天数级别', u'运输车ID']
    writer.write_title('order', order_title)
    day_data = []
    for order in Orders.values():
        data = [order.id, Bases[order.base].name, Destinations[order.destination].name, 1,
                order.delay_time, order.class_of_delay_time]
        if order.trunk_id is None:
            data.append(u'未派单')
        else:
            data.append(Trucks[order.trunk_id].license)
        # if order.class_of_delay_time == 1:
        #     orders_1 += 1
        # elif order.class_of_delay_time == 2:
        #     orders_2 += 1
        # elif order.class_of_delay_time == 3:
        #     orders_3 += 1
        day_data.append(data)
    writer.write_data('order', day_data)


def write_statistic(writer, day):
    statistic_title = [u'等计划', u'运输中(提货)', u'总计',
                       u'压板订单（1-5）', u'压板订单（5-10）',
                       u'压板订单（10-?）', u'总计']
    writer.write_title('statistic', statistic_title)
    truck_wait = 0
    truck_on_road = 0
    order_delay1 = 0
    order_delay2 = 0
    order_delay3 = 0
    for truck in Trucks.values():
        if truck.status in (Truck_status.TRUCK_IN_ORDER_DESTINATION, Truck_status.TRUCK_IN_ORDER):
            truck_wait += 1
        else:
            truck_on_road += 1
    for order in Orders.values():
        if order.trunk_id is None and order.class_of_delay_time == 1:
            order_delay1 += 1
        elif order.trunk_id is None and order.class_of_delay_time == 2:
            order_delay2 += 1
        if order.trunk_id is None and order.class_of_delay_time == 3:
            order_delay3 += 1
    l = [[truck_wait, truck_on_road, truck_wait + truck_on_road, order_delay1, order_delay2, order_delay3,
         order_delay3 + order_delay2 + order_delay1]]
    writer.write_data('statistic', l)


def write_excel(day):
    writer = Writer(day)
    write_base(writer, day)
    write_truck(writer, day)
    write_order(writer, day)
    write_statistic(writer, day)
    writer.save()
