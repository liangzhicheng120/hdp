#!/usr/bin/python
# coding=utf-8

import sys
import re

# 功能说明：
# 统计内容中含有“@…… ”或者“[……]”、“#……#”特殊格式的内容和数量

####################以下是参数######################

COLUMN = 1  # 要清洗的数据在第几列
FILE_NAME = "8.23-8.31.csv"  # 数据文件，必须是立方导出的数据
COLUMN_TOTAL = 1  # 总列数
PATTERNTYPE = 3  # 选择匹配规则patternTemp1，patternTemp2，patternTemp3
OUTPUT_FILE = "result.csv"  # 输出结果文件名
COUNT_FILE = "8.6-8.21t.txt"  # 统计结果文件名

####################以上是参数######################
DELIMITER = ","
CODING = "gbk"
patternTemp1 = "@[^,，：:\s@()/]+"
patternTemp2 = "\[.*?\]"
patternTemp3 = "#.*?#"

i = 0
j = 0
result = dict()


def utf8_2_gbk(src):
    res = src.decode("utf-8").encode("gbk", "ignore")
    return res


if __name__ == "__main__":
    ResultWriter = file(OUTPUT_FILE, "w+")
    reader = open(FILE_NAME, 'rb')
    count_file = file(COUNT_FILE, "w+")

    next(reader)

    for line in reader:
        content = line.split(DELIMITER)[COLUMN - 1].strip().decode(CODING,'ignore')

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
    count_file.write(utf8_2_gbk("统计结果：") + str(i + j))

    ResultWriter.close()
    reader.close()
