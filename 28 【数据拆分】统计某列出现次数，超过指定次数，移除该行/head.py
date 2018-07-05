#!/usr/bin/python
#coding=utf-8

import sys

# 功能说明：
# 取文件的前几行

####################以下是参数######################

LINE_NUM = 100000  # 行数
FILE_NAME = "save.csv"  #数据文件，必须是立方导出的数据
OUTPUT_FILE = "mini.csv"  #输出结果文件名


####################以上是参数######################



if __name__ == "__main__":
        ResultWriter = file(OUTPUT_FILE, "w+")
        reader = open(FILE_NAME, 'rb')
 
        count = 0
        for line in reader:
                count = count + 1
                if count > LINE_NUM:
                        break
                ResultWriter.write(line.strip() + '\n')

        ResultWriter.close()
        reader.close()
 
