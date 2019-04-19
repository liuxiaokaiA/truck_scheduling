# coding: utf-8
# 封装其他模块对模型的修改接口
# 外部模块只能通过本文件的函数对模型进行修改

from global_data import SUCCESS, Orders, Trucks, Bases

# truck接单，修改模型相关状态：truck/order/base
# 传入参数为object
# 返回是否修改成功
from model.base_model.base import Base


def model_truck_take_orders(truck_id, order_ids):
    result = SUCCESS
    truck = Trucks[truck_id]
    if truck_id in Bases[truck.current_base].local_truck:
        Bases[truck.current_base].local_truck.remove(truck_id)
    elif truck_id in Bases[truck.current_base].other_truck:
        Bases[truck.current_base].other_truck.remove(truck_id)
    truck.add_orders(order_list=order_ids)
    for order_id in order_ids:
        Orders[order_id].trunk_id = truck_id
        # del Orders[order_id]

    return result
