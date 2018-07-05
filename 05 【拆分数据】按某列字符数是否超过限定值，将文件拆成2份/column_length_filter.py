#!/usr/bin/python
# coding=utf-8

import sys

# 功能说明：
# 按某列字符数是否超过限定值，将文件拆成2份

####################以下是参数######################

COLUMN = 37  # 要清洗的数据在第几列
FILE_NAME = "sample_min_test.csv"  # 数据文件，必须是立方导出的数据
COLUMN_TOTAL = 45  # 总列数
MAX_LENGTH = 100  # 指定长度
OUTPUT_FILE = "result.csv"  # 小于100的数据文件名
REMOVE_FILE = "removed.csv"  # 大于100的数据文件名

####################以上是参数######################
DELIMITER = ","
CODING = "gbk"
flag = 0

if __name__ == "__main__":
    ResultWriter = file(OUTPUT_FILE, "w+")
    FilteredWriter = file(REMOVE_FILE, "w+")
    reader = open(FILE_NAME, 'rb')
    for line in reader:
        # 保存文件头
        if flag == 0:
            header = line
            flag = 1
            ResultWriter.write(header.strip() + "\n")
            FilteredWriter.write(header.strip() + "\n")
            continue
        data = line.strip().split(DELIMITER)
        # 发生乱行，则结束本次循环
        if data < COLUMN_TOTAL:
            continue
        # 指定列
        content = data[COLUMN - 1]

        # content列超过100字符的写入removed文件
        if len(content) > MAX_LENGTH + 1:
            FilteredWriter.write(line.strip() + "\n")
        # content列超过100字符的写入result文件
        else:
            ResultWriter.write(line.strip() + "\n")

    FilteredWriter.close()
    ResultWriter.close()
    reader.close()
