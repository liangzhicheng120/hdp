#!/bin/bash
# coding=utf-8
import re
import os
import sys
import util as u
import linecache

###################参数说明################
SOURCE_FILE = 'new source-new分析对象-声音来源.csv'  # 输入文件
RESULT_FILE = 'result.csv'  # 输出文件
COLUNM = 13  # 需要匹配的列
LABELWORD = '平台分类.txt'  # 匹配关键词
##########################################
i = 0
keyWordCount = {}


def writeFileList(list, fileName):
    f = file(fileName, 'w+')
    f.writelines(list)
    f.close()


if __name__ == '__main__':

    columnName = u.GetFileNameAndExt(u.utf8_2_gbk(LABELWORD))[0]
    labelWords = u.create_match_words(LABELWORD)
    labelWordp = u.build_match_label(labelWords)
    head = linecache.getline(u.utf8_2_gbk(SOURCE_FILE), 1).strip()
    TOTALCOLUNM = len(head.split(','))
    print u.utf8_2_gbk('标签词个数:') + u.printDictLen(labelWordp)

    source_file_body = u.create_file_body(SOURCE_FILE)
    for key, value in labelWordp.items():
        i += 1
        print u.utf8_2_gbk('当前执行到{0}个'.format(i))
        for num, line in enumerate(source_file_body):
            data = line.strip().split(',')
            if len(data) == TOTALCOLUNM + 1:
                continue
            content = data[COLUNM - 1]
            p = re.compile(value)
            if p.match(content):
                source_file_body[num] = source_file_body[num].strip() + ',' + key + '\n'
                keyWordCount[key] = keyWordCount.get(key, 0) + 1

    # 补全格式
    for num, line in enumerate(source_file_body):
        data = line.strip().split(',')
        if len(data) == TOTALCOLUNM + 1:
            continue
        source_file_body[num] = source_file_body[num].strip() + ',' + '' + '\n'

    result_file_head = u.create_file_head(SOURCE_FILE, 'right', [u.gbk_2_utf8(columnName)])
    u.create_result_file(RESULT_FILE, result_file_head, source_file_body)

    KEYWORD_FILE = LABELWORD.split('.')[0] + '统计.txt'
    u.writeDictFile(KEYWORD_FILE, keyWordCount)  # 输出统计结果
