#!/bin/bash
# coding=utf-8
import re
import sys
import os
import util as u
import traceback
import itertools

'''
标签词文件放在label文件夹,数据源放在source文件夹

标签词和关键词用'\t'隔开,关键词用','隔开,支持A&B关系的关键词（不限个数）,用'&'隔开,匹配词和过滤词用'|'隔开
数据源文件为csv,gbk编码
标签词文件为txt,gbk或utf-8编码

例子:
标签词 关键词|过滤关键词
水饺  水饺1&水饺2,云吞,馄饨,饺子|汤圆,元宵1&元宵2&元宵3

注意:
A&B关键词不支持'支付宝'$'支付'这种类型的关键词
带过滤词的写法:过滤词放在最后
资金往来	转账
资金往来	亲情账户
资金往来	亲密付
资金往来	零钱
资金往来	话费卡转让
资金往来	红包
资金往来	支付宝&口令
资金往来	付款
资金往来	买东西
资金往来	埋单
资金往来	给钱
资金往来	付钱
资金往来	AA收款
资金往来	微信&支付|支付宝
或者
资金往来	转账,亲情账户,亲密付,零钱,话费卡转让,红包,支付宝&口令,口令&支付宝,付款,买东西,埋单,给钱,付钱,aa收款,微信&支付,支付&微信|支付宝
'''

###########################参数说明##################
COLUNM = 22  # 需要匹配的列
ACCURATE = False  # 是否精确匹配
#####################################################


def combinefileName(file1, file2):
    return file1.split('.')[0] + '-' + file2.split('.')[0] + '.csv'


def changeStr(k):  # 构造A&B关系词
    if '&' in k:
        newstr = ''
        strList = k.strip().split('&')
        sLen = len(strList)
        for line in list(itertools.permutations(k.split('&'), sLen)):
            newstr += ',' + '&'.join(line)
        return k.replace(k, newstr[1:])
    else:
        return k


def createMoreMatch(fileName):  # 构造匹配关键词
    typeCount = {}
    count = 0
    File = open(u.utf8_2_gbk(fileName), 'rb')
    for line in File:
        if line[:-1].strip():
            try:
                content = u.utf8_2_gbk(line).strip().split('\t')
            except:
                content = line.strip().split('\t')

            typeCount[content[0]] = typeCount.get(content[0], '') + ',' + content[1]
    for key, value in typeCount.items():
        count += 1
        c = value[1:].split('|')
        if len(c) == 2:
            k = c[0].split(',')
            f = c[1].split(',')
            newk = map(changeStr, k)
            newf = map(changeStr, f)
            typeCount[key] = ','.join(newk) + '|' + ','.join(newf)
        if len(c) == 1:
            k = c[0].split(',')
            newk = map(changeStr, k)
            typeCount[key] = ','.join(newk)
    File.close()
    # u.writeDictFile('match.txt', typeCount, 0)  # 将匹配词输出到文件
    return [typeCount, count]


def createPattern(str, accurate):  # 添加正则匹配规则
    if ACCURATE:
        result = '^' + str.replace(',', '$|^').replace('&', '$|^') + '$'
    else:
        result = '.*' + str.replace(',', '.*|.*').replace('&', '.*') + '.*'
    return result


if __name__ == '__main__':
    try:
        keyWordCount = {}
        count = 0
        LABEL_FILE, LABEL_PATH = u.getFirstFile('txt')
        SOURCE_FILE, SOURCE_PATH = u.getFirstFile('csv')
        print u.utf8_2_gbk('打标签文件:' + LABEL_FILE)
        print u.utf8_2_gbk('数据源文件:' + SOURCE_FILE)
        print u.utf8_2_gbk('是否精确匹配' + str(ACCURATE))
        source_file_body = u.create_file_body(SOURCE_PATH)
        print len(source_file_body)
        for num, line in enumerate(source_file_body):
            source_file_body[num] = line.strip() + ',' + '\n'
        labelType, labelNum = createMoreMatch(LABEL_PATH)
        matchHead = u.create_file_head(SOURCE_PATH, 'right', [LABEL_FILE.split('.')[0]])
        print u.utf8_2_gbk('标签个数:' + str(labelNum) + '个')
        for key, value in labelType.items():
            count += 1
            print u.utf8_2_gbk('当前执行到第' + str(count) + '个')
            words = value.strip().split('|')
            if len(words) == 1:  # 只有关键词无过滤词
                c = createPattern(words[0], ACCURATE)
                p = re.compile(c, re.I)
                for num, line in enumerate(source_file_body):
                    content = u.create_content(line, COLUNM)
                    if p.match(content):
                        source_file_body[num] = source_file_body[num].strip() + key + '|' + '\n'
                        keyWordCount[key] = keyWordCount.get(key, 0) + 1

            if len(words) == 2:  # 有关键词和过滤词
                c = createPattern(words[0], ACCURATE)
                f = createPattern(words[1], ACCURATE)
                cp = re.compile(c, re.I)
                fp = re.compile(f, re.I)
                for num, line in enumerate(source_file_body):
                    content = u.create_content(line, COLUNM)
                    if cp.match(content) and not fp.match(content):
                        source_file_body[num] = source_file_body[num].strip() + key + '|' + '\n'
                        keyWordCount[key] = keyWordCount.get(key, 0) + 1
        # 输出结果文件
        u.create_result_file(u.setFileName(SOURCE_FILE, LABEL_FILE), matchHead, source_file_body)
        u.writeDictFile(u.changeFileName(combinefileName(SOURCE_FILE, LABEL_FILE), '统计.txt'), keyWordCount, 1)
    except:
        traceback.print_exc()
        print '=============================================================='
        print u.utf8_2_gbk('运行出错')
        print u.utf8_2_gbk('常见错误')
        print u.utf8_2_gbk('IndexError: list index out of range')
        print u.utf8_2_gbk('匹配列选择错误或source文件夹为空或label文件夹为空')
        print '=============================================================='
        raw_input('Press Enter to exit...')
