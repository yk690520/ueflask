import ueflask.ue
import ueflask.qiniu


#此方法用来设置flask和对应的ue配置文件位置
setApp=ueflask.ue.setApp

#此方法用来设置七牛云的AK和SK以及存储空间
setAcScBucket=ueflask.qiniu.setAcScBucket

#此方法用来设置七牛云存储空间
setBucket=ueflask.qiniu.setBucket

#此方法用来设置是否启用七牛云
openQiniu=