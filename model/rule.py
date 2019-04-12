# coding: utf-8
# 调度规则，模型提供规则即可，模型不用关心规则如何在算法中实现

MAX = 100000

rules = {
    # order的优先级划分
    'order_level': [
        {
            # 0-5 天的order
            'start': 0,
            'end': 5,
            'level': 1,
        },
        {
            # 6-10 天的order
            'start': 6,
            'end': 10,
            'level': 2,
        },
        {
            # >10 天的order
            'start': 11,
            'end': MAX,
            'level': 3,
        }
    ],
    'must_take_order_level': (3, 11),
    # 板车最少运输订单个数
    'truck_take_order_min': 8,
    # 板车异地滞留最长时间
    'truck_delay_max': MAX,
    # truck最远接单距离
    'max_distance': 500,
}

# 策略执行等级
levels = [
    # 返程板车优先
    'get_truck_return',
    # 顺路订单凑整运输
    'get_order_nearby',
    # 散单拼单
    'ga',
]
