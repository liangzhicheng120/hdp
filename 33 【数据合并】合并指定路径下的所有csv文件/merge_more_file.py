#!/bin/bash
# coding=utf-8
import sys
import re
import util as u
import os

'''
功能说明:将指定路径的文件合并成一个文件(文件格式为csv)
'''

##################参数说明#################
FILE_PATH = r'G:\merge_n_file\data'  # 文件路径
RESULT_FILE = 'result.csv'  # 合并之后的文件
RESULT_HEAD = r'G:\merge_n_file\data\3779_利鑫－999道私房菜.csv'  # 指定合并后的文件标题基准
##########################################
file_dict = {}

if __name__ == '__main__':

    file_list = u.GetFileList(u.utf8_2_gbk(FILE_PATH), [])
    for f in file_list:
        file_dict[f.encode('gbk')] = u.create_file_body(f.encode('utf-8'))

    result_file = file(RESULT_FILE, 'w+')
    result_file_head = u.create_file_head(RESULT_HEAD)
    result_file.write(result_file_head)

    for key, value in file_dict.items():
        result_file.writelines(value)
    result_file.close()
