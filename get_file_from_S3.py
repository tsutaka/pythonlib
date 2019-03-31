#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import json
import boto3
import logging
import configparser

s3 = boto3.resource('s3')
s3client = boto3.client('s3')

def get_file_from_s3(bucket_name='', path='', fileName=''):
    #open bucket
    bucket = s3.Bucket(bucket_name)
    print("open")

    #download
    bucket.download_file(Key=path, Filename=fileName)
    print("download")

if __name__ == '__main__':
    get_file_from_s3(
                bucket_name = "xxxx",
                path = "xxxx",
                fileName = "xxxx"
    )
    print("ok")
