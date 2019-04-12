# coding: utf-8
# 封装其他模块对模型的修改接口
# 外部模块只能通过本文件的函数对模型进行修改

from global_data import SUCCESS, Orders


# truck接单，修改模型相关状态：truck/order/base
# 传入参数为object
# 返回是否修改成功
def model_truck_take_orders(truck, orders):
    result = SUCCESS
    order_list = []
    for index in orders:
        order_list.append(Orders[index])

    truck.add_orders(order_list=order_list)
    for index in orders:
        Orders.remove(Orders[index])

    return result
