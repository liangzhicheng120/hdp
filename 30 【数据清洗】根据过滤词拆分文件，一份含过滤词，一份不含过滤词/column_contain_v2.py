#!/bin/bash
# coding=utf-8
import sys
import os
import re
import util as u
import linecache
from collections import defaultdict
import multiprocessing

__author__ == 'liangzhicheng'
'''
根据过滤词拆分文件，一份含过滤词，一份不含过滤词
性能:输入文件100万行,过滤词文件1000行,执行时间约为15min,内存占用400mb
'''
#####################参数说明####################

COLUMN = 37  # 要清洗的数据在第几列
SOURCE_FILE = "test.csv"  # 输入文件
RESULT_FILE = "result.csv"  # 输出文件(不含关键词)
REMOVE_FILE = "remove.csv"  # 输出文件(含关键词)
FILETER_FILE = "filter.txt"  # 过滤词文件

################################################
result_list = []
remove_list = []

if __name__ == "__main__":

    result_file_head = u.create_file_head(SOURCE_FILE)
    result_file_body = u.create_file_body(SOURCE_FILE)

    words_file = u.create_match_words(FILETER_FILE)

    chiness_words = words_file[0]
    english_words = words_file[1]

    pattern = u.build_pattern(chiness_words, english_words)

    print 'start'
    for line in result_file_body:
        content = u.create_content(line, COLUMN)
        if pattern.match(content):
            remove_list.append(line)
        else:
            result_list.append(line)
    print 'end'

    u.create_result_file(RESULT_FILE, result_file_head, result_list)
    u.create_result_file(REMOVE_FILE, result_file_head, remove_list)
