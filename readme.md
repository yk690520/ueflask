--------------------------------项目说明-------------------------------

项目名：ueflask

ue说明：UEditor是由百度web前端研发部开发所见即所得富文本web编辑器，具有轻量，可定制，注重用户体验等特点，开源基于MIT协议，允许自由使用和修改代码.

项目说明：ueflask是基于flask框架，使用flask作为ueditor的后端服务器，实现ueditor的图片、视频、附件上传的支持

python环境：python3

版本说明：v0.4

其他说明：实现了后端图片、视频、文件、涂鸦上传，图片和附件的管理支持，但是远程抓图由于我没有找到使用入口，所以只是编写了代码并未做线上测试（知道的朋友可以email我，yk690520@outlook.com)

已知问题：单个上传图片和视频后不能自动插入编辑器，求大神解答

--------------------------------项目重要文件说明-------------------------

-static

--ue       (ueditor前端控件）

---config   (ueditor配置文件放置目录)

----config.json   (ueditor配置文件，非常重要）


-templates           (flask模板放置文件夹)

--index.htm       (demo）


setup.py    (setup 安装文件)

---------------------------------项目使用说明（简单的Demo）-------------------------

1、git clone git@github.com:yk690520/ueflask.git           #克隆ueflask代码

2、cd ueflask                 #进入ueflask目录

3、python setup.py install            #安装ueflask模块

4、将 static 下的文件拷贝至【你的项目】目录下的 static 目录里

5、将 templates 下的文件拷贝至【你的项目】目录下的 templates 目录里

6、在【你的项目】app.py里：

    from flask import Flask

    from flask import render_template

    import ueflask

    ueflask.setApp(app)

    @app.route("/")

    def hello():

        return render_template("index.html")


7、即可使用

---------------------------项目自带Demo展示----------------------------------------------------

1、git clone git@github.com:yk690520/ueflask.git           #克隆ueflask代码

2、cd ueflask                     #进入ueflask目录

3、python setup.py install

4、flask run                       #运行flask

5、在浏览器访问127.0.0.1:5000即可



----------------------------API--------------------------------------

ueflask.setApp(app:Flask,ueconfig="\static\ue\config\config.json"):

    @param:app 一个Flask对象

    @param:ueconfig ueconfig的配置文件，默认放置在\static\ue\config目录下
