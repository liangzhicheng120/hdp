#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-01-05 10:33:38
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import sys
import xlwt
import xlrd
reload(sys)
sys.setdefaultencoding('utf-8')

def getTableContent(path, sheetsName):
	data = xlrd.open_workbook(path)
	lines = []
	for sheetName in sheetsName:
		try:
			sheet = data.sheet_by_name(sheetName)
			for lineNum in xrange(0, sheet.nrows):
				lines.append(sheet.row_values(lineNum))
		except Exception as e:
			print "[WARN]\t%s 文件不存在 %s 表" % (path, sheetName)
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
		cols = map(lambda x:str(x).replace('\n', '').replace('\r', ''), rows[r])
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
		val = unicode(val,"gb2312")
		param[key].append(val)
	return param

HELP_MAP = u'''该脚本用于将多个文件的多个sheet合并成一个大文件。
脚本将会将合并的结果存于根文件夹下名为out.xlxs的文件中。
待提供参数如下：
	-r 根文件夹，即包含所有待合并excel的文件夹路径
	-s 每个excel中要合并的sheet的名称，若一个文件中有多个sheet要合并，可提供多个-s
'''

if __name__ == "__main__":
	try:
		PARAM = getParam(sys.argv[1:])
	except Exception as e:
		print HELP_MAP
		exit(0)
	if "h" in PARAM.keys() or "H" in PARAM.keys() or "r" not in PARAM.keys() or "s" not in PARAM.keys():
		print HELP_MAP
		exit(0)
	sheetsName = PARAM["s"]
	baseDir = PARAM["r"][0]
	print u"[INFO]\t待处理根路径为: %s" % baseDir
	# book = xlwt.Workbook()
	# sheet = book.add_sheet('Sheet 1')
	# start = 0
	for root, dirs, files in os.walk(baseDir):
		for i in xrange(0, len(files)):
			path = os.path.join(root, files[i])
			print u"[INFO]\t正在处理第 %s 个文件，该文件路径为 %s" % (i + 1, path)
			rows = getTableContent(path, sheetsName)
			appendRowsIntoTxt(rows, os.path.join(baseDir, 'out.txt'))
			# appendRowsIntoSheet(rows, start, sheet)
			# start += len(rows)
	# book.save(os.path.join(baseDir, "out.xlsx"))
	print '[INFO]\t合并完成，储存路径为 %s' % os.path.join(baseDir, "out.txt")
	# writeRowsInto(u"E:\peiling0105\\test_out.xls", getTableContent(u"E:\peiling0105\\test.xlsx"))
