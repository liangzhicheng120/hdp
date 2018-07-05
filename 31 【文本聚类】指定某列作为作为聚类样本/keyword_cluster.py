#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import re
import jieba.analyse
import util as u

####################参数说明###################

SOURCE_FILE = "test.csv"  # 输入文件
RESULT_FILE = "test聚类.csv"  # 输出文件
TOPKET = 3  # 抽取作为唯一某类标示符的词个数(建议设置3-4)
COLUMN = 2  # 要聚类的内容所在列
COUNT_FILE = "聚类种类.txt"  # 每种种类的统计文件

##############################################

"""
读取原始文件，抽取每段话的关键词，将关键词排序后最后这段话的key
将相同key的段落判断为一个cluster
将结果按照每个cluster的大小排序，大的在前面
性能:
行数----1000----10000----100000----1000000--
耗时-----2s------11s------129s------1432s---
内存----0.3mb----3mb------33mb------400mb---
"""
__author__ = "liangzhicheng"

cluster = {}
result_file_body = []
pattern = re.compile("\w|[/.,/#@$%^& ]")
count_file_list = []

if __name__ == '__main__':

    source_file_head = u.create_file_head(SOURCE_FILE, 'left', ['类型'])
    source_file_body = u.create_file_body(SOURCE_FILE)

    for num, line in enumerate(source_file_body):
        content = re.sub(pattern, '', u.create_content(line, COLUMN))
        if len(content) <= 20:
            keywords = jieba.analyse.extract_tags(content, topK=2)
        else:
            keywords = jieba.analyse.extract_tags(content, topK=TOPKET)
        keywords.sort()
        key = ','.join(keywords)
        cluster[key] = str(cluster.get(key, 0)) + "," + str(num + 1)

    for num, value in enumerate(cluster.itervalues()):
        cluster_list = value[2:].split(',')
        count_file_list.append(str(num) + '\t' + str(len(cluster_list)) + '\n')
        for n in cluster_list:
            result_file_body.append(str(num) + ',' + source_file_body[int(n) - 1])

    u.create_result_file(RESULT_FILE, source_file_head, result_file_body)
    u.create_result_file(COUNT_FILE, ['type\tcount\n'], count_file_list)
