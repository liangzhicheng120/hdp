#!/usr/bin/python
# coding=utf-8

import sys
import re
import util as u
import traceback
'''
功能说明：
统计内容中含有“@…… ”或者“[……]”、“#……#”特殊格式的内容和数量
数据文件放在source文件夹,数据文件为csv,gbk编码
'''

####################以下是参数######################
COLUMN = 37  # 要清洗的数据在第几列
PATTERNTYPE = 3  # 选择匹配规则patternTemp1，patternTemp2，patternTemp3

####################以上是参数######################

patternTemp1 = "@[^,，：:\s@()/]+"
patternTemp2 = "\[.*?\]"
patternTemp3 = "#.*?#"

DELIMITER = ","
CODING = "gbk"
SOURCE, SOURCEPATH = u.getFirstFile('csv')
COUNT_FILE = u.changeFileName(SOURCE, '-总数统计.txt')
OUTPUT_FILE = u.changeFileName(SOURCE, '-统计.csv')

i = 0
j = 0
result = dict()


def utf8_2_gbk(src):
    res = src.decode("utf-8").encode("gbk", "ignore")
    return res


if __name__ == "__main__":

    try:
        ResultWriter = file(u.utf8_2_gbk(OUTPUT_FILE), "w+")
        reader = open(u.utf8_2_gbk(SOURCEPATH), 'rb')
        count_file = file(u.utf8_2_gbk(COUNT_FILE), "w+")
        print u.utf8_2_gbk('开始执行')
        next(reader)

        for line in reader:
            content = line.split(DELIMITER)[COLUMN - 1].strip().decode(CODING, 'ignore')
            if PATTERNTYPE == 1:
                pattern = re.compile(r'' + patternTemp1)
            elif PATTERNTYPE == 2:
                pattern = re.compile(r'' + patternTemp2)
            elif PATTERNTYPE == 3:
                pattern = re.compile(r'' + patternTemp3)
            matches = pattern.findall(content)
            if len(matches) != 0:
                for ele in matches:
                    if ele in result:
                        result[ele] = result[ele] + 1
                        i = i + 1
                    else:
                        result[ele] = 1
                        j = j + 1
        # 排序
        result = sorted(result.iteritems(), key=lambda asd: asd[1], reverse=True)
        for key, value in result:
            out = str(key.encode(CODING)) + "," + str(value) + "\n"
            ResultWriter.write(out)

        # 输出统计结果
        count_file.write(utf8_2_gbk("统计结果:") + str(i + j))
        print u.utf8_2_gbk('总数统计:' + str(i + j))
        print u.utf8_2_gbk('执行完毕')
        ResultWriter.close()
        reader.close()
        count_file.close()
    except:
        traceback.print_exc()
        print '=============================================================='
        print u.utf8_2_gbk('运行出错')
        print u.utf8_2_gbk('常见错误')
        print u.utf8_2_gbk('IndexError: list index out of range')
        print u.utf8_2_gbk('匹配列选择错误或source文件夹为空或label文件夹为空')
        print '=============================================================='
        raw_input('Press Enter to exit...')
