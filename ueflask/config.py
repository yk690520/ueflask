# -*- coding: utf-8 -*-
import os,json
#七牛云AK
_access_key=None
#七牛云SK
_secret_key=None
#七牛云Bucket
_bucket={}
#是否启用七牛云
_if_use_qiniu=False


def __checkSupixx(path):
    '''
    检查前缀
    :return:
    '''
    return path if path[:1]=="/" else "/%s" % path

def setAcSc(access_key:str,secret_key:str):
    '''
    设置主要key和存储空间的方法,如果设置了七牛云的ak和sk将会自动把图片上传至指定的七牛云key，并删除本地文件存储
    :param access_key:
    :param secret_key:
    :return:
    '''
    global _access_key
    global _secret_key
    global _if_use_qiniu
    _if_use_qiniu=True
    _access_key=access_key
    _secret_key=secret_key

def setBucket(bucket_name:str,bucket_host:str):
    '''
    设置bucket名字和域名
    :param bucket_name:bucket name
    :param bucket_host:bucket host
    :return:
    '''
    global _bucket
    if not "http://" in bucket_host:
        bucket_host="http://%s" % bucket_host
    if not bucket_host[-2:-1]=="/":
        bucket_host="%s/" % bucket_host
    _bucket[bucket_name]=bucket_host

