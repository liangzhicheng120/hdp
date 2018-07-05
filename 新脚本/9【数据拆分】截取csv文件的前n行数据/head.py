#!/usr/bin/python
# -*- coding=utf-8 -*-
# -*- author=liangzhicheng -*-
import sys
import util as u
import os
import re

'''
功能说明:
取文件的前几行
'''
####################以下是参数######################
LINE_NUM = 300  # 行数
####################以上是参数######################

FILE_NAME, FILE_PATH = u.getFirstFile('csv')

if __name__ == "__main__":

    try:
        RESULT_FILE = u.changeFileName(FILE_NAME, '-' + str(LINE_NUM) + '.csv')
        ResultWriter = file(u.utf8_2_gbk(RESULT_FILE), "w+")
        reader = open(u.utf8_2_gbk(FILE_PATH), 'rb')
        count = 0
        for line in reader:
            count = count + 1
            if count > LINE_NUM:
                break
            ResultWriter.write(line.strip() + '\n')
        ResultWriter.close()
        reader.close()
    except:
        traceback.print_exc()
        print '=============================================================='
        print u.utf8_2_gbk('运行出错')
        print u.utf8_2_gbk('常见错误')
        print u.utf8_2_gbk('IndexError: list index out of range')
        print u.utf8_2_gbk('匹配列选择错误或source文件夹为空或label文件夹为空')
        print '=============================================================='
        raw_input('Press Enter to exit...')
