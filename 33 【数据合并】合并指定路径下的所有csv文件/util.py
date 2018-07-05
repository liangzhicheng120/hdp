# coding=utf-8
import os
import sys
import re
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
        if list[0] == 'left':
            file_head = ",".join(map(utf8_2_gbk, list[1])) + "," + file_head
        if list[0] == 'right':
            file_head = file_head + "," + ",".join(map(utf8_2_gbk, list[1]))
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


def print_any_dict(dict):
    '''
    打印字典中的内容
    :param dict: 字典
    :return:
    '''
    for key, value in dict.items():
        print key, value


def remove_blank_line(file_name):
    '''
    移除文件中的空行
    :param file_name:
    :return:
    '''
    new_word_list = []
    word_list = linecache.getlines(utf8_2_gbk(file_name))
    for line in word_list:
        if line[:-1].strip():
            new_word_list.append(line)
    return new_word_list


def create_match_words(file_name):
    '''
    创建匹配词，过滤词文本
    :param file_name: 文件名称
    :return: 文件列表[中文，英文]
    '''
    words = []
    try:
        words = map(utf8_2_gbk, remove_blank_line(file_name))
        words = list(set(words))
        words = build_word_cup(words)
    except Exception, e:
        words = remove_blank_line(file_name)
        words = list(set(words))
        words = build_word_cup(words)
    finally:
        return words


def build_word_cup(word_list):
    '''
    将原列表中的中英文分开
    :param word_list: [中英文]
    :return: [中文，英文]
    '''
    words = []
    chinese = []
    english = []
    p = re.compile(r'^[A-z].*[\w]$')
    for line in word_list:
        if p.match(line):
            english.append(line)
        else:
            chinese.append(line)
    words.append(chinese)
    words.append(english)
    return words


def build_pattern(chinese_list, english_list):
    '''
    构造匹配关键词正则表达式
    :param filter_words:chinese_list,english_list
    :param type: chinese,english
    :return:pattern
    '''

    def build_chinese_pattrns(line):
        str = line.strip().split(' ')
        line = '.*' + line.strip().replace(' ', '.*') + '.*'
        if len(str) == 2:
            line = line + '|' + '.*' + str[1] + '.*' + str[0] + '.*'
        return line

    def build_english_pattrns(line):
        line = '.*' + line.strip() + '.*'
        return line

    e_pattrns = '|'.join(map(build_english_pattrns, english_list))
    c_pattrns = '|'.join(map(build_chinese_pattrns, chinese_list))

    c_len = len(c_pattrns)
    e_len = len(e_pattrns)

    if c_len != 0 and e_len != 0:
        pattrns = c_pattrns + '|' + e_pattrns
    if c_len != 0 and e_len == 0:
        pattrns = c_pattrns
    if c_len == 0 and e_len != 0:
        pattrns = e_pattrns

    print pattrns
    pattern = re.compile(r'(' + pattrns + ')')

    return pattern


def print_len(list):
    '''
    打印列表长度
    :param list:
    :return:
    '''
    print len(list)


def print_type(any):
    '''
    打印类型
    :param any:
    :return:
    '''
    print type(any)


def build_match_label(list):
    '''
    构造匹配词列表
    :param list:
    :return:
    '''
    keywords = {}
    if len(list[0]) != 0:
        for line in list[0]:
            var = line.strip().split('\t')
            keywords[var[1]] = str(keywords.get(var[1], 0)) + "|" + '.*' + var[0] + '.*'
    if len(list[1]) != 0:
        for line in list[1]:
            var = line.strip().split('\t')
            keywords[var[1]] = str(keywords.get(var[1], 0)) + "|" + '.*' + var[0] + '.*'
    for key, value in keywords.items():
        keywords[key] = value[2:]
    return keywords


def GetFileList(dir, fileList):
    '''
    获取指定目录的所有文件
    :param dir:
    :param fileList:
    :return:
    '''
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir.decode('gbk'))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            GetFileList(newDir, fileList)
    return fileList
