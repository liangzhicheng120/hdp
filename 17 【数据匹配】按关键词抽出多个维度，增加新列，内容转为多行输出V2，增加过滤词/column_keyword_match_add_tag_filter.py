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
DELIMITER2 = "\t"  # 列间间隔
DELIMITER3 = "|"  # 过滤关键词间隔
keyword_delimiter = " "
CODING = "gbk"
patternTemp = "(?=.*{0})"
match_words = dict()
filter_words = []


def utf8_2_gbk(src):
    res = src.decode("utf-8").encode("gbk", "ignore")
    return res


def builder(sign, src):
    res = sign + src.encode("gbk", "ignore")
    return res


def builder_data(src):
    res = builder(DELIMITER, add[0]) + builder(DELIMITER, add[1]) + builder(DELIMITER, add[2]) + "\n"
    return res


def builder_header(src):
    res = DELIMITER + header[0] + DELIMITER + header[1] + DELIMITER + header[2] + "\n"
    return res


if __name__ == "__main__":
    ResultWriter = file(OUTPUT_FILE, "w+")  # 输出文件名
    reader = open(FILE_NAME, 'rb')  # 数据文件名

    add_head = ""

    with open(FILTER_WORDS, "rb") as f:
        add_head = utf8_2_gbk(next(f))  # 过滤词文件标题
        header = add_head.strip().split(DELIMITER2)
        # print header[0]
        # print header[1]
        # print header[2]
        # print header[3]
        for line in f:
            words = line.decode("utf-8").strip().split(DELIMITER2)
            if len(words) < 3:
                continue
            match_words[words[2]] = line.decode("utf-8").strip()
    # (抬头）
    ResultWriter.write(next(reader).strip() + builder_header(header))

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
                if len(to_add.split(DELIMITER2)) > 3:  # 读取过滤关键词
                    filter_words = to_add.split(DELIMITER2)[3].split(DELIMITER3)
                    count = 0
                    add = to_add.split(DELIMITER2)
                    # print add[0]
                    # print add[1]
                    # print add[2]
                    # print add[3]

                    for filter_word in filter_words:
                        if filter_word not in content:
                            count = count + 1
                    if count == len(filter_words):
                        matched = True
                        out = line.strip() + builder_data(add)
                        ResultWriter.write(out)  # 输出匹配到过滤关键词的行
                else:
                    matched = True
                    # 输出未匹配到过滤关键词的行
                    out = line.strip() + builder_data(add)
                    ResultWriter.write(out)
        if not matched:
            ResultWriter.write(line.strip() + ",,,\n")

    ResultWriter.close()
    reader.close()
