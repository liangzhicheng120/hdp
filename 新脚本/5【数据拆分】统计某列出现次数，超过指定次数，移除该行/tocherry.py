#! /usr/bin/python
# -*-coding=utf-8-*-
# -*-author=liangzhicheng-*-
import sys
import os
import re
import util as u
import constants as c
import traceback

'''
功能说明:
统计某列出现次数，超过指定次数，移除该行
数据文件放在source文件夹,数据文件为csv,gbk编码
'''

##############参数说明##############
COLUMN = 1  # 要处理的列数
NUMBER = 100  # 出现的次数
###################################

SOURCE_NAME, SOURCE_FILE = u.getFirstFile('csv')  # 输入文件
SAVE_FILE = u.changeFileName(SOURCE_NAME, '少于' + str(NUMBER) + '次.csv')  # 不符合条件的输出文件
REMOVE_FILE = u.changeFileName(SOURCE_NAME, '大于等于' + str(NUMBER) + '次.csv')  # 符合条件的输出文件（大于等于101次）
save_list = []  # 保存保留文件行号
remove_list = []  # 保存过滤文件行号
content_list = []
save_file_list = []
remove_file_list = []
res = {}


def remove_linebreak(line):
    return line.strip()


def create_content_list(list):
    for line in list:
        line = line.strip().split(",")[COLUMN - 1]
        content_list.append(line)


def factory(body_list):
    count = 0
    for line in result_file_body:
        count += 1
        content = u.create_content(line, COLUMN)
        res[content] = str(res.get(content, 0)) + "," + str(count)

    for key, value in res.items():
        rowNum_list = value[2:].split(",")
        if len(rowNum_list) >= NUMBER:
            for num in rowNum_list:
                remove_list.append(num)
        else:
            for num in rowNum_list:
                save_list.append(num)


if __name__ == "__main__":

    try:
        print u.utf8_2_gbk('开始执行')
        result_file_head = u.create_file_head(SOURCE_FILE)  # 文件标题
        result_file_body = u.create_file_body(SOURCE_FILE)  # 文件内容
        factory(result_file_body)  # 构造输出文件
        for num in save_list:
            save_file_list.append(result_file_body[int(num) - 1])

        for num in remove_list:
            remove_file_list.append(result_file_body[int(num) - 1])

        print u.utf8_2_gbk(SAVE_FILE + '行数:' + str(len(save_file_list)))
        print u.utf8_2_gbk(REMOVE_FILE + '行数:' + str(len(remove_file_list)))
        u.create_result_file(REMOVE_FILE, result_file_head, remove_file_list)  # 符合条件的输出文件（大于等于101次）
        u.create_result_file(SAVE_FILE, result_file_head, save_file_list)  # 不符合条件的输出文件
    except:
        traceback.print_exc()
        print '=============================================================='
        print u.utf8_2_gbk('运行出错')
        print u.utf8_2_gbk('常见错误')
        print u.utf8_2_gbk('IndexError: list index out of range')
        print u.utf8_2_gbk('匹配列选择错误或source文件夹为空或label文件夹为空')
        print '=============================================================='
        raw_input('Press Enter to exit...')
