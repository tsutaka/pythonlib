#!/usr/bin/python
# -*- coding: utf-8 -*-

#read file return rows_list
def read_file(path='./', fileName=''):
    file_list = []
    with open(path + fileName,'r') as f:
        for row in f:
            # print(row.strip())
            file_list += row.strip()
    return file_list

#write file get rows_list
def write_file(path='./', fileName='', row_list=[]):
    with open(path + fileName,'w') as f:
        for row in row_list:
            # print(row)
            f.write(row + "\n")


if __name__ == '__main__':
    print(">start")
    str_list = read_file(
                path = "sample/",
                fileName = "sample_text.txt"
    )

    for row in str_list:
        print(row)

    str_list = ['1', '2', 'a']
    write_file(
                path = "sample/",
                fileName = "sample_outpu.txt",
                row_list = str_list
    )

    print(">end")
