#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-06-17
# @Author  : Leslie (yangfei@hudongpai.com)
# @Link    : http://www.datastory.com.cn
# @Version : $0.2$

import os
import sys
import ConfigParser

cf = ConfigParser.ConfigParser()
cf.readfp(open('param.ini'))

SECTION_PARAMS = 'params'
CODING = cf.get(SECTION_PARAMS, 'coding')
FILE_NAME = cf.get(SECTION_PARAMS, 'filename')
DELIMITER = cf.get(SECTION_PARAMS, 'delimiter')
COLUMN = int(cf.get(SECTION_PARAMS, 'column'))
OUTPUT = cf.get(SECTION_PARAMS, 'output')

print CODING, FILE_NAME, DELIMITER
writer = open(OUTPUT, "wb")

with open(FILE_NAME, "rb") as reader:
    writer.write(next(reader))
    #next(reader)
    count = 0
    for line in reader:
        count = count + 1
        data = line.decode(CODING).strip().split(DELIMITER)
        if len(data) < 14:
            continue
        attr,dim,fs,fea,sen,senti = data[COLUMN - 1: COLUMN + 5]

        if len(attr) > 0:
            #print attr, dim, fs, fea, sen, senti
            #break
            attr_spl = attr.strip().split("|")
            dim_spl = dim.strip().split("|")
            fs_spl = fs.strip().split("|")
            fea_spl = fea.strip().split("|")
            sen_spl = sen.strip().split("|")
            senti_spl = senti.strip().split("|")
            n = len(attr_spl)
            #print n
            for i in range(n):
                #print sen_spl[i]
                if sen_spl[i] == u"负面":
                    #print sen_spl[i]
                    data[COLUMN - 1] = attr_spl[i]
                    data[COLUMN] = dim_spl[i]
                    data[COLUMN + 1]= fs_spl[i]
                    data[COLUMN + 2]= fea_spl[i]
                    data[COLUMN + 3]= sen_spl[i]
                    data[COLUMN + 4]= senti_spl[i]
                    l = ','.join(data)+"\n"
                    writer.write(l.encode(CODING))
        
        
writer.close()
