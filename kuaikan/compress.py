# encoding:utf-8
"""
@Time    : 2020-05-09 14:02
@Author  : yshhuang@foxmail.com
@File    : compress.py
@Software: PyCharm
"""
import json
import csv

with open('/Volumes/develop/code-repository/python/dish/kuaikan/500k-1000k.csv', 'r') as f:
    spamreader = csv.reader(f, delimiter=',')
    sum_rate = 0
    i = 0
    for row in spamreader:
        i += 1
        sum_rate += int(row[4].replace(',', '')) / int(row[2].replace(',', ''))
    print(i)
    print(sum_rate / i)
