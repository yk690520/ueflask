# -*- coding: utf-8 -*-


from qiniu import Auth,put_file,etag
import qiniu.config

_access_key=None
_secret_key=None
_bucket={}


def uploadFile(key ,localfile,bucket_name=None):
    '''
    上传文件的方法
    :param key: 长传到七牛云保存的文件名,必须
    :param localfile: 要上传的文件，必须
    :param bucket_name: 要上传的空间，可选
    :return:返回上传成功的文件url,失败则返回None
    '''
    global _access_key
    global _secret_key
    temp_bucket_name,temp_bucket_host=__getABucket(bucket_name)
    if temp_bucket_name==None:
        raise BaseException("not set qiniu bucket")
    q=Auth(_access_key,_secret_key)

    token=q.upload_token(temp_bucket_name,key,3600)
    ret,info=put_file(token,key,localfile)

    name=ret.get("key")
    if not name:
        return None

    return "%s%s" % (temp_bucket_host,ret.get("key"))

def setBucket(bucket_name,bucket_host):
    '''
    设置bucket名字和域名
    :param bucket_name:
    :param bucket_host:
    :return:
    '''
    global _bucket
    if not "http://" in bucket_host:
        bucket_host="http://%s" % bucket_host
    if not bucket_host[-2:-1]=="/":
        bucket_host="%s/" % bucket_host
    _bucket[bucket_name]=bucket_host


def setAcScBucket(access_key,secret_key):
    '''
    设置主要key和存储空间的方法
    :param access_key:
    :param secret_key:
    :return:
    '''
    global _access_key
    global _secret_key
    _access_key=access_key
    _secret_key=secret_key

def __getABucket(cbucketName=None):
    '''
    获得一个bucket
    :return:
    '''
    global _bucket
    if cbucketName and cbucketName in _bucket:
        return cbucketName, _bucket[cbucketName]
    else:
        for bucketName,bucketHost in _bucket.items():
            return bucketName,bucketHost
    return None