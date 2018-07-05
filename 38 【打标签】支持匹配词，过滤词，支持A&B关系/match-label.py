#!/bin/bash
# coding=utf-8
import re
import sys
import os
import util as u
import linecache

'''
标签词和关键词用'\t'隔开,多关键词用','隔开,匹配词和过滤词用'|'隔开
数据源文件为csv,gbk编码
标签词文件为txt,gbk编码
'''
###########################参数说明##################
LABEL_FILE = '功效.txt'
SOURCE_FILE = '酵素数据源.csv'
COLUNM = 22
#####################################################

keyWordCount = {}
count = 0


def createMoreMatch(fileName):
    typeCount = {}
    count = 0
    f = open(u.utf8_2_gbk(fileName), 'rb')
    for line in f:
        if line[:-1].strip():
            content = line.strip().split('\t')
            typeCount[content[0]] = typeCount.get(content[0], '') + ',' + content[1]
    for key, value in typeCount.items():
        typeCount[key] = value[1:].lower()
        count += 1
    return [typeCount, count]


def createPattern(str):
    result = '.*' + str.replace(',', '.*|.*') + '.*'
    return result


def createContent(fileName, rows):
    result = []
    count = 0
    f = open(u.utf8_2_gbk(fileName), 'rb')
    f.next()
    for line in f:
        count += 1
        result.append(u.create_content(line, rows).lower() + ',' + '\n')
    f.close()
    return [result, count]


if __name__ == '__main__':

    source_file_body, totalRows = createContent(SOURCE_FILE, COLUNM)
    labelType, labelNum = createMoreMatch(LABEL_FILE)
    matchHead = u.utf8_2_gbk('内容' + ',' + LABEL_FILE.split('.')[0] + '\n')

    print u.utf8_2_gbk('标签个数:' + str(labelNum) + '个')

    for key, value in labelType.items():
        count += 1
        print u.utf8_2_gbk('当前执行到第' + str(count) + '个')
        words = value.strip().split('|')
        if len(words) == 1:
            c = createPattern(words[0])
            p = re.compile(c)
            for num, line in enumerate(source_file_body):
                if p.match(line):
                    source_file_body[num] = source_file_body[num].strip() + key + '|' + '\n'
                    keyWordCount[key] = keyWordCount.get(key, 0) + 1
        if len(words) == 2:
            c = createPattern(words[0])
            f = createPattern(words[1])
            cp = re.compile(c)
            fp = re.compile(f)
            for num, line in enumerate(source_file_body):
                if cp.match(line) and not fp.match(line):
                    source_file_body[num] = source_file_body[num].strip() + key + '|' + '\n'
                    keyWordCount[key] = keyWordCount.get(key, 0) + 1

    u.create_result_file(u.setFileName(SOURCE_FILE, LABEL_FILE), matchHead, source_file_body)
    u.writeDictFile(u.changeFileName(LABEL_FILE, '统计.csv'), keyWordCount, 1)
