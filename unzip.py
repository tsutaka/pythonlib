#!/usr/bin/python
# -*- coding: utf-8 -*-

import zipfile


def unZip(target_file_name='', output_path=''):
    #解凍
    with zipfile.ZipFile(target_file_name,'r') as inputFile:
        inputFile.extractall(output_path)
    print("unzip")

if __name__ == '__main__':
    unZip(
                target_file_name = "face_traindata.zip",
                output_path = "/home/fujitamtt/dev/chainer_imagenet_tools/101_ObjectCategories/",
    )
    print("ok")
