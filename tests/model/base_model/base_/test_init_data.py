# coding: utf-8
from global_data import Bases
from model.base_model.base_.init_data import Init_data
from model.base_model.base_.type import BASE, DESTINATION


class Test_Init_Data():
    def test_get_position(self):
        init_data = Init_data()
        base_position_x, base_position_y = init_data.get_position(BASE, 0)
        destination_position_x, destination_position_y = init_data.get_position(DESTINATION, 0)

        assert base_position_x - 4366.018 < 0.01
        assert base_position_y - 4529.621 < 0.01
        assert destination_position_x - 3684.558 < 0.01
        assert destination_position_y - 3996.274 < 0.01
