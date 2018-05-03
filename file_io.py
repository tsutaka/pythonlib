#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

#read file return rows_list
def read_file(path='./', fileName=''):
    file_list = []
    with open(path + fileName,'r') as f:
        for row in f:
            # print(row.strip())
            file_list += [row.strip()]
    return file_list

#write file from rows_list
def write_file(path='./', fileName='', row_list=[]):
    with open(path + fileName,'w') as f:
        for row in row_list:
            # print(row)
            f.write(row + "\n")

def json2text(data):
    return json.dumps(
        data, ensure_ascii=False, indent=4,
        sort_keys=False, separators=(',', ': ')
        )

if __name__ == '__main__':
    print(">start")
    str_list = read_file(
                path = "sample/",
                fileName = "sample_text.txt"
    )

    for row in str_list:
        print(row)

    str_list = ['1', '2', 'ab']
    write_file(
                path = "sample/",
                fileName = "sample_outpu.txt",
                row_list = str_list
    )

    json_str = {"c": 0, "b": 0, "a": 0}
    print(json2text(json_str))


    print(">end")
