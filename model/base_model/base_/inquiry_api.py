# -*- encoding: utf-8 -*-
from .data_inquiry import DataInquiry


# 封装查询方法，比如查询附近的trucks等
# 主要是对业务逻辑提供查询接口
# 继承自DataInquiry
# DataInquiry封装了基本的数据查询方法
# 如果base/destination查询结果是一样的，那就只封装一个类
# 否则，封装成两个类
class InquiryAPI(DataInquiry):
    type = None

    def __init__(self):
        super(InquiryAPI, self).__init__()

    # 封装base/destination调用的查询函数
