# coding: utf-8
# 封装其他模块对模型的修改接口
# 外部模块只能通过本文件的函数对模型进行修改

from global_data import SUCCESS, Orders, Trucks


# truck接单，修改模型相关状态：truck/order/base
# 传入参数为object
# 返回是否修改成功
def model_truck_take_orders(truck_id, order_ids):
    result = SUCCESS
    truck = Trucks[truck_id]
    truck.add_orders(order_list=order_ids)
    temp_order = []
    for order in Orders:
        if order.id in order_ids:
            temp_order.append(order)
    for order in temp_order:
        Orders.remove(order)
    return result
