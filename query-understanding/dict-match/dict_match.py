#!/bin/python
# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('UTF8')

# line format : keyword<\t>type
def load_dict(in_file):
    key_array = []
    val_array = []
    for line in open(in_file):
        items = line.strip().split("\t")
        if len(items) == 2:
            key_array.append(items[0])
            val_array.append(items[1])
    return key_array, val_array
#  直接调用此函数,则按照词典的顺序依次匹配
def match_process(key_array, val_array, line):
    result_key = []
    result_val = []
    for i in range(len(key_array)):
        if line.find(key_array[i]) == -1:
            continue;
        else:
            result_key.append(key_array[i])
            result_val.append(val_array[i])
            line = line.replace(key_array[i], "\t", 1)
            continue;
    return result_key, result_val

# 调整词典的顺序,按照最长匹配优先
def string_len_compare(x, y):
    return len(y) - len(x)
def sort_pattern_by_len(key_array, val_array):
    tmp_dict = {}
    for i in range(len(key_array)):
        tmp_dict[key_array[i]] = val_array[i]
    key_array = sorted(key_array, cmp=string_len_compare)
    for i in range(len(key_array)):
        val_array[i] = tmp_dict[key_array[i]]
    return key_array, val_array

# 处理流程
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage :"
        print sys.argv[0] + " pattern_file 0-nature_match|1-len_priority < intput > output"
        exit();
    key_array, val_array = load_dict(sys.argv[1])
    if sys.argv[2] == "1":
        key_array, val_array = sort_pattern_by_len(key_array, val_array)
    for line in sys.stdin:
        line = line.strip()
        result_key, result_val = match_process(key_array, val_array, line)
        result_num = len(result_key)
        result_str = "";
        if result_num == 0:
            result_str = line + "\t0\t";
        else:
            result_str =  line + "\t" + str(result_num);
            for i in range(len(result_key)):
                result_str += "\t" + result_key[i] + " || " + result_val[i];
        print result_str
