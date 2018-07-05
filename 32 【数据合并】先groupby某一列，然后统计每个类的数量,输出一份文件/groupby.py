#!/bin/bash
# coding=utf-8
import re
import sys
import os
import util as u

'''
功能说明:先groupby某一列，然后统计每个类的数量,输出一份文件
'''

##############参数说明###############
SOURCE_FILE = 'hebing.csv'  # 输入文件
RESULT_FILE = 'result.csv'  # 输出文件
COLUMN = 1  # 要groupby和统计的列的列
####################################
count_dict = {}

if __name__ == '__main__':
    source_file_head = u.create_file_head(SOURCE_FILE, 'right', ['次数'])
    source_file_body = u.create_file_body(SOURCE_FILE)
    for line in source_file_body:
        content = u.create_content(line, COLUMN)
        count_dict[content] = count_dict.get(content, 0) + 1
    result_file = file(RESULT_FILE, 'w+')
    result_file.write(source_file_head)
    for key, value in count_dict.items():
        result_file.write(key + ',' + str(value) + '\n')
    result_file.close()
