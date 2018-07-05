#!/bin/bash
# -*- coding=utf-8 -*-
# -*- author=liangzhicheng -*-
import re
import os
import util as u
import sys
import traceback

'''
功能说明:
将数据文件拆分成一份含关键词,一份不含关键词
关键词之间用逗号隔开,数据文件问csv,gbk编码,匹配词文件txt,gbk编码,匹配词支持中英文,支持大小写,支持精确匹配
关键词放在label文件夹,数据文件放在source文件夹
'''
####################参数和说明#####################
COLUMN = 5  # 需要匹配的列
ACCURATE = True  # 选择是否精确匹配
##################################################

SOURCE, SOURCEPATH = u.getFirstFile('csv')
LABEL, LABELPATH = u.getFirstFile('txt')

result_list = []
remove_list = []


def createPattern(fileName):
    content = ''
    f = open(u.utf8_2_gbk(fileName))
    for line in f:
        if line[:-1].strip():
            if ACCURATE:
                content += '|' + '^' + line.strip() + '$'
            else:
                content += '|' + '.*' + line.strip() + '.*'
    f.close()
    return content[1:].lower()


if __name__ == '__main__':
    try:
        source_file_body = u.create_file_body(SOURCEPATH)
        source_file_head = u.create_file_head(SOURCEPATH)
        m = createPattern(LABELPATH)
        print m
        print '===============>>' + u.utf8_2_gbk('若乱码,匹配词文件请使用gbk编码') + '<<==================='
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
        u.create_result_file(u.changeFileName(SOURCE, '-含关键词.csv'), source_file_head, result_list)
        u.create_result_file(u.changeFileName(SOURCE, '-不含关键词.csv'), source_file_head, remove_list)
    except:
        traceback.print_exc()
        print '=============================================================='
        print u.utf8_2_gbk('运行出错')
        print u.utf8_2_gbk('常见错误')
        print u.utf8_2_gbk('IndexError: list index out of range')
        print u.utf8_2_gbk('匹配列选择错误或source文件夹为空或label文件夹为空')
        print '=============================================================='
        raw_input('Press Enter to exit...')
