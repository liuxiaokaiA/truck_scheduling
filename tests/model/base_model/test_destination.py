# coding: utf-8
from global_data import Destinations
from model.base_model.destination import Destination


class Test_Destination():
    def test_dest_position(self):
        dest = Destination(u'北京')
        dest.set_position()

        # assert Destinations == {u'北京': dest}
        # assert dest.x == 2
        # assert dest.y == 2
        # assert dest.get_id() == u'北京'
