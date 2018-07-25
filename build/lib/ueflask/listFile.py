from flask import request
import os,re
#列出文件
def lists(config):
    size=request.args.get("size",config['listSize'])
    start=request.args.get("start",0)
    end=int(start)+int(size)
    allowFiles=config["allowFiles"]
    #获取文件列表
    path="%s%s" % (os.getcwd(),config["path"])
    files=getfiles(path,allowFiles,config['path'])
    if len(files)==0:
        return {
            "state":"no match file",
            "list":[],
            "start":start,
            "total":len(files)
        }
    #获取指定范围的列表
    lenSize=len(files) if len(files)<end else end
    list=files[:lenSize]
    return {
        "state":"SUCCESS",
        "list":list,
        "start":start,
        "total":len(files)
    }

#遍历获取目录下的指定类型文件
def getfiles(path,allowFiles,realPath):
    if (not os.path.isdir(path)):
        return None
    if(path[-2:-1]!="/"):
        path="%s/" % path
    filess=[]
    for root,dirs,files in os.walk(path,topdown=False):
        for name in dirs:
            getfiles(os.path.join(root,name),allowFiles,realPath)
        for name in files:
            if os.path.splitext(name)[1] in allowFiles:
                filess.append({"url":fixUrl(re.findall("%s.+" % realPath,os.path.join(root,name))[0])})
    return filess

#修正url
def fixUrl(url):
    url=url.replace("//","/")
    url=url.replace("\\\\","/")
    url=url.replace("\\","/")
    return url

