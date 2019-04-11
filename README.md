Truck_Scheduling
====


Testing
-------

You need `pytest`, then:

    make test

Style
-----

Run:

    make flake8


Requirement
-----------

首先在 *setup.py* 中写入依赖， 安装 *pip-tools* ，然后执行:

    pip-compile                          # 更新 requirements.txt
    pip-compile --upgrade                # 升级 all packages
    pip-compile --upgrade-package flask  # 升级 a pacakge



程序结构说明
==========

程序结构如下：
	
	# 物流调度
	truck_scheduling
	├── algorithm                # 算法模块
	│   ├── base 
	│   │   ├── basic_algorithm             # 基础算法文件夹
	│   │   │   └── deap_scoop_ga.py        # 基于 deap+scoop 的 ga 封装
	│   │   ├── data             # 算法模块数据文件夹
	│   │   │   ├── data.py      # 算法需要数据
	│   │   │   └── rule.py      # 算法需要规则
	│   │   └── model_process.py # 模型修改接口
	│   └── truck_scheduling.py  # 物流调度算法
	├── conf
	│   └── default.conf         # 配置文件 
	├── logs                     # 日志文件夹
	├── model                    # 模型文件夹
	│   ├── base_model           # 物流调度模型
	│   │   ├── base_            # 原始数据操作、基类文件夹
	│   │   │   ├── position_data           # 原始数据存放文件夹
	│   │   │   ├── data_inquiry.py         # 原始数据查询接口
	│   │   │   ├── init_data.py            # 原始数据读取
	│   │   │   ├── inquiry_api.py          # 业务逻辑查询接口
	│   │   │   ├── path.py                 # 路径优化
	│   │   │   ├── position.py             # 位置基类
	│   │   │   ├── truck_inquiry_api.py    # 板车查询原始数据接口
	│   │   │   └── type.py                 # 类型文件
	│   │   ├── base.py          # 网点模型
	│   │   ├── destination.py   # 4S店模型
	│   │   ├── order.py         # 订单模型
	│   │   └── truck.py         # 板车模型
	│   ├── get_model_data.py    # 模型对外提供数据获取接口
	│   ├── modify_model.py      # 模型对外提供修改接口
	│   ├── output.py  	         # 模型对外提供输出数据获取接口
	│   └── rule.py              # 模型对外提供计算规则接口
	├── output                   # 输出模块
	├── tests                    # 测试模块
	├── utils                    # 工具模块
	│   ├── load_conf.py         # 配置文件读取
	│   └── log.py               # 日志
	├── global_data.py           # 全局变量
	└── main.py                  # 主程序
	
