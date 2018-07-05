#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-04-08
# @Author  : Leslie (yangfei@hudongpai.com)
# @Link    : http://www.datastory.com.cn
# @Version : $0.1$

#功能介绍：两批id的重合计算

import sys
import os
import codecs

SET1_FILENAME = "japan fans.txt"
SET2_FILENAME = "Japan.txt"

SET1_DIFF_FILENAME = "_diff.txt"
SET2_DIFF_FILENAME = "_diff.txt"


set1 = set()
set2 = set()

def id_set(file_name, code = "utf8"):
    s = set()
    with codecs.open(file_name, "rb", code, 'ignore') as reader:
        #next(reader)
        for line in reader:
            data = line.strip().split("\t")
            if len(data) < 1:
                continue
            if data[0].strip() == "":
                continue
            s.add(data[0])
    return s
    
set1 = id_set(SET1_FILENAME, "gbk")
set2 = id_set(SET2_FILENAME, "gbk")
#set2 = id_set(SET2_FILENAME, "UTF-16LE")
# print set1.pop()
# print set1.pop()
# print set1.pop()
# # print set1.pop()
# print set2.pop()
# print set2.pop()
# print set2.pop()
# # print set2.pop()
# print set2.pop()
# print set2.pop()
# print set2.pop().replace(" ", "")
# print set2.pop()
# print set2.pop()


ss = set1 &set2
setDiff1 = set1 - ss;
setDiff2 = set2 - ss;
#print ss
filename = str(len(ss)) + ".txt"
#print filename

f = file(filename, 'wb+')

for id in ss:
    f.write(id + "\n")

nameForm1 = SET1_FILENAME.strip().split(".")
nameForm2 = SET2_FILENAME.strip().split(".")

Set1DiffWriter = file(nameForm1[0] + SET1_DIFF_FILENAME, "w+")
Set2DiffWriter = file(nameForm2[0] + SET2_DIFF_FILENAME, "w+")

for id in setDiff1:
    Set1DiffWriter.write(id + "\n")

for id in setDiff2:
    Set2DiffWriter.write(id + "\n")


