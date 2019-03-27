# coding: utf-8
# 本文件封装模型数据的获取
# 将模型与算法分隔开
# 算法只需使用获取之后的数据计算即可，不用关系模型的具体信息
# 模型修改不会影响到算法，只需修改数据获取函数即可
# 本文件只需调用model/get_model_data.py的接口，不用关心模型的结构
# 本文件涉及到的都是模型的object的id,不会使用具体的object

from model.get_model_data import *


base_near_base = {}


def update_base_near_base():
    pass
