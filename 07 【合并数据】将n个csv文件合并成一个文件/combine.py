#!/usr/bin/python
# coding=utf-8
import sys

# 功能说明：将两个文件合并
###############参数说明############

FILE_NAME1 = "sample_min_test.csv"  # 要合并的文件
FILE_NAME2 = "sample_min_test.csv"  # 要合并的文件
RESULT_NAME = "result.csv"  # 合并后的文件

###################################
if __name__ == "__main__":
    file1 = open(FILE_NAME1, "rb")
    file2 = open(FILE_NAME2, "rb")
    result = file(RESULT_NAME, "w+")

    for line in file1:  # 将file1文件复制到result文件中
        line = line.strip() + "\n"
        result.write(line)

    next(file2) # 忽略file2文件的抬头

    for line in file2:  # 将file2文件复制到result文件中
        line = line.strip() + "\n"
        result.write(line)

    file1.close()
    file2.close()
    result.close()
