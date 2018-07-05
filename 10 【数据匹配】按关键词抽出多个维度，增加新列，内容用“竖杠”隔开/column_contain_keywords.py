#!/usr/bin/python
# coding=utf-8

import sys
import chardet

# 功能：
# 按关键词抽出多个维度，增加新列,最多三个维度，关键词之间用\t分隔

####################以下是参数######################

COLUMN = 37  # 要清洗的数据在第几列
FILE_NAME = "sample_min_test.csv"  # 数据文件，必须是立方导出的数据
CLASS_FILE = "sick.txt"  # 分类文件
COLUMN_TOTAL = 42  # 总列数
OUTPUT_FILE = "result.csv"  # 输出结果文件名
####################以上是参数######################
DELIMITER = ","
CODING = "gbk"
one_dimension = {}
two_dimension = {}
keywords_set = set()
flag = 0
hflag = 0
type = 0
if __name__ == "__main__":
    ResultWriter = file(OUTPUT_FILE, "w+")
    reader = open(FILE_NAME, 'rb')
    with open(CLASS_FILE, "rb") as f:
        for i in f:
            if flag == 0:
                header = i.strip().decode('utf-8').encode('gbk', 'ignore').split("\t")
                flag = 1
                continue
            words = i.strip().split("\t")
            if len(words) < 3:
                continue
            one, two, keyword = words
            keywords_set.add(keyword)
            one_dimension[keyword] = one
            two_dimension[keyword] = two

    for line in reader:
        data = line.strip().split(DELIMITER)
        if data < COLUMN_TOTAL:
            continue
        content = data[COLUMN - 1].decode(CODING).encode("utf-8")
        matched_set = set()
        for word in keywords_set:
            if word in content:
                matched_set.add(word)

        keys = ""
        one = ""
        two = ""

        for word in matched_set:
            if len(keys) == 0:
                keys = keys + word
                one = one + one_dimension.get(word)
                two = two + two_dimension.get(word)
            else:
                keys = keys + "|" + word
                one = one + "|" + one_dimension.get(word)
                two = two + "|" + two_dimension.get(word)
                type = 1

        if hflag == 0:
            if type == 0:
                h_content = DELIMITER + header[0] + DELIMITER + header[1] + DELIMITER + header[2]
            else:
                h_content = DELIMITER + header[0] + "|" + header[1] + "|" + header[2]
            ResultWriter.write(line.strip() + h_content + "\n")
            hflag = 1
            continue
        more = DELIMITER + keys + DELIMITER + two + DELIMITER + one
        ResultWriter.write(line.strip() + more.decode("utf-8").encode(CODING) + "\n")

    ResultWriter.close()
    reader.close()
