import socket
import struct


def isPrivateIp(ip):
    '''
    代码来自https://blog.csdn.net/kwsy2008/article/details/50098701
    :param ip:
    :return:
    '''
    ip1 = 167772160
    ip2 = 2886729728
    ip3 = 3232235520
    # 将ip地址转换成二进制的形式
    binaryIp = socket.inet_aton(ip)
    # 将二进制转成无符号long型
    numIp = struct.unpack('!L', binaryIp)[0]
    # 32位都是1
    mark = 2 ** 32 - 1
    # 取numIP的前16位
    tag = (mark << 16) & numIp
    if ip3 == tag:
        return True
    # 取numIP的前12位
    tag = mark << 20 & numIp
    if ip2 == tag:
        return True
    # 取numIP的前8位
    tag = (mark << 24) & numIp
    if ip1 == tag:
        return True
    return False
