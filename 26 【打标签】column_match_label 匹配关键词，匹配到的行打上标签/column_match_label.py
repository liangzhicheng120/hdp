#!/usr/bin/python
# coding=utf-8

import sys
import os

# 功能介绍
# 选中某列，匹配关键词，末列添加一列用做打标签

####################以下是参数######################

FILE_NAME = "hsfs.csv"  # 数据文件
COLUMN = 59  # 要统计的数据在第几列
COLUMN_TOTAL = 66  # 总列数
KEYWORDS = "keywords.txt"  # 关键词
OUTPUT_FILE = "result.csv"  # 输出结果文件名
LABEL = "机打情感值判断"  # 标签标题

####################以上是参数######################

DELIMITER = ","  # 分隔符
DELIMITER2 = " "  # 分隔符
CODING = "gbk"  # 字符编码
flag = 0
keywords = []
i = 0
j = 0
k = 0


# utf-8转码为gbk
def changeUtfToGbk(char):
    char = char.decode("utf-8").encode("gbk", "ignore")
    return char


if __name__ == "__main__":
    # 录入关键词文本
    keywords_file = open(KEYWORDS, "rb")
    for word in keywords_file:
        word = changeUtfToGbk(word.strip())
        keywords.append(word)

    # 创建输出文本
    result_file = open(OUTPUT_FILE, "w+")

    # 处理数据文本
    data_file = open(FILE_NAME, "rb")

    for line in data_file:
        data = line.strip().split(DELIMITER)

        # 若该行数据超过总行数，则认为该行数据有误，舍弃
        if len(data) > COLUMN_TOTAL:
            continue

        # 保存指定列标题
        if flag == 0:
            header = line.strip() + "," + changeUtfToGbk(LABEL) + "\n"
            result_file.write(header)
            flag = 1
            continue
        # 获取指定列内容
        content = data[COLUMN - 1]
        # 读取关键词并做匹配
        removed_flag = False
        for word in keywords:

            key_data = word.strip().split(DELIMITER2)
            # 循环总次数
            k = k + 1
            if key_data[0] in content:
                out = line.strip() + "," + key_data[1] + "\n"
                result_file.write(out)
                i = i + 1
                removed_flag = True
                break
        # 未匹配到的文本
        if not removed_flag:
            out = line.strip() + "\n"
            result_file.write(out)
            j = j + 1


    # 关闭打开的文件
    print "include word count:{0}".format(i)
    print "uninclude word count:{0}".format(j)
    print "total count:{0}".format(k)
    result_file.close()
    data_file.close()
    keywords_file.close()
