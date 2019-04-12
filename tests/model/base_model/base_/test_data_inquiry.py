# coding: utf-8
from global_data import Bases
from model.base_model.base_.data_inquiry import DataInquiry
from model.base_model.base_.type import BASE, DESTINATION


class Test_Init_Data():

    def __init__(self):
        self.inquiry = DataInquiry()

    def test_get_position(self):
        base_position_x, base_position_y = self.inquiry.get_position(BASE, 0)
        destination_position_x, destination_position_y = self.inquiry.get_position(DESTINATION, 0)

        assert base_position_x - 4366.018 < 0.01
        assert base_position_y - 4529.621 < 0.01
        assert destination_position_x - 3684.558 < 0.01
        assert destination_position_y - 3996.274 < 0.01

    def test_get_distance(self):
        pass
        # distance_b_b = self.inquiry.get_distance(base_id_1=0, base_id_2=1)
        # distance_b_d = self.inquiry.get_distance(base_id_1=0, destination_id_1=0)
        # d
        # pass
