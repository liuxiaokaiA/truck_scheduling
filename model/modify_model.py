# coding: utf-8
# 封装其他模块对模型的修改接口
# 外部模块只能通过本文件的函数对模型进行修改

from global_data import SUCCESS


# truck接单，修改模型相关状态：truck/order/base
# 传入参数为object
# 返回是否修改成功
def trunk_take_orders(trunk, orders):
    result = SUCCESS

    return result
