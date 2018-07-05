#!/usr/bin/python
# coding=utf-8

import sys
import os

# 功能介绍
# 对某一个字段，统计某些关键词出现的次数
# 多关键词实例：宝宝|咳嗽|女
# 单关键词实例：宝宝
####################以下是参数######################

FILE_NAME = "sample_min_test.csv"  # 数据文件
COLUMN = 37  # 要统计的数据在第几列
COLUMN_TOTAL = 42  # 总列数
KEYWORDS = "keywords.txt"  # 关键词
OUTPUT_FILE = "result.txt"  # 输出结果文件名
DELIMITER = ","  # 分隔符
DELIMITER2 = "|"  # 过滤词间的分隔符
CODING = "gbk"  # 字符编码

####################以上是参数######################

keywords_count = dict()
final = []
flag = 0
keywords = []


# 检查关键词是否全部在内容列中
def checkout(data, content):
    count = 0
    for word in data:
        if word in content:
            count = count + 1
        else:
            break
    if len(data) == count:
        return True
    else:
        return False


if __name__ == "__main__":
    # 录入关键词文本
    keywords_file = open(KEYWORDS, "rb")
    for line in keywords_file:
        line = line.strip().decode("utf-8").encode("gbk", "ignore")
        keywords.append(line)
    # 创建输出文本
    result_file = open(OUTPUT_FILE, "w+")

    # 处理数据文本
    data_file = open(FILE_NAME, "rb")
    for line in data_file:
        # 获取指定列内容
        data = line.strip().split(DELIMITER)
        # 若该行数据超过总行数，则认为该行数据有误，舍弃
        if len(data) > COLUMN_TOTAL:
            continue
        content = data[COLUMN - 1]
        # 保存指定列标题
        if flag == 0:
            header = content + "\t" + "数目".decode("utf-8").encode("gbk", "ignore") + "\n"
            result_file.write(header)
            flag = 1
            continue

        # 读取关键词并做匹配
        for word in keywords:
            data = word.strip().split(DELIMITER2)
            print word
            # 处理关键词大于1的文本
            if len(data) > 1:
                if checkout(data, content):
                    keywords_count[word] = keywords_count.get(word, 0) + 1
                else:
                    keywords_count[word] = keywords_count.get(word, 0) + 0
            # 处理关键词等于1的文本或文本无关键词的内容
            else:
                if checkout(data, content):
                    keywords_count[word] = keywords_count.get(word, 0) + 1
                else:
                    keywords_count[word] = keywords_count.get(word, 0) + 0
    # 输出统计结果
    for key, value in keywords_count.items():
        out = "{0}\t{1}\n".format(key, value)
        result_file.write(out)

    # 关闭打开的文件
    result_file.close()
    data_file.close()
    keywords_file.close()
