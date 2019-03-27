# coding: utf-8
# 本文件封装模型数据的获取，供algorithm/data/compute_data.py调用
# 提供模型的对外接口
# 其他模块不会调用base_model文件夹内的任何东西
# 其他模块均通过本文件来获取模型的数据


# 获取用于计算的所有数据
# 返回所有未派订单和可用车辆
def get_compute_data():
    compute_data = {
        # 未派订单 id
        'orders': [],
        # 可用车辆 id
        'trucks': [],
    }
    return compute_data
