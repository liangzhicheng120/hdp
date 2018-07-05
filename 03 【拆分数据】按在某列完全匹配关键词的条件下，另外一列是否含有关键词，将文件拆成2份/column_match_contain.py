#!/usr/bin/python
# coding=utf-8

import sys

# 功能说明：
# 按在某列完全匹配关键词的条件下，另外一列是否含有关键词，将文件拆成2份
####################以下是参数######################

MAIN_COLUMN = 42  # 分类数据在第几列
KEY_WORDS = "感冒"  # 分类关键词
FOLLOW_COLUMN = 37  # 要清洗的数据在第几列
FILTER_WORDS = "filter_words.txt"  # 过滤词文件
COLUMN_TOTAL = 42  # 总列数
FILE_NAME = "sample_min_test.csv"  # 数据文件，必须是立方导出的数据
OUTPUT_FILE = "result.csv"  # 输出结果文件名(不含关键词)
REMOVE_FILE = "removed.csv"  # 被过滤的数据数据文件名（含关键词）

####################以上是参数######################
DELIMITER = ","
CODING = "gbk"
filter_words = []
flag = 0


# 将utf-8字符转换为gbk编码
def changeUtfToGbk(char):
    char = char.decode("utf-8").encode("gbk", "ignore")
    return char


if __name__ == "__main__":
    ResultWriter = file(OUTPUT_FILE, "w+")
    FilteredWriter = file(REMOVE_FILE, "w+")
    reader = open(FILE_NAME, 'rb')
    data_file = open(FILTER_WORDS, "rb")
    # 读取并保存过滤关键词
    for word in data_file:
        word = word.strip().decode('utf-8').encode('gbk', 'ignore')
        if word is not None and word != "":
            filter_words.append(word)
            # print filter_words[0]

    for line in reader:
        # 保存标题
        if flag == 0:
            flag = 1
            ResultWriter.write(line.strip() + "\n")
            FilteredWriter.write(line.strip() + "\n")
            continue
        data = line.strip().split(DELIMITER)
        # 出现乱行则舍弃
        if data < COLUMN_TOTAL:
            continue
        # 分类数据所在列数
        clazz = data[MAIN_COLUMN - 1]
        # 要清洗的数据所在列
        content = data[FOLLOW_COLUMN - 1]
        print content
        removed = False
        # 若分类数据所在列与分类关键词匹配，且在要清洗的数据所在列，则输出removed.csv
        if clazz == changeUtfToGbk(KEY_WORDS):
            for word in filter_words:
                if word in content:
                    FilteredWriter.write(line.strip() + "\n")
                    removed = True
                    break
        # 不符合规则的则输出到result.csv
        if not removed:
            ResultWriter.write(line.strip() + "\n")

    FilteredWriter.close()
    ResultWriter.close()
    reader.close()
