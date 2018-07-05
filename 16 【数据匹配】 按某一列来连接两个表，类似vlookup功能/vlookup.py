#!/usr/bin/python
# coding=utf-8

import sys
import re

# 功能说明：
# 按维度表匹配生成新列(类似vlookup) data1 left join data2

####################以下是参数######################

COLUMN1 = 1  # 基准列
FILE_NAME1 = "raw_id.txt"  # 基准数据文件，必须是立方导出的数据
COLUMN2 = 1  # 基准列
FILE_NAME2 = "raw_id2.txt"  # 数据文件，必须是立方导出的数据
NEW_COLUMN = [9, 13, 15]  # 新列

OUTPUT_FILE = "result.csv"  # 输出结果文件名

####################以上是参数######################
DELIMITER = ","
CODING = "gbk"

result = dict()

if __name__ == "__main__":
    ResultWriter = file(OUTPUT_FILE, "w+")
    reader1 = open(FILE_NAME1, 'rb')
    reader2 = open(FILE_NAME2, 'rb')

    # next(reader1)
    # next(reader2)

    l2 = list(reader2)

    for line1 in reader1:
        stand1 = line1.split(DELIMITER)[COLUMN1 - 1].strip().decode(CODING)

        for line2 in l2:
            insert = ""
            arr2 = line2.split(DELIMITER)
            stand2 = arr2[COLUMN2 - 1].strip().decode(CODING)
            for field in NEW_COLUMN:
                insert = insert + arr2[field - 1] + ","
            insert = insert.strip(",")

            if stand1 == stand2:
                ResultWriter.write(line1.strip() + "," + insert + "\n")
                break

    ResultWriter.close()
    reader1.close()
    reader2.close()
