#!/bin/bash
# -*- coding=utf-8 -*-
# -*- author=liangzhicheng -*-
import re
import os
import sys
import util as u
import linecache
import traceback

########################参数说明#######################
COUNT = 10  # 要切分的列数
######################################################

FILE_NAME, FILE_PATH = u.getFirstFile('csv')


def create_file(fileName):
    fileList = linecache.getlines(u.utf8_2_gbk(fileName))
    fileHead = fileList[0]
    fileBody = fileList[1:]
    fileBLen = len(fileBody)
    return [fileHead, fileBody, fileBLen]


if __name__ == '__main__':
    try:
        fileHead, fileBody, fileBLen = create_file(FILE_PATH)
        middle = (fileBLen / COUNT) + 1
        for num in range(COUNT):
            left = num * middle
            right = (num + 1) * middle
            u.create_result_file(u.changeFileName(FILE_NAME, '-' + str(num) + '.csv'), fileHead,
                                 fileBody[left:right])
    except:
        traceback.print_exc()
        print '=============================================================='
        print u.utf8_2_gbk('运行出错')
        print u.utf8_2_gbk('常见错误')
        print u.utf8_2_gbk('IndexError: list index out of range')
        print u.utf8_2_gbk('匹配列选择错误或source文件夹为空或label文件夹为空')
        print '=============================================================='
        raw_input('Press Enter to exit...')
