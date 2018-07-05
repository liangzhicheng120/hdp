#!/usr/bin/python
# coding=utf-8

import sys

# 功能介绍
# 根据某一列开头的字符，进行过滤

####################以下是参数######################

COLUMN = 37  # 要清洗的数据在第几列
FILE_NAME = "sample_min_test.csv"  # 数据文件，必须是立方导出的数据
FILTER_WORDS = "filter_words.txt"  # 过滤词文件
COLUMN_TOTAL = 45  # 总列数
OUTPUT_FILE = "result.csv"  # 不含过滤词的文件名
REMOVE_FILE = "removed.csv"  # 含过滤词的文件名

####################以上是参数######################
DELIMITER = ","
CODING = "gbk"
filter_words = []
flag = 0
header = ""

if __name__ == "__main__":
    # 输出不符合过滤的文件
    ResultWriter = file(OUTPUT_FILE, "w+")
    # 输出符合过滤的文件
    FilteredWriter = file(REMOVE_FILE, "w+")
    # 打开数据文件
    reader = open(FILE_NAME, 'rb')
    # 读取过滤词文件，并将过滤词文件转码成gbk
    with open(FILTER_WORDS, "rb") as f:
        for line in f:
            word = line.strip().decode('utf-8', 'ignore').encode('gbk', 'ignore')
            if word is not None and word != "":
                filter_words.append(word)

    for line in reader:
        # 保存数据文件标题并将标题写入输出文件
        if flag == 0:
            header = line
            flag = 1
            ResultWriter.write(header.strip() + "\n")
            FilteredWriter.write(header.strip() + "\n")
            continue
        # 读取每一行数据并将数据以逗号分隔，返回一个列表
        data = line.strip().split(DELIMITER)
        # 对于乱行的数据不做处理
        if data < COLUMN_TOTAL:
            continue
        # 返回该行中含指定列的数据列表
        content = data[COLUMN - 1]
        # 设置分离标识
        removed = False

        for word in filter_words:
            # 每行开头符合过滤词的行写入含过滤词的文件
            if content.startswith(word):
                FilteredWriter.write(line.strip() + "\n")
                removed = True
                break
        # 该行不含过滤词，则将该行写入不含过滤词的文件
        if not removed:
            ResultWriter.write(line.strip() + "\n")

    FilteredWriter.close()
    ResultWriter.close()
    reader.close()
