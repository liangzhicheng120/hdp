#!/usr/bin/python
# coding=utf-8

import sys

# 功能说明：
# 选择任意多列数据，将选择的列拆分出来


####################以下是参数######################

COLUMN = [8, 13, 15, 23, 33]  # 要提取的数据在第几列
FILE_NAME = "sample_min_test.csv"  # 数据文件，必须是立方导出的数据
COLUMN_TOTAL = 42  # 总列数
OUTPUT_FILE = "result.csv"  # 输出结果文件名

####################以上是参数######################
DELIMITER = ","
if __name__ == "__main__":
    ResultWriter = file(OUTPUT_FILE, "w+")
    with open(FILE_NAME, "rb") as f:
        for line in f:
            fields = line.strip().split(DELIMITER)
            for index in COLUMN:
                ResultWriter.write(fields[index - 1] + DELIMITER)
            ResultWriter.write("\n")
    ResultWriter.close()
