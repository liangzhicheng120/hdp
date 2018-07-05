#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- author: liangzhicheng -*-
import os
import sys
import xlwt
import xlrd
import traceback
reload(sys)
sys.setdefaultencoding('utf-8')
'''
功能介绍：
合并当前source目录下所有的excel文件，限定每个excel文件包含1个sheet
'''
#########################参数说明######################
baseDir = sys.path[0] + '\\source'  # 当前路径下的目录名


######################################################

def utf8_2_gbk(str):
    '''
    utf-8转gbk
    :param str: 字符串
    :return: 转码后的字符串
    '''
    result = str.decode("utf-8").encode("gbk", "ignore")
    return result


def getTableContent(path):
    wb = xlrd.open_workbook(path)
    lines = []
    try:
        sheet = wb.sheets()[0]
        print "Sheet: " + sheet.name
        for lineNum in xrange(0, sheet.nrows):
            lines.append(sheet.row_values(lineNum))
    except Exception as e:
        print "[WARN]\t%s 文件不存在 sheet" % (path)
    return lines


def appendRowsIntoSheet(rows, start, sheet):
    for r in xrange(0, len(rows)):
        cols = rows[r]
        for c in xrange(0, len(cols)):
            sheet.write(start + r, c, cols[c])
    return sheet


def appendRowsIntoTxt(rows, path):
    f = open(path, 'a')
    for r in xrange(0, len(rows)):
        cols = map(lambda x: str(x).replace('\n', '').replace('\r', ''), rows[r])
        f.write('\t'.join(cols) + "\n")
    f.close()


def getParam(args):
    param = {}
    args = " ".join(args).split("-")[1:]
    for arg in args:
        arr = arg.split(" ")
        key = arr[0].strip()
        val = arr[1].strip()
        if key not in param.keys():
            param[key] = []
        val = unicode(val, "gb2312")
        param[key].append(val)
    return param


if __name__ == "__main__":
    try:
        count = 0
        flag = False
        for root, dirs, files in os.walk(baseDir):
            for i in xrange(0, len(files)):
                path = os.path.join(root, files[i])
                print path
                if not path.endswith(".xlsx"):
                    continue
                count = count + 1
                rows = getTableContent(path)
                if count == 0:
                    print utf8_2_gbk('[INFO]\t{0}不存在xlsx文件或文件路径错误!'.format(baseDir))
                if count == 1:
                    flag = True
                    appendRowsIntoTxt(rows, os.path.join(sys.path[0], utf8_2_gbk('合并.txt')))
                else:
                    flag = True
                    appendRowsIntoTxt(rows[1:], os.path.join(sys.path[0], utf8_2_gbk('合并.txt')))
        if flag:
            print utf8_2_gbk('[INFO]\t合并完成，储存路径为') + os.path.join(sys.path[0], utf8_2_gbk("合并.txt"))
        else:
            print utf8_2_gbk('[INFO]\t{0}不存在xlsx文件或文件路径错误!'.format(baseDir))
    except:
        traceback.print_exc()
        print '=============================================================='
        print u.utf8_2_gbk('运行出错')
        print u.utf8_2_gbk('常见错误')
        print u.utf8_2_gbk('IndexError: list index out of range')
        print u.utf8_2_gbk('匹配列选择错误或source文件夹为空或label文件夹为空')
        print '=============================================================='
        raw_input('Press Enter to exit...')
