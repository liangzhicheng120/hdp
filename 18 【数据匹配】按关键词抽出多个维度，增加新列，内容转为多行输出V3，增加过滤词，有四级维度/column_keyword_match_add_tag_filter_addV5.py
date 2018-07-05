#!/usr/bin/python
#coding=utf-8

import sys
import re

# 功能说明：
# 关键词匹配，根据码表打标签
# 支持关键词中  用 空格表示 and的关系
# 支持过滤词，用 空格表示 and的关系 eg:止咳，咳不出 痰
# 

####################以下是参数######################

COLUMN = 37      #要清洗的数据在第几列
FILE_NAME = "sample_min_test.csv"  #数据文件，必须是立方导出的数据
FILTER_WORDS = "sick.txt"  #过滤词文件
COLUMN_TOTAL = 42 #总列数

OUTPUT_FILE = "result.csv"  #输出结果文件名
REMOVE_FILE = "removed.csv" #被过滤的数据数据文件名


####################以上是参数######################
DELIMITER = ","
CODING = "gbk"
DELIMITER2 = "\t"
keyword_delimiter = " "

patternTemp = "(?=.*{0})"

other = " 无"
wrongID = []
match_words = dict()
filter_words = [] #


if __name__ == "__main__":
        ResultWriter = file(OUTPUT_FILE, "w+")
        reader = open(FILE_NAME, 'rb')

        add_head = ""

        with open(FILTER_WORDS, "rb") as f:
                add_head = next(f).replace('\xef\xbb\xbf', '').decode("utf-8")  #.replace('\ufeff', '')
                #print add_head
                for line in f:
                        words = line.decode("utf-8").strip().split(DELIMITER2)
                        #print len(words)
                        if len(words) < 4: #
                                continue
                        match_words[words[3]] = line.decode("utf-8").strip()
                        #filter_words.append(words[3]) #

        #print match_words.items()

        # print next(reader).strip() + DELIMITER + DELIMITER.join(add_head.split(DELIMITER2)[0:3]).encode(CODING)#.replace(DELIMITER2, DELIMITER)
        ResultWriter.write(next(reader).strip() + DELIMITER + DELIMITER.join(add_head.split(DELIMITER2)[0:3]).encode(CODING) + "\n")  # (抬头）
        for line in reader:
                data = line.strip().split(DELIMITER)
                if len(data) != COLUMN_TOTAL:
                        print line
                        continue
                content = data[COLUMN - 1].decode(CODING)

                matched = False
                
                for word, to_add in match_words.items():
                        words = word.split(DELIMITER)
                        pattrns = [ '(?=.*' + w + ')' for w in words]
                        pattern = re.compile(r'(' + ''.join(pattrns) + '.*)')
                        if pattern.match(content):
                        ######if word in content:
                                if len(to_add.split(DELIMITER2)) > 4: #带过滤词的情况
                                        filter_words = to_add.split(DELIMITER2)[4].split(DELIMITER)
                                        count = 0
                                        for filter_word in filter_words:                                                                
                                                #print filter_word
                                                if len(filter_word.split(keyword_delimiter)) > 1: #过滤词有空格表示and的情况
                                                        branch = 0
                                                        for ele in filter_word.split(keyword_delimiter):
                                                               if ele not in content:
                                                                        branch = branch + 1
                                                        if branch > 0: #只要有一个不匹配
                                                                count = count + 1
                                                elif filter_word not in content:
                                                        count = count + 1

                                        if count == len(filter_words): #全部过滤词都不匹配
                                                matched = True
                                                ######print word
                                                # ResultWriter.write(line.strip() + DELIMITER + to_add.encode(CODING).replace(DELIMITER2, DELIMITER) + "\n")
                                                ResultWriter.write(line.strip() + DELIMITER + DELIMITER.join(to_add.split(DELIMITER2)[0:3]).encode(CODING) + "\n")
                                else:
                                        matched = True
                                        ResultWriter.write(line.strip() + DELIMITER + DELIMITER.join(to_add.split(DELIMITER2)[0:3]).encode(CODING) + "\n")
                if not matched:
                        ResultWriter.write(line.strip() + ",,,\n")
                

        ResultWriter.close()
        reader.close()
 
