# coding=utf-8
from ueflask.ue.uploader import Uploader
from ueflask.ue.listFile import ListFile
from flask import request
from flask import json
from flask import Flask
import re,os
from flask import jsonify
from functools import wraps
from flask import current_app


def __setApp(app:Flask,ueconfig:str="/static/ue/config/config.json"):
    '''
    设置flask对象
    :param app: flask原始对象
    :param ueconfig: ue配置文件放置位置，默认在/static/ue/config/config.json
    :return:
    '''
    if isinstance(app,Flask):
        __loadconfig(ueconfig)
        app.route("/controller", methods=['GET', 'POST'])(__controller)
    else:
        raise BaseException("not is a flask object")
    pass


def jsonp(func):
    '''
    #来自flask官网的代码段：网址为http://flask.pocoo.org/snippets/79/
    """Wraps JSONified output for JSONP requests."""
    :param func:
    :return:
    '''
    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            data = str(func(*args, **kwargs).data)
            content = str(callback) + '(' + data + ')'
            mimetype = 'application/javascript'
            return current_app.response_class(content, mimetype=mimetype)
        else:
            return func(*args, **kwargs)
    return decorated_function

#ue的控制器处理方法
@jsonp
def __controller():
    global __ue_config
    action=request.args.get('action','')
    if request.method=='GET':
        if action=="config":
            return jsonify(__ue_config)
        elif action == "listimage":
            config = {'allowFiles': __ue_config['imageManagerAllowFiles'],
                      "listSize": __ue_config['imageManagerListSize'],
                      "path": __ue_config['imageManagerListPath']
                      }
            listFile = ListFile(config)
            return jsonify(listFile.getReturnInfor())
        elif action=="listfile":
            config = {'allowFiles': __ue_config['fileManagerAllowFiles'],
                      "listSize": __ue_config['fileManagerListSize'],
                      "path": __ue_config['fileManagerListPath']
                      }
            listFile = ListFile(config)
            return jsonify(listFile.getReturnInfor())
        elif action=="catchimage":
            config={
                "pathFormat": __ue_config['catcherPathFormat'],
                "maxSize": __ue_config['catcherMaxSize'],
                "allowFiles": __ue_config['catcherAllowFiles'],
                "oriName": "remote.png"
            }
            fieldName=__ue_config['catcherFieldName']
            lists=[]
            sources=request.form.get('source')
            if sources:
                for source in sources:
                    uploader=Uploader(source,config,"remote")
                    infor=uploader.getFileInfo()
                    lists.append({
                        "state":infor["state"],
                        "url":infor["url"],
                        "size":infor["url"],
                        "title":infor["title"],
                        "original":infor["original"],
                        "source":source
                    })
            return jsonify({
                'state':'ERROR' if len(list)<=0 else 'SUCCESS',
                'list':list
            })

        else:
            return jsonify({"state":"error request"})
    elif request.method=='POST':
        type="upload"
        if action=="uploadimage":
            config={
                "pathFormat":__ue_config['imagePathFormat'],
                "maxSize":__ue_config['imageMaxSize'],
                "allowFiles":__ue_config['imageAllowFiles']
            }
            fieldName=__ue_config['imageFieldName']
        elif action=="uploadscrawl":#暂未实现
            config = {
                "pathFormat": __ue_config['imagePathFormat'],
                "maxSize": __ue_config['imageMaxSize'],
                "allowFiles": __ue_config['imageAllowFiles'],
                "oriName":"scrawl.png"
            }
            fieldName=__ue_config['scrawlFieldName']
            type="base64"
        elif action=="uploadvideo":
            config={
                "pathFormat":__ue_config['videoPathFormat'],
                "maxSize":__ue_config['videoMaxSize'],
                "allowFiles":__ue_config['videoAllowFiles']
            }
            fieldName=__ue_config['videoFieldName']
        elif action=="uploadfile":
            config={
                "pathFormat": __ue_config['filePathFormat'],
                "maxSize": __ue_config['fileMaxSize'],
                "allowFiles": __ue_config['fileAllowFiles']
            }
            fieldName=__ue_config['fileFieldName']
        else:
            return jsonify({"state":"error request"})
        uploader=Uploader(fieldName,config,type)
        return jsonify(uploader.getFileInfo())
    #列出图片



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
