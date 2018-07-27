# -*- coding: utf-8 -*-


from qiniu import Auth,put_file,etag
import ueflask.config as config

def uploadFile(key ,localfile,bucket_name=None):
    '''
    上传文件的方法
    :param key: 长传到七牛云保存的文件名,必须
    :param localfile: 要上传的文件，必须
    :param bucket_name: 要上传的空间，可选
    :return:返回上传成功的文件url,失败则返回None
    '''
    temp_bucket_name,temp_bucket_host=__getABucket(bucket_name)
    if temp_bucket_name==None:
        raise BaseException("not set qiniu bucket")
    q=Auth(config._access_key,config._secret_key)

    token=q.upload_token(temp_bucket_name,key,3600)
    ret,info=put_file(token,key,localfile)

    name=ret.get("key")
    if not name:
        return None

    return "%s%s" % (temp_bucket_host,ret.get("key"))


def __getABucket(cbucketName=None):
    '''
    获得一个bucket
    :return:
    '''
    if not config._bucket:
        raise  BaseException("not set qiniu a bucket")
    if cbucketName and cbucketName in config._bucket:
        return cbucketName, config._bucket[cbucketName]
    else:
        for bucketName,bucketHost in config._bucket.items():
            return bucketName,bucketHost
    return None