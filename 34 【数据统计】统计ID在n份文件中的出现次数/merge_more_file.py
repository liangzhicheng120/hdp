#!/bin/bash
# coding=utf-8
import sys
import re
import util as u
import os

'''
功能说明:将指定路径的文件合并成一个文件(文件格式为csv)
'''

#######################参数说明#######################
FILE_PATH = r'C:\Users\XinRui\Desktop\tolixing\data'  # 文件路径
RESULT_FILE = 'result.txt'  # 输出文件
#####################################################
count_dict = {}
file_dict = {}


def rm_repeat(file_list):
    rm_set = set()
    for line in file_list:
        content = u.create_content(line, 1)
        rm_set.add(content.replace('"', '') + '\n')
    return list(rm_set)


if __name__ == '__main__':

    file_list = u.GetFileList(u.utf8_2_gbk(FILE_PATH), [])
    for f in file_list:
        file_dict[f.encode('gbk')] = rm_repeat(u.create_file_body(f.encode('utf-8')))

    total_file = file('total.csv', 'w+')
    for key, value in file_dict.items():
        total_file.writelines(value)
    total_file.close()

    count_file = open('total.csv', 'rb')
    for line in count_file:
        content = u.create_content(line, 1)
        count_dict[content] = count_dict.get(content, 0) + 1

    result_file = file(RESULT_FILE, 'w+')
    for key, value in count_dict.items():
        result_file.write(key + '\t' + str(value) + '\n')
    result_file.close()

    os.remove('total.csv')