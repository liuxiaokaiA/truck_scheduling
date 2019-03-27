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
