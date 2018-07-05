#!/usr/bin/python
# coding=utf-8

import sys
import random
import linecache
import os

# 功能说明：
# 按在某列完全匹配关键词的条件下，随机抽取若干行数据

####################以下是参数######################

COLUMN = 42  # 要清洗的数据在第几列
RANDOMNUM = 10  # 随机选取的行数
FILE_NAME = "sample_min_test.csv"  # 数据文件，必须是立方导出的数据
FILTER_WORDS = "sick.txt"  # 过滤词文件
COLUMN_TOTAL = 45  # 总列数
REMOVE_FILE = "removed.csv"  # 被过滤的数据数据文件名
RANDOM_FILE = "random.csv"  # 随机抽取的数据文件名
####################以上是参数######################
DELIMITER = ","
DELIMITER2 = " "  # 过滤词间的分隔符
CODING = "gbk"
filter_words = []


def createRemove():
    flag = 0
    header = ""
    FilteredWriter = file(REMOVE_FILE, "w+")
    reader = open(FILE_NAME, 'rb')
    with open(FILTER_WORDS, "rb") as f:
        for line in f:
            word = line.strip().decode('utf-8').encode('gbk', 'ignore')
            if word is not None and word != "":
                filter_words.append(word)

    # next(reader)  # 忽略第一行（抬头）
    for line in reader:
        if flag == 0:
            header = line
            flag = 1
            FilteredWriter.write(header.strip() + "\n")
            continue
        data = line.strip().split(DELIMITER)
        if data < COLUMN_TOTAL:
            continue
        content = data[COLUMN - 1].decode(CODING).encode(CODING)
        removed = False
        for word in filter_words:
            filterArr = word.strip().split(DELIMITER2)
            count = 0
            for fil in filterArr:
                if fil in content:
                    count = count + 1
                else:
                    break
            if count == len(filterArr):
                FilteredWriter.write(line.strip() + "\n")
                removed = True
                break
    FilteredWriter.close()
    reader.close()
    return header


def random_read(num):
    count = len(open(REMOVE_FILE, 'rU').readlines())  # 获取行数
    return random.sample(range(1, count), num)


def row():
    return len(open(REMOVE_FILE, 'rU').readlines())


if __name__ == "__main__":
    header = createRemove()
    random_file = open(RANDOM_FILE, "w+")
    row = row()
    random_file.write(header.strip() + "\n")
    count = 0
    if RANDOMNUM <= row:
        random_row = random_read(RANDOMNUM)
        if random_row is not None:
            for i in random_row:
                random_file.write(linecache.getline(REMOVE_FILE, i))  # 随机读取某行
                count = count + 1
    else:
        random_file.write("随机行数过大，不超过{0}".decode('utf-8').encode('gbk', 'ignore').format(row))

    if count == RANDOMNUM:
        os.remove(REMOVE_FILE)
