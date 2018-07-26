# coding=utf-8
from ueflask.ue.uploader import Uploader
from ueflask.ue.listFile import ListFile
from flask import request
from flask import json
from flask import Flask
import re,os
from flask import jsonify

__ue_config=None

def setApp(app:Flask,ueconfig:str="/static/ue/config/config.json"):
    if isinstance(app,Flask):
        __loadconfig(ueconfig)
        app.route("/controller", methods=['GET', 'POST'])(__controller)
    else:
        raise BaseException("not is a flask object")
    pass


#ue的控制器处理方法
def __controller():
    global __ue_config
    action=request.args.get('action','')
    if request.method=='GET':
        if action=="config":
            return jsonify(__ue_config)
        else:
            return jsonify({"message":"error request"})
    elif request.method=='POST':
        if action=="uploadimage":
            config={
                "pathFormat":__ue_config['imagePathFormat'],
                "maxSize":__ue_config['imageMaxSize'],
                "allowFiles":__ue_config['imageAllowFiles']
            }
            fieldName=__ue_config['imageFieldName']
        elif action=="uploadscrawl":#暂未实现
            return None
        elif action=="uploadvideo":
            config={
                "pathFormat":__ue_config['videoPathFormat'],
                "maxSize":__ue_config['videoMaxSize'],
                "allowFiles":__ue_config['videoAllowFiles']
            }
            fieldName=__ue_config['videoFieldName']
        else:
            config={
                "pathFormat": __ue_config['filePathFormat'],
                "maxSize": __ue_config['fileMaxSize'],
                "allowFiles": __ue_config['fileAllowFiles']
            }
            fieldName=__ue_config['fileFieldName']
        uploader=Uploader(fieldName,config)
        return jsonify(uploader.getFileInfo())
    #列出图片
    elif action=="listimage":
        config={'allowFiles':__ue_config['imageManagerAllowFiles'],
                "listSize":__ue_config['imageManagerListSize'],
                "path":__ue_config['imageManagerListPath']
                }
        listFile=ListFile(config)
        return jsonify(listFile.getReturnInfor())


#载入ue配置文件
def __loadconfig(ueconfig="/static/ue/config/config.json"):
    global __ue_config
    if ueconfig[:1]!="/":
        ueconfig="/%s" % ueconfig
    path="%s%s" % (os.getcwd(),ueconfig)
    if not os.path.exists(path):
        raise FileNotFoundError("not found ue config file")
    if not os.access(path,os.R_OK):
        raise BaseException("can not read ue config file ")
    __ue_config=json.loads(re.sub("\/\*[\s\S]+?\*\/","",open(path,encoding='utf8').read()))
