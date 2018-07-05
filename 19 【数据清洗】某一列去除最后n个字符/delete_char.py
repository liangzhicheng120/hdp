#!/usr/bin/python
# coding=utf-8
import sys
import re

# 功能介绍：
# 某一列去除最后n个字符

####################以下是参数######################

COLUMN = 8  # 要清洗的数据在第几列
FILE_NAME = "sample_min_test.csv"  # 数据文件，必须是立方导出的数据
COLUMN_TOTAL = 42  # 总列数
NUMBER = 4  # 某一列去除最后n个字符
OUTPUT_FILE = "result.csv"  # 输出结果文件名

####################以上是参数######################
DELIMITER = ","
CODING = "gbk"

if __name__ == "__main__":
    ResultWriter = file(OUTPUT_FILE, "w+")
    reader = open(FILE_NAME, 'rb')
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')

    ResultWriter.write(next(reader).strip() + "\n")
    for line in reader:
        data = line.strip().split(DELIMITER)
        if data < COLUMN_TOTAL:
            continue
        elif re.match('^[0-9a-zA-Z]+$', data[COLUMN - 1]):
            data[COLUMN - 1] = data[COLUMN - 1][:-NUMBER]
        elif zhPattern.search(data[COLUMN - 1]):
            data[COLUMN - 1] = data[COLUMN - 1][:-NUMBER * 2]
        else:
            data[COLUMN - 1] = data[COLUMN - 1][:-NUMBER * 2]
        ResultWriter.write(",".join(data) + "\n")
    ResultWriter.close()
    reader.close()
