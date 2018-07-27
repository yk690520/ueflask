import ueflask.ue
import ueflask.qiniu
import ueflask.config

#此方法用来设置flask和对应的ue配置文件位置
setApp=ueflask.ue.__setApp

#此方法用来设置七牛云的AK和SK以及存储空间
setAcSc=ueflask.config.setAcSc

#此方法用来设置七牛云存储空间
setBucket=ueflask.config.setBucket
