#!/usr/bin/python3
from flask import Flask
from flask import render_template
import ueflask
app=Flask(__name__)
#为ue设置flask对象，这是启动ue后端服务必须的方法
ueflask.setApp(app)
ueflask.setAcSc('BtJNCJFHJHbsBOA7YFLgZx2CqZ785adbpGj-w7zv','w2n95EOG4V3Lyj__JWGhuFGzu74gjBpUg-2eLB0D')
ueflask.setBucket("test","pcgvmcq7e.bkt.clouddn.com")
@app.route("/")
def hello():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()