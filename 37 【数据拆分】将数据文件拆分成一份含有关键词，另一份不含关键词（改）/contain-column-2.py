#!/bin/bash
# coding=utf-8
import re
import sys
import os
import util as u

#######################参数说明####################
SOURCE_FILE = '0726-0831 non e-com platform.csv'
MATCH_FILE = 'filter_words- non e-com platform.txt'
COLUMN = 57
##################################################

resultFile = []
removeFile = []


def getFileName(fileName, nickName):
    return fileName.split('.')[0] + nickName


def createPattern(match_words):
    pattern = ''
    cmatch_words = map(lambda line: '.*' + line.strip() + '.*', match_words[0])
    ematch_words = map(lambda line: '.*' + line.strip() + '.*', match_words[1])
    if len(ematch_words) == 0:
        pattern = '|'.join(cmatch_words)
    else:
        pattern = '|'.join(cmatch_words) + '|' + '|'.join(ematch_words)
    return pattern


if __name__ == '__main__':
    source_file_body = u.create_file_body(SOURCE_FILE)
    source_file_head = u.create_file_head(SOURCE_FILE)

    match_words = u.create_match_words(MATCH_FILE)
    pattern = createPattern(match_words)
    p = re.compile(pattern)

    for line in source_file_body:
        content = u.create_content(line, COLUMN)
        if p.match(content):
            resultFile.append(line)
        else:
            removeFile.append(line)

    resultFileName = getFileName(SOURCE_FILE, '-含关键词.csv')
    removeFileName = getFileName(SOURCE_FILE, '-不含关键词.csv')

    u.create_result_file(resultFileName, source_file_head, resultFile)
    u.create_result_file(removeFileName, source_file_head, removeFile)
