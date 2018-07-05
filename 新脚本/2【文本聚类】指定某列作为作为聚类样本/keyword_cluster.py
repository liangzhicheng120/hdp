#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import re
import jieba.analyse
import util as u
import traceback

####################参数说明##############################
TOPKET = 3  # 抽取作为唯一某类标示符的词个数(建议设置3-4)
COLUMN = 2  # 要聚类的内容所在列
#########################################################

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

SOURCENAME, SOURCEPATH = u.getFirstFile('csv')
cluster = {}
result_file_body = []
pattern = re.compile("\w|[/.,/#@$%^& ]")
count_file_dict = {}

if __name__ == '__main__':

    try:
        source_file_head = u.create_file_head(SOURCEPATH, 'left', ['类型'])
        source_file_body = u.create_file_body(SOURCEPATH)
        print u.utf8_2_gbk('开始执行聚类')
        for num, line in enumerate(source_file_body):
            content = re.sub(pattern, '', u.create_content(line, COLUMN))
            if len(content) <= 20:
                keywords = jieba.analyse.extract_tags(content, topK=2)
            else:
                keywords = jieba.analyse.extract_tags(content, topK=TOPKET)
            keywords.sort()
            key = ','.join(keywords)
            cluster[key] = str(cluster.get(key, 0)) + "," + str(num + 1)
        print u.utf8_2_gbk('聚类完成,生成输出文件')
        for num, value in enumerate(cluster.itervalues()):
            cluster_list = value[2:].split(',')
            count_file_dict[num] = len(cluster_list)
            for n in cluster_list:
                result_file_body.append(str(num) + ',' + source_file_body[int(n) - 1])
        u.create_result_file(u.changeFileName(SOURCENAME, '-聚类.csv'), source_file_head, result_file_body)
        u.writeDictFile(u.changeFileName(SOURCENAME, '-聚类统计.txt'), count_file_dict, 1)
    except:
        traceback.print_exc()
        print '=============================================================='
        print u.utf8_2_gbk('运行出错')
        print u.utf8_2_gbk('常见错误')
        print u.utf8_2_gbk('IndexError: list index out of range')
        print u.utf8_2_gbk('匹配列选择错误或source文件夹为空或label文件夹为空')
        print '=============================================================='
        raw_input('Press Enter to exit...')
