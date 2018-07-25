--------------------------------项目说明-------------------------------

项目名：ueflask

ue说明：UEditor是由百度web前端研发部开发所见即所得富文本web编辑器，具有轻量，可定制，注重用户体验等特点，开源基于MIT协议，允许自由使用和修改代码.

项目说明：ueflask是基于flask框架，使用flask作为ueditor的后端服务器，实现ueditor的图片、视频、附件上传的支持

python环境：python3

--------------------------------项目重要文件说明-------------------------

-static

--ue       (ueditor前端控件）

---config   (ueditor配置文件放置目录)

----config.json   (ueditor配置文件，非常重要）


-templates           (flask模板放置文件夹)

--index.htm       (demo）


setup.py    (setup 安装文件)

---------------------------------项目使用说明（简单的Demo）-------------------------

1、使用git clone

2、使用 python setup.py install 安装ueflask包

3、将 static 下的文件拷贝至【你的项目】目录下的static目录里

4、将 templates 下的文件拷贝至【你的项目】目录下的templates目录里

5、在【你的项目】app.py里：

    from flask import Flask

    from flask import render_template

    import ueflask

    ueflask.setApp(app)

    @app.route("/")

    def hello():

    return render_template("index.html")


6、即可使用

---------------------------项目自带Demo展示----------------------------------------------------

1、cd ueflask目录

2、flask run

3、在浏览器访问127.0.0.1:5000即可

（提示：需先配置flask环境pip3 install flask)

----------------------------API--------------------------------------

ueflask.setApp(app:Flask,ueconfig="\static\ue\config\config.json"):

    @param:app 一个Flask对象

    @param:ueconfig ueconfig的配置文件，默认放置在\static\ue\config目录下
