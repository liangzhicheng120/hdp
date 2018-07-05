#!/usr/bin/python
# coding=utf-8
import sys
import chardet
import codecs

# 功能介绍：
# 把从立方下载的文件，转码为utf-8

####################以下是参数######################

FILE_NAME = "sample_min_test.csv"  # 数据文件，必须是立方导出的数据
OUTPUT_FILE = "result.csv"  # 输出结果文件名

####################以上是参数######################

if __name__ == "__main__":
    reader = open(FILE_NAME, "r")
    result = file(OUTPUT_FILE, "w")
    result.write(codecs.BOM_UTF8) 
    for line in reader:
        line = line.strip() + "\n"
        result.write(line.decode("gbk").encode("utf-8"))
    reader.close()
    result.close()
