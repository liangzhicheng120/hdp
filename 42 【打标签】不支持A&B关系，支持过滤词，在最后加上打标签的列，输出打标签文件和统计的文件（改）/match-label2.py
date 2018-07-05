#!/bin/bash
# coding=utf-8
import re
import sys
import os
import util as u
import traceback

'''
标签词和关键词用'\t'隔开,多关键词用','隔开,匹配词和过滤词用'|'隔开
数据源文件为csv,gbk编码
标签词文件为txt,gbk编码
例子:
标签词 关键词|过滤关键词
水饺  水饺,云吞,馄饨,饺子|汤圆,元宵
'''
###########################参数说明##################
COLUNM = 1  # 需要匹配的列
ACCURATE = False  # 是否精确匹配
#####################################################

keyWordCount = {}
count = 0


def combinefileName(file1, file2):
    return file1.split('.')[0] + '-' + file2.split('.')[0] + '.csv'


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
    f.close()
    return [typeCount, count]


def createPattern(str, accurate):  # 添加正则匹配规则
    if accurate:
        result = '^' + str.replace(',', '$|^') + '$'
    else:
        result = '.*' + str.replace(',', '.*|.*') + '.*'
    return result


if __name__ == '__main__':

    try:
        LABEL_FILE, LABEL_PATH = u.getFirstFile('txt')
        SOURCE_FILE, SOURCE_PATH = u.getFirstFile('csv')
        print u.utf8_2_gbk('打标签文件:' + LABEL_FILE)
        print u.utf8_2_gbk('数据源文件:' + SOURCE_FILE)
        source_file_body = u.create_file_body(SOURCE_PATH)
        for num, line in enumerate(source_file_body):
            source_file_body[num] = line.strip().lower() + ',' + '\n'
        labelType, labelNum = createMoreMatch(LABEL_PATH)
        matchHead = u.create_file_head(SOURCE_PATH, 'right', [LABEL_FILE.split('.')[0]])
        print u.utf8_2_gbk('标签个数:' + str(labelNum) + '个')
        for key, value in labelType.items():
            count += 1
            print u.utf8_2_gbk('当前执行到第' + str(count) + '个')
            words = value.strip().split('|')
            if len(words) == 1:
                c = createPattern(words[0], ACCURATE)
                p = re.compile(c)
                for num, line in enumerate(source_file_body):
                    content = u.create_content(line, COLUNM)
                    if p.match(content):
                        source_file_body[num] = source_file_body[num].strip() + key + '|' + '\n'
                        keyWordCount[key] = keyWordCount.get(key, 0) + 1
            if len(words) == 2:
                c = createPattern(words[0], ACCURATE)
                f = createPattern(words[1], ACCURATE)
                cp = re.compile(c)
                fp = re.compile(f)
                for num, line in enumerate(source_file_body):
                    content = u.create_content(line, COLUNM)
                    if cp.match(content) and not fp.match(content):
                        source_file_body[num] = source_file_body[num].strip() + key + '|' + '\n'
                        keyWordCount[key] = keyWordCount.get(key, 0) + 1

        u.create_result_file(u.setFileName(SOURCE_FILE, LABEL_FILE), matchHead, source_file_body)
        u.writeDictFile(u.changeFileName(combinefileName(SOURCE_FILE, LABEL_FILE), '统计.txt'), keyWordCount, 1)
    except:
        traceback.print_exc(file=open('error.txt', 'w+'))
