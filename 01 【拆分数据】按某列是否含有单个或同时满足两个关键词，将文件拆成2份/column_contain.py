#!/usr/bin/python
# coding=utf-8

import sys

# 功能说明：
# 按某列是否同时含有一个或多个关键词，将文件拆成2份

####################以下是参数######################

COLUMN = 37  # 要清洗的数据在第几列
FILE_NAME = "sample_min_test.csv"  # 数据文件，必须是立方导出的数据
FILTER_WORDS = "filter_words.txt"  # 过滤词文件
COLUMN_TOTAL = 42  # 总列数
OUTPUT_FILE = "result.csv"  # 输出结果文件名
REMOVE_FILE = "removed.csv"  # 被过滤的数据数据文件名

####################以上是参数######################
DELIMITER = ","
DELIMITER2 = " "  # 过滤词间的分隔符
CODING = "gbk"
filter_words = []
flag = 0

if __name__ == "__main__":
    ResultWriter = file(OUTPUT_FILE, "w+")
    FilteredWriter = file(REMOVE_FILE, "w+")
    reader = open(FILE_NAME, 'rb')
    # 读入过滤词文件，将过滤词从utf-8转码成gbk
    with open(FILTER_WORDS, "rb") as f:
        for line in f:
            word = line.strip().decode('utf-8', 'ignore').encode('gbk', 'ignore')
            print word
            if word is not None and word != "":
                filter_words.append(word)
    # 读取数据文件
    for line in reader:
        # 保存数据文件标题
        if flag == 0:
            header = line
            flag = 1
            ResultWriter.write(header.strip() + "\n")
            FilteredWriter.write(header.strip() + "\n")
            continue
        # 读取每一行，以逗号作为分隔符，返回一个列表
        data = line.strip().split(DELIMITER)
        # 如果该行超过总行数，则认为是乱行，这行数据不应处理，跳过
        if len(data) < COLUMN_TOTAL:
            print "this row is too long"
            continue
        # 要清洗的数据所在的列
        content = data[COLUMN - 1].decode(CODING).encode(CODING)
        # 设置旗帜
        removed = False
        # 读取过滤词
        for word in filter_words:
            # 若每一行有多个过滤词，根据空格将其拆分，返回一个列表
            filterArr = word.strip().split(DELIMITER2)
            count = 0
            # 处理每一个在过滤词列表中的关键词
            for fil in filterArr:
                # 如果关键词在要清洗的数据所在的列中
                if fil in content:
                    count = count + 1
                # 关键词不在要清洗的数据所在的列中，则跳出循环
                else:
                    break
            # 如果一行中一个或多个关键词都在过滤词列表中，则写入removed文件中
            if count == len(filterArr):
                FilteredWriter.write(line.strip() + "\n")
                removed = True
                break
        # 若未匹配到关键词，那么就写入result文件中
        if not removed:
            ResultWriter.write(line.strip() + "\n")

    FilteredWriter.close()
    ResultWriter.close()
    reader.close()
