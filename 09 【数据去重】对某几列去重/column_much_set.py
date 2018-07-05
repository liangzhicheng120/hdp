#!/usr/bin/python
# coding=utf-8
import sys

# 功能描述
# 根据某一列去重

####################以下是参数######################

COLUMN = [12, 42]  # 要清洗的数据在第几列
FILE_NAME = "sample_min_test.csv"  # 数据文件，必须是立方导出的数据
COLUMN_TOTAL = 42  # 总列数
OUTPUT_FILE = "result.csv"  # 输出结果文件名

####################以上是参数#### ##################
DELIMITER = ","
CODING = "gbk"
unique_set = set()
source_dict = {}

if __name__ == "__main__":
    ResultWriter = file(OUTPUT_FILE, "w+")
    reader = open(FILE_NAME, 'rb')

    for line in reader:
        data = line.strip().split(DELIMITER)
        if data < COLUMN_TOTAL:
            continue
        pid = ""
        # 将去重列保存在pid中
        for i in COLUMN:
            pid = pid + data[i - 1]
        # 若去重列内容不再元祖中，则认为不是重复，写入输出文件
        if pid not in unique_set:
            unique_set.add(pid)
            ResultWriter.write(line.strip() + "\n")

    ResultWriter.close()
    reader.close()
