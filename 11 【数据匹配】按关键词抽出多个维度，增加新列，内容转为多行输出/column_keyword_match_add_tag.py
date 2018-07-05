#!/usr/bin/python
# coding=utf-8

import sys
import re

# 功能说明：
# 关键词匹配，根据码表打标签
# 支持关键词中  用 空格表示 and的关系
# 

####################以下是参数######################

COLUMN = 37  # 要清洗的数据在第几列
FILE_NAME = "sample_min_test.csv"  # 数据文件，必须是立方导出的数据
FILTER_WORDS = "sick.txt"  # 过滤词文件
COLUMN_TOTAL = 42  # 总列数
OUTPUT_FILE = "result.csv"  # 输出结果文件名
REMOVE_FILE = "removed.csv"  # 被过滤的数据数据文件名

####################以上是参数######################
DELIMITER = ","
CODING = "gbk"
DELIMITER2 = "\t"
keyword_delimiter = " "
patternTemp = "(?=.*{0})"
match_words = dict()

if __name__ == "__main__":
    ResultWriter = file(OUTPUT_FILE, "w+")
    reader = open(FILE_NAME, 'rb')

    add_head = ""

    with open(FILTER_WORDS, "rb") as f:
        add_head = next(f).decode("utf-8")
        for line in f:
            words = line.decode("utf-8").strip().split(DELIMITER2)
            if len(words) < 3:
                continue
            match_words[words[2]] = line.decode("utf-8").strip()

    ResultWriter.write(
        next(reader).strip() + DELIMITER + add_head.encode(CODING).replace(DELIMITER2,
                                                                           DELIMITER).strip() + "\n")  # (抬头）
    for line in reader:
        data = line.strip().split(DELIMITER)
        if len(data) != COLUMN_TOTAL:
            print line
            continue
        content = data[COLUMN - 1].decode(CODING)

        matched = False

        for word, to_add in match_words.items():
            words = word.split(keyword_delimiter)
            pattrns = ['(?=.*' + w + ')' for w in words]
            pattern = re.compile(r'(' + ''.join(pattrns) + '.*)')
            if pattern.match(content):
                matched = True
                ResultWriter.write(
                    line.strip() + DELIMITER + to_add.encode(CODING).replace(DELIMITER2, DELIMITER) + "\n")
        if not matched:
            ResultWriter.write(line.strip() + ",,,\n")

    ResultWriter.close()
    reader.close()
