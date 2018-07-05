#!/usr/bin/python
# coding=utf-8

import sys

# 功能说明：
# 先group by某一列，再对某一列进行去重,检查是否唯一
#
####################以下是参数######################

GROUP_BY_COLUMN = 12  # 对哪一列 group by
UNIQUE_COLUMN = 33  # 根据哪一列去重
FILE_NAME = "sample_min_test.csv"  # 数据文件，必须是立方导出的数据
COLUMN_TOTAL = 42  # 总列数
OUTPUT_FILE = "result.txt"  # 输出结果文件名

####################以上是参数######################
DELIMITER = ","
CODING = "gbk"
result = dict()
flag = 0

if __name__ == "__main__":
    ResultWriter = file(OUTPUT_FILE, "w+")
    reader = open(FILE_NAME, 'rb')

    for line in reader:
        data = line.strip().split(DELIMITER)
        if data < COLUMN_TOTAL:
            continue
        # groupby列数据
        group = data[GROUP_BY_COLUMN - 1]

        # 去重列数据
        uniq = data[UNIQUE_COLUMN - 1]

        if flag == 0:
            header = group
            flag = 1
            ResultWriter.write(header + "\t" + uniq + "\n")
            continue

        # 若groupby列无数据，则结束本次循环
        if len(group) == 0:
            continue
        # 若元祖中不含groupby列数据，则写入result字典中（元祖中的元素唯一）
        if result.get(group, None) is None:
            result[group] = set()

        result[group].add(uniq)
    # 遍历 字典里的所有元素
    for key, value in result.items():
        to_write = key + "\t" + str(len(value))
        ResultWriter.write(to_write + "\n")

    ResultWriter.close()
    reader.close()
