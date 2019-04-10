# coding: utf-8
from global_data import Bases
from model.base_model.base import Base


class Test_Base():
    def test_base_position(self):
        base = Base(u'北京')
        base.set_position()

        # assert Bases == {u'北京': base}
        # assert base.x == 1
        # assert base.y == 1
        # assert base.get_id() == u'北京'
