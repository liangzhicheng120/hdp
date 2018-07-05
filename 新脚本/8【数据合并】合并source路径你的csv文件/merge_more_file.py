#!/bin/bash
# -*- coding=utf-8 -*-
# -*- author=liangzhicheng -*-
import sys
import re
import util as u
import os
import traceback

'''
功能说明:将指定路径的csv文件合并成一个csv文件
'''

######################参数说明######################
RESULT_FILE = 'result.csv'  # 合并之后的文件

###################################################
file_dict = {}
FILE_PATH = sys.path[0] + '\\source'  # 文件路径
RESULT_HEAD = u.getFirstFile('csv')[1]  # 默认以第一个csv文件抬头为合并后的csv文件抬头
if __name__ == '__main__':
    try:
        print u.utf8_2_gbk('开始执行')
        file_list = u.GetFileList(FILE_PATH, [])
        for f in file_list:
            file_dict[f.encode('gbk')] = u.create_file_body(f.encode('utf-8'))
        result_file = file(u.utf8_2_gbk(RESULT_FILE), 'w+')
        result_file_head = u.create_file_head(RESULT_HEAD)
        result_file.write(result_file_head)
        for key, value in file_dict.items():
            result_file.writelines(value)
        result_file.close()
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
