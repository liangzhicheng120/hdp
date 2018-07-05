#! /usr/bin/python
# coding=utf-8
import sys
import os
import re
import util as u
import constants as c

# 功能说明:
# 统计某列出现次数，超过指定次数，移除该行

##############参数说明##############
SOURCE_FILE = "支付宝理财-不含关键词-聚类.csv"  # 输入文件
SAVE_FILE = "save.csv"  # 不符合条件的输出文件
REMOVE_FILE = "remove.csv"  # 符合条件的输出文件（大于等于101次）
COLUMN = 1  # 要处理的列数
NUMBER = 100  # 出现的次数

###################################
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
    result_file_head = u.create_file_head(SOURCE_FILE)  # 文件标题

    result_file_body = u.create_file_body(SOURCE_FILE)  # 文件内容

    factory(result_file_body)  # 构造输出文件

    for num in save_list:
        save_file_list.append(result_file_body[int(num) - 1])

    for num in remove_list:
        remove_file_list.append(result_file_body[int(num) - 1])

    u.create_result_file(REMOVE_FILE, result_file_head, remove_file_list)  # 符合条件的输出文件（大于等于101次）

    u.create_result_file(SAVE_FILE, result_file_head, save_file_list)  # 不符合条件的输出文件
