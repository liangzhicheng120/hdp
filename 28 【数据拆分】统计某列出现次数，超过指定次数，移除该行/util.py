# coding=utf-8
import os
import sys
import re
import chardet
import linecache
import random
import time
from functools import wraps


def utf8_2_gbk(str):
    '''
    utf-8转gbk
    :param str: 字符串
    :return: 转码后的字符串
    '''
    result = str.decode("utf-8").encode("gbk", "ignore")
    return result


def gbk_2_utf8(str):
    '''
    gbk转utf-8
    :param str: 字符串
    :return: 转码后的字符串
    '''
    result = str.decode("gbk").encode("utf-8", "ignore")
    return result


def create_word_list(file_name, rows_list):
    '''
    读入txt文件，返回一个编码为gbk的集合
    :param file_name:txt文件名称
    :return:编码为gbk的集合
    '''
    a = []
    try:
        if rows_list[1] <= rows_list[0] and rows_list[1] != 0:
            f = open(file_name, "rb")
            next(f)
            for line in f:
                line_list = line.strip().split("\t")
                word = line_list[rows_list[1] - 1].decode("utf-8").encode("gbk", "ignore")
                a.append(word)
        else:
            print c.OPEN_LINE_ERROR
    except Exception, e:
        if type(e) == UnicodeDecodeError:
            f = open(file_name, "rb")
            next(f)
            for line in f:
                line_list = line.strip().split("\t")
                a.append(line_list[rows_list[1] - 1])
        elif type(e) == IOError:
            print c.OPEN_FILE_ERROR
        else:
            print e
    finally:
        f.close()
        return a


def create_and_list(word):
    '''
    创建and关系列表
    :param word:要拆分的内容
    :return: 拆分后的列表
    '''
    split_word = word.strip().split("&")
    return split_word


def create_or_list(word):
    '''
    创建and关系列表
    :param content:要拆分的内容
    :return: 拆分后的列表
    '''
    split_word = word.strip().split("|")
    return split_word


def create_content(line, row_num):
    '''
    以逗号分隔内容，返回指定列
    :param line: 行数
    :param row_num: 指定列
    :return:某行指定列内容
    '''
    split_line = line.strip().split(",")[row_num - 1]
    return split_line


def fetch_n_rows(source_file_name, result_file_name, rows):
    '''
    拆分前n行数据
    :param source_file_name: 数据源
    :param result_file_name: 拆分后结果
    :param rows: 要拆分的行数
    :return:拆分后的文件
    '''
    result_file = file(result_file_name, "w+")
    source_file_head = create_file_head(source_file_name)
    result_file_body = linecache.getlines(source_file_name)[1:rows]
    result_file.writelines(source_file_head)
    result_file.writelines(result_file_body)
    result_file.close()


def print_any_list(any_list):
    '''
    向控制台循环输出列表中的内容
    :param any_list:
    :return:
    '''
    i = 0
    for (num, value) in enumerate(any_list):
        i = i + 1
        print "row is:", num + 1, "\tthe value is:", value.strip()
    print "total row is:", i


def create_file_head(file_name, *list):
    '''
    获取文件标题
    :param file_name:文件名
    :return: 文件标题（字符串）
    '''
    file_head = linecache.getline(utf8_2_gbk(file_name), 1).strip()
    if len(list) != 0:
        file_head = file_head + "," + ",".join(map(utf8_2_gbk, list[0]))
    file_head = file_head + "\n"
    return file_head


def create_file_body(file_name):
    '''
    获取文件主体内容
    :param file_name:文件名
    :return: 文件主体（列表）
    '''
    file_body = linecache.getlines(utf8_2_gbk(file_name))[1:]
    return file_body


def create_random_file(source_file_name, result_file_name, row):
    '''
    产生一个随机行数的文件(不计算文件标题行)
    :param source_file_name:源文件
    :param result_file_name: 目标文件
    :param row: 随机行数
    :return:
    '''
    result_file_body = []
    result_file = open(result_file_name, "w+")
    result_file_head = create_file_head(source_file_name)
    result_file.writelines(result_file_head)
    source_file_body = create_file_body(source_file_name)
    try:
        random_row_list = random.sample(range(1, len(source_file_body)), row)
        for random_row in random_row_list:
            result_file_body.append(linecache.getline(source_file_name, random_row))
        result_file.writelines(result_file_body)
    except Exception, e:
        if type(e) == ValueError:
            print c.ROW_VALUE_ERROR
        else:
            print Exception, e
    finally:
        result_file.close()


def modify_file_column(dispose_list, function, dispose_column):
    '''
    对某列文本数据进行处理
    :param function: 处理列的函数
    :param dispose_list: 待处理列表
    :param dispose_column: 待处理列
    :return: 处理后的列表
    '''
    modify_file = []
    for dispose_line in dispose_list:
        content = dispose_line.strip().split(",")
        total_column = len(content)
        left = ",".join(content[0:dispose_column - 1]) + ","
        center = "," + function(content[dispose_column]) + ","
        right = ",".join(content[dispose_column + 1:total_column]) + "\n"
        modify_file.append(left + center + right)
    return modify_file


def create_result_file(result_file_name, result_file_head, result_file_body):
    '''
    生成目标文件
    :param result_file_name: 目标文件名称
    :param result_file_head: 目标文件标题
    :param result_file_body: 目标文件主体
    :return:
    '''
    result_file = file(utf8_2_gbk(result_file_name), "w+")
    result_file.writelines(result_file_head)
    result_file.writelines(result_file_body)
    result_file.close()


def list_2_set(list):
    '''
    列白哦列表转集合
    :param list:列表
    :return:集合
    '''
    list_set = set()
    for line in list:
        list_set.add(line.strip())
    return list_set


def fn_timer(function):
    '''
    计算程序运行时间
    :param function:
    :return:
    '''

    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.clock()
        result = function(*args, **kwargs)
        t1 = time.clock()
        print ("Total time running %s: %s s" % (function.func_name, str(t1 - t0)))
        return result

    return function_timer
