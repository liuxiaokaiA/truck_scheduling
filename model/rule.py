# coding: utf-8
MAX = 100000

rules = {
    # order的优先级划分
    'order_level': {
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
    },
    # 板车最少运输订单个数
    'truck_take_order_min': 8,
    # 板车异地滞留最长时间
    'truck_delay_max': MAX,
}

# 策略执行等级
levels = [
    # 返程板车优先
    'get_trunk_return',
    # 顺路订单凑整运输
    'get_order_nearby',
    # 散单拼单
    'ga',
]