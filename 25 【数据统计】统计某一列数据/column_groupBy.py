#!/usr/bin/python
# coding=utf-8
import sys

# 功能介绍：
# 根据某一列统计，类似sql的group by 操作

####################以下是参数######################
FILE_NAME = "sample_min_test.csv"  # 数据文件
OUTPUT_FILE = "result.txt"  # 输出结果文件名
COLUMN = 10  # 要统计的数据在第几列
DELIMITER = ","
####################以上是参数######################
CODING = "gbk"
flag = 0
time_dict = {}

if __name__ == "__main__":
    ResultWriter = file(OUTPUT_FILE, "w+")
    reader = open(FILE_NAME, 'rb')

    for line in reader:
        # 保存列的标题
        if flag == 0:
            header = line.split(DELIMITER)
            flag = 1
            ResultWriter.write(header[COLUMN - 1].strip() + "\n")
            continue
        data = line.strip().split(DELIMITER)
        # 将需要统计的列保存在元祖中
        key = data[COLUMN - 1]
        # 统计指定列相同内容的数目,若字典不含有这个值，则更新字典
        if key in time_dict:
            time_dict[key] = time_dict[key] + 1
        # 若字典含有这个键值，则字典中该键值保持不变
        else:
            time_dict[key] = 1
    # 遍历输出字典中的所有项
    for key, value in time_dict.items():
        ResultWriter.write(str(key) + '\t' + str(value) + '\n')

    ResultWriter.close()
    reader.close()
