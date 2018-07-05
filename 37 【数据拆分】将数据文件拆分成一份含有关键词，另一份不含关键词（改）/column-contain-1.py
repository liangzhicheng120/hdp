#!/bin/bash
# coding=utf-8
import re
import os
import util as u
import sys

'''
关键词之间用逗号隔开,数据文件问csv,gbk编码,匹配词文件txt,gbk编码,匹配词支持中英文,支持大小写
'''
####################参数和说明#####################
SOURCE_FILE = 'save.csv'  # 数据文件
MATCH_FILE = 'lvandhv.txt'  # 匹配词文件
COLUMN = 26  # 需要匹配的列
##################################################

result_list = []
remove_list = []


def createPattern(fileName):
    content = ''
    f = open(u.utf8_2_gbk(fileName))
    for line in f:
        if line[:-1].strip():
            content += '|' + '.*' + line.strip() + '.*'
    f.close()
    return content[1:].lower()


if __name__ == '__main__':
    source_file_body = u.create_file_body(SOURCE_FILE)
    source_file_head = u.create_file_head(SOURCE_FILE)
    m = createPattern(MATCH_FILE)
    print m + '===>>' + u.utf8_2_gbk('若乱码,匹配词文件请使用gbk编码')
    p = re.compile(m)
    print u.utf8_2_gbk('数据源文件行数:') + str(len(source_file_body))
    for line in source_file_body:
        content = u.create_content(line, COLUMN).lower()
        if p.match(content):
            result_list.append(line)
        else:
            remove_list.append(line)
    print u.utf8_2_gbk('不包含关键词行数:') + str(len(remove_list))
    print u.utf8_2_gbk('包含关键词行数:') + str(len(result_list))
    u.create_result_file(u.changeFileName(SOURCE_FILE, '-含关键词.csv'), source_file_head, result_list)
    u.create_result_file(u.changeFileName(SOURCE_FILE, '-不含关键词.csv'), source_file_head, remove_list)
    raw_input('Press Enter to exit...')
