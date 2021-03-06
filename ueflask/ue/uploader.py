#!/usr/bin/python3
# coding=utf-8
from datetime import datetime
from flask import request
from werkzeug.utils import secure_filename
import random,re,os
from ueflask.qiniu import *
import ueflask.config as config
import base64,ueflask.tools,socket
from urllib.request import urlopen
from urllib.request import urlretrieve
class Uploader():
    def __init__(self,fileField,config,type="upload"):
        '''
        Uploader是上传文件，图片，视频的主要类
        :param fileField: 文件域名
        :param config: 相关配置文件
        '''
        self._stateMap={
            "SUCESS":"SUCESS",
            "OUT_UPLOAD_MAX_SIZE":"文件大小超出 upload_max_filesize 限制",
            "OUT_FILE_MAX_SIZE":"文件大小超出 MAX_FILE_SIZE 限制",
            "FILE_UPLOAD_PART":"文件未被完整上传",
            "NO_FILE":"没有文件被上传",
            "FILE_IS_NULL":"上传文件为空",
            "ERROR_TMP_FILE": "临时文件错误",
            "ERROR_TMP_FILE_NOT_FOUND": "找不到临时文件",
            "ERROR_SIZE_EXCEED": "文件大小超出网站限制",
            "ERROR_TYPE_NOT_ALLOWED": "文件类型不允许",
            "ERROR_CREATE_DIR": "目录创建失败",
            "ERROR_DIR_NOT_WRITEABLE": "目录没有写权限",
            "ERROR_FILE_MOVE": "文件保存时出错",
            "ERROR_FILE_NOT_FOUND": "找不到上传文件",
            "ERROR_WRITE_CONTENT": "写入文件内容错误",
            "ERROR_UNKNOWN": "未知错误",
            "ERROR_DEAD_LINK": "链接不可用",
            "ERROR_HTTP_LINK": "链接不是http链接",
            "ERROR_HTTP_CONTENTTYPE": "链接contentType不正确",
            "INVALID_URL": "非法 URL",
            "INVALID_IP": "非法 IP",
            "UNKNOWN_ERROR":"未知错误"
        }
        self._fileField=fileField
        self._config=config
        if type=="remote":
            self.__saveRemote()
            pass
        elif type=="base64":
            self.__upBase64()
        else:
            self.__upFile()

    def __saveRemote(self):
        '''
        保存远程图片
        :return:
        '''
        imgurl=self._fileField.replace("&amp;","&")

        #http开头验证
        if imgurl.find("http")!=0:
            self._stateInfo=self.__getStateInfo("ERROR_HTTP_LINK")
            return

        #判断是否是合法 url
        matches=re.findall("(^https*:\/\/[^:\/]+)",imgurl)
        host_with_protocol='' if len(matches)<=0 else matches[0]

        if not re.match(r'^https?:/{2}\w.+$',host_with_protocol):
            self._stateInfo=self.__getStateInfo("INVALID_URL")
            return
        matches=re.findall("^https*:\/\/(.+)",host_with_protocol)
        host_with_protocol='' if len(matches)<=0 else matches[0]

        ip=socket.gethostbyname(host_with_protocol)
        if not ueflask.tools.isPrivateIp(ip):
            self._stateInfo=self.__getStateInfo("INVALID_IP")
            return
        #检测是否死链
        response = urlopen(imgurl)
        if response.msg!="OK" and response.status!=200:
            self._stateInfo=self.__getStateInfo("ERROR_HTTP_CONTENTTYPE")
            return

        #格式验证
        self._oriName=imgurl
        self._fileType=self.__getFileType()
        if not self.__checkType():
            self._stateInfo = self.__getStateInfo("ERROR_SIZE_EXCEED")
            return

        matches=re.findall("[\/]([^\/]*)[\.]?[^\.\/]*$",imgurl)
        self._oriName='' if len(matches)<=0 else matches[0]
        self._fileSize=response.length
        self._fullName=self.__getFullName()
        self._filePath=self.__getFilePath()
        self._fileName=self.__getFileName()
        dirname = os.path.dirname(self._filePath)
        if (not self.__checkSize()):
            self._stateInfo = self.__getStateInfo("ERROR_SIZE_EXCEED")
            return
        if (not os.path.exists(dirname)):
            try:
                os.makedirs(dirname)
            except NotImplementedError as e:
                self._stateInfo = self.__getStateInfo("ERROR_CREATE_DIR")
                return
        elif (not os.access(dirname, os.W_OK)):
            self._stateInfo = self.__getStateInfo("ERROR_DIR_NOT_WRITEABLE")

        #保存文件
        urlretrieve(imgurl,self._filePath)
        if not os.path.exists(self._filePath):
            self._stateInfo=self.__getStateInfo("ERROR_WRITE_CONTENT")
        else:
            self._stateInfo=self._stateMap["SUCESS"]
        # 上传至七牛云
        self.__uploadQiniu()


    def __upFile(self):
        '''
        执行上传的主要方法
        :return:None
        '''
        if self._fileField not in request.files:
            self._stateInfo=self.__getStateInfo("ERROR_FILE_NOT_FOUND")
            return
        #取到上传的文件对象
        file=request.files[self._fileField]
        self._oriName = file.filename
        if self._oriName=="":
            self._stateInfo=self.__getStateInfo("ERROR_FILE_NOT_FOUND")
            return


        ######
        self._fileSize = file.stream._max_size  ######此代码不一定是正确的
        ######

        self._fileType=self.__getFileType()#文件后缀
        self._fullName=self.__getFullName()#完整的文件名（从站点目录下开始）
        self._filePath=self.__getFilePath()#完整的文件路径（全路径）
        self._fileName=self.__getFileName()#文件名
        dirname=os.path.dirname(self._filePath)

        if(not self.__checkSize()):
            self._stateInfo=self.__getStateInfo("ERROR_SIZE_EXCEED")
            return

        if(not self.__checkType()):
            self._stateInfo=self.__getStateInfo("ERROR_TYPE_NOT_ALLOWED")
            return
        #如果目录是不存在的
        if(not os.path.exists(dirname)):
            try:
                os.makedirs(dirname)
            except NotImplementedError as e:
                self._stateInfo=self.__getStateInfo("ERROR_CREATE_DIR")
                return
        elif(not os.access(dirname,os.W_OK)):
            self._stateInfo=self.__getStateInfo("ERROR_DIR_NOT_WRITEABLE")

        #保存文件
        try:
            file.save(self._filePath)
        except:
            self._stateInfo = self.__getStateInfo("UNKNOWN_ERROR")
        else:
            self._stateInfo=self._stateMap["SUCESS"]

        # 上传至七牛云
        self.__uploadQiniu()

    def __upBase64(self):
        '''
        base64的上传方法
        :return:
        '''
        try:
            base64Data=request.form[self._fileField]
        except KeyError:
            self._stateInfo=self.__getStateInfo("NO_FILE")
            return
        #获取base64位的图片数据

        img=base64.b64decode(base64Data)

        self._oriName=self._config['oriName']
        self._fileSize=len(img)
        self._fileType=self.__getFileType()
        self._fullName=self.__getFullName()
        self._filePath=self.__getFilePath()
        self._fileName=self.__getFileName()

        dirname = os.path.dirname(self._filePath)

        if (not self.__checkSize()):
            self._stateInfo = self.__getStateInfo("ERROR_SIZE_EXCEED")
            return
            # 如果目录是不存在的
        if (not os.path.exists(dirname)):
            try:
                os.makedirs(dirname)
            except NotImplementedError as e:
                self._stateInfo = self.__getStateInfo("ERROR_CREATE_DIR")
                return
        elif (not os.access(dirname, os.W_OK)):
            self._stateInfo = self.__getStateInfo("ERROR_DIR_NOT_WRITEABLE")

        #保存img
        try:
            #保存base64位的图片需要用2进制的方法打开文件
            with open(self._filePath,"wb") as f:
                f.write(img)
        except:
            self._stateInfo=self.__getStateInfo("UNKNOWN_ERROR")
        else:
            self._stateInfo=self._stateMap["SUCESS"]

        #上传至七牛云
        self.__uploadQiniu()


    def __uploadQiniu(self):
        if config._if_use_qiniu:
            try:
                self._fullName = uploadFile(self._fullName, self._filePath)
                if self._fullName == None:
                    self._stateInfo = self.__getStateInfo("UNKNOWN_ERROR")
            finally:
                if os.path.exists(self._filePath) and os.access(self._filePath,os.W_OK) and config._if_use_qiniu:
                    os.remove(self._filePath)

    #检测文件类型
    def __checkType(self):
        return self._fileType in self._config['allowFiles']

    #检查文件大小
    def __checkSize(self):
        return self._fileSize<=self._config["maxSize"]

    #获取新的文件名
    def __getFileName(self):
        return self._filePath.split("/")[-1]

    #获取文件完整路径
    def __getFilePath(self):
        fullname=self._fullName
        rootPath=os.getcwd()
        if fullname[:1]!="/":
            fullname="/%s" % fullname
        return "%s%s" %(rootPath,fullname)

    #重名名文件
    def __getFullName(self):
        #替换日期时间
        now = datetime.now()
        time = int(now.timestamp() * 1000)
        date = now.strftime("%Y-%y-%m-%d-%H-%M-%S").split("-")
        format=self._config["pathFormat"]
        if format[:1]!="/":
            format="/%s" % format
        format=format.replace("{yyyy}",date[0])
        format = format.replace("{yy}", date[1])
        format = format.replace("{mm}", date[2])
        format = format.replace("{dd}", date[3])
        format = format.replace("{hh}", date[4])
        format = format.replace("{ii}", date[5])
        format = format.replace("{ss}", date[6])
        format = format.replace("{time}", str(time))
        #替换文件名的非法字符，并替换文件名
        oriName=secure_filename(self._oriName if self._oriName.rfind(".") == -1 else self._oriName[:self._oriName.rfind(".")])
        format=format.replace("{filename}",oriName)
        #替换随机字符串
        randNum = str(int(random.random() * 10000000000))[:int(re.findall("\{rand\:([\d]*)\}", format)[0])]
        format = re.sub("\{rand\:[\d]*\}", randNum, format)

        ext=self._fileType
        return format if ext=="" else "%s%s" % (format,ext)


    #获取文件类型
    def __getFileType(self):
        return "" if self._oriName.rfind(".")==-1 else self._oriName[self._oriName.rfind("."):].lower()

    #获取编码相对应的错误
    def __getStateInfo(self,error):
        if error in self._stateMap:
            return self._stateMap[error]
        else:
            return self._stateMap['UNKNOWN_ERROR']



    #获取返回信息
    def getFileInfo(self):
        return {
            "state":self._stateInfo,
            "url":self._fullName,
            "title":self._fileName,
            "original":self._oriName,
            "type":self._fileType,
            "size":self._fileSize
        }


