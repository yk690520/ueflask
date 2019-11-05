from flask import request
from ueflask.qiniu import listFile
import os,re
import ueflask.config as config

class ListFile():
    def __init__(self,config):
        '''
        ListFile是一个列出指定目录下文件的类
        :param config: 相关的配置文件
        '''
        self._config=config
        self._files=[]  #所有的文件列表
        self._lists=[]  #实际返回的文件列表
        self.__lists()

    def __lists(self):
        '''
        执行列出文件的主方法
        :return: 无返回值
        '''
        size = request.args.get("size", self._config['listSize'])
        self._start = request.args.get("start", 0)
        end = int(self._start) + int(size)
        self._allowFiles = self._config["allowFiles"]
        # 获取文件列表
        if config._if_use_qiniu:
            self.__getFilesFromQiniusel()
        else:
            self._path = self.__addposfixx("%s%s" % (os.getcwd(), self.__addsufixx(self._config["path"])))
            self.__getfiles()
        if len(self._files) == 0:
            self._stateinfor="no match file"
        else:
            # 获取指定范围的列表
            lenSize = len(self._files) if len(self._files) < end else end
            self._lists = self._files[:lenSize]
            self._stateinfor="SUCCESS"

    def __getFilesFromQiniusel(self):
        '''
        从七牛云获取文件
        :return:null或者取到的文件
        '''
        files=listFile(self._config["path"],)
        self._files= [] if files==None else files


    def getReturnInfor(self):
        '''
        得到返回的字典
        :return:
        '''
        return {
            "state":self._stateinfor,
            "list":self._lists,
            "start":self._start,
            "total":len(self._files)
        }

    def __getfiles(self):
        '''
        得到path目录下的指定文件url字典，并追加至self._files
        :return:无
        '''
        for root, dirs, files in os.walk(self._path, topdown=False):
            for name in files:
                if os.path.splitext(name)[1] in self._allowFiles:
                    self._files.append({"url": self.__fixUrl(re.findall("%s.+" % self._config["path"], os.path.join(root, name))[0])})

    def __addsufixx(self,path):
        '''
        如果path首字符不是【/】，则添加，否则什么都不做
        :param path:
        :return: 添加后的字符串
        '''
        return path if path[:1]=="/" else "/%s" % path

    def __addposfixx(self,path):
        '''
        如果path尾字符不是【/】，则添加，否则什么都不做
        :param path:
        :return: 添加后的字符串
        '''
        return path if path[-2:-1]=="/" else "%s/" % path

    def __fixUrl(self,url):
        '''
        去除url中的双//，并把\\替换为\
        :param url:
        :return:返回替换后的url
        '''
        url = url.replace("//", "/")
        url = url.replace("\\\\", "/")
        url = url.replace("\\", "/")
        return url

