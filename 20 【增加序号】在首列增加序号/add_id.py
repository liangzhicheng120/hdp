#!/usr/bin/python
#coding=utf-8

import sys

# 功能说明：
# 给每一行加id

####################以下是参数######################

FILE_NAME = "test-mini-match.csv"  #数据文件，必须是立方导出的数据

OUTPUT_FILE = "raw_id.txt"  #输出结果文件名


####################以上是参数######################
DELIMITER = ","


if __name__ == "__main__":
        ResultWriter = file(OUTPUT_FILE, "w+")
        reader = open(FILE_NAME, 'rb')
 
        count = 0
        for line in reader:
                count = count + 1
                ResultWriter.write(str(count) + DELIMITER + line.strip() + '\n')

        ResultWriter.close()
        reader.close()
 
