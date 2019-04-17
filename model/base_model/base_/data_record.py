# coding: utf-8

# coding: utf-8
import time

import xlwt
import logging
import os

from global_data import mode_start_time

log = logging.getLogger('default')


def timestamp_to_date_time(timestamp):
    timeTuple = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeTuple)[:-3]


def data_time_to_timestamp(datetime):
    st = time.strptime(datetime, '%Y-%m-%d %H:%M:%S')
    return time.mktime(st)


def model_time_to_date_time(day, hour):
    timestamp = mode_start_time + day * 24 * 3600 + hour * 3600
    return timestamp_to_date_time(timestamp)


# 获取字符串长度，一个中文的长度为2
def len_byte(value):
    length = len(value)
    utf8_length = len(value.encode('utf-8'))
    return int((utf8_length - length) / 2 + length)


# 确定栏位宽度
def set_width(result, worksheet):
    col_width = []
    for i in range(len(result)):
        col_width.append(len_byte(result[i]))
    # 设置栏位宽度，栏位宽度小于10时候采用默认宽度
    for i in range(len(col_width)):
        if col_width[i] > 10:
            worksheet.col(i).width = 256 * (col_width[i] + 1)


class Writer(object):
    def __init__(self, day):
        self.file_name = 'output/' + str(model_time_to_date_time(day, 0)[0:10]) + '.xls'
        self.handle = xlwt.Workbook(encoding='utf-8')
        self.rows = {
            'base': 1,
            'trunk': 1,
            'order': 1,
            'statistic': 1,
        }
        self.worksheet = {
            'base': self.handle.add_sheet(u'网点信息'),
            'trunk': self.handle.add_sheet(u'车辆信息'),
            'order': self.handle.add_sheet(u'订单信息'),
            'statistic': self.handle.add_sheet(u'总计'),
        }

    def write_data(self, name, data):
        if name not in self.worksheet:
            return
        for i in range(len(data)):
            rows = i + self.rows[name]
            for columns in range(len(data[i])):
                self.worksheet[name].write(rows, columns, label=data[i][columns])
        self.rows[name] += len(data)

    def write_title(self, name, title_list):
        if name not in self.worksheet:
            return
        set_width(title_list, self.worksheet[name])
        for columns in range(len(title_list)):
            self.worksheet[name].write(0, columns, label=title_list[columns])

    def save(self):
        if not os.path.exists('output'):
            os.mkdir('output')
        self.handle.save(self.file_name)
