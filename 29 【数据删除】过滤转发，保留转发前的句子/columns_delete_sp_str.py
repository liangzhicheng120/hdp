#!/usr/bin/python
# coding=utf-8

import sys

import io

import codecs

import re

####################以下是参数######################

FILE_NAME = "walmart_demo.csv"  # 数据文件，必须是立方导出的数据
COLUMN = 57  # 要清洗的数据在第几列
COLUMN_TOTAL = 63  # 总列数
FILTER_WORDS = "//@"  # 过滤词

OUTPUT_FILE = "result.csv"  # 输出结果文件名
REMOVE_FILE = "removed.txt"  # 被过滤的数据数据文件名

FLAG = 1  # 是否含有抬头 1代表有， 0代表没

# removed.txt文件的内容是被删掉的\\@内容
# result.csv 文件是删除\\@后的内容

####################以上是参数######################


DELIMITER = ","
CODING = "gbk"

if __name__ == "__main__":
    ResultWriter = file(OUTPUT_FILE, "w+")
    FilteredWriter = file(REMOVE_FILE, "w+")
    reader = open(FILE_NAME, 'rb')
    print "start"
    for line in reader:
        if FLAG == 1:
            ResultWriter.write(line.strip() + "\n")
            FLAG = 0
            continue
        data = line.strip().split(DELIMITER)
        content = data[COLUMN - 1].decode(CODING, 'ignore').encode("utf-8")
        word = re.search(FILTER_WORDS, content)
        re_line = ""
        content1 = ""
        if word != None:
            range = word.span()
            content1 = content
            content = content[:range[0]]
            content1 = content1[range[0]:]
            FilteredWriter.write(content1 + "\n")
            data[COLUMN - 1] = content.decode("utf-8").encode("gbk")
            re_line = ",".join(data)
        else:
            re_line = line
        ResultWriter.write(re_line.strip() + "\n")
    print "end"
    ResultWriter.close()
    FilteredWriter.close
    reader.close();
