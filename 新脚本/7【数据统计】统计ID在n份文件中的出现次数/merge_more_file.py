#!/bin/bash
# -*- coding=utf-8 -*-
# -*-author=liangzhicheng-*-
import sys
import re
import util as u
import os
import traceback

'''
功能说明:
将指定路径的文件合并成一个文件
数据文件放在source中,文件格式为csv
数据文件只有一列为id列
'''

#######################参数说明#######################
RESULT_FILE = '统计.txt'  # 输出文件
#####################################################
count_dict = {}
file_dict = {}

FILE_PATH = sys.path[0] + '\\source'


def rm_repeat(file_list):
    rm_set = set()
    for line in file_list:
        content = u.create_content(line, 1)
        rm_set.add(content.replace('"', '') + '\n')
    return list(rm_set)


if __name__ == '__main__':

    try:
        print u.utf8_2_gbk('开始执行')
        file_list = u.GetFileList(FILE_PATH, [])
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
        count_file.close()

        u.writeDictFile(RESULT_FILE, count_dict, 1)
        print u.utf8_2_gbk('执行完毕')
        print u.utf8_2_gbk('输出文件路径:') + sys.path[0] + u.utf8_2_gbk('\\' + RESULT_FILE)
    except:
        traceback.print_exc()
        print '=============================================================='
        print u.utf8_2_gbk('运行出错')
        print u.utf8_2_gbk('常见错误')
        print u.utf8_2_gbk('IndexError: list index out of range')
        print u.utf8_2_gbk('匹配列选择错误或source文件夹为空或label文件夹为空')
        print '=============================================================='
        raw_input('Press Enter to exit...')
    os.remove('total.csv')
    
