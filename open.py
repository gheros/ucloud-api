#!/usr/bin/env python -u
# -*- coding: utf-8 -*-
import hashlib
# import urlparse
import urllib.request
import urllib
from collections import OrderedDict
import configparser
import time


config=configparser.ConfigParser()
config.read("config.ini")
image=['','','','']
image[0]=config.get("uhost-main","image")
image[1]=config.get("uhost-ws","image")
image[2]=config.get("uhost-bkbrws","image")
image[3]=config.get("uhost-bkbr360","image")
group=config.get("group","group")
list=config.get("open","list")
print(image)
#基本配置
base_url='https://api.ucloud.cn/'
public_key='???'
private_key='???'
#文件操作
#签名算法
def _verfy_ac(private_key, params):
    items=OrderedDict(sorted(params.items(), key=lambda t: t[0]))
    params_data = "";
    for key,value in items.items():
        params_data = params_data + str(key) + str(value)
    params_data = params_data + private_key
    sign = hashlib.sha1()
    sign.update(params_data.encode())
    signature = sign.hexdigest()
    print("签名ok")
    return signature
#字符串排序加工
def _url_(params):
    params_data=''
    items = OrderedDict(sorted(params.items(), key=lambda t: t[0]))
    for key,value in items.items():
        params_data=params_data+str(key)+'='+str(value)+'&'
    print("字符串排序完成")
    return params_data
#接口调用访问程序与字符串拼接
def _request_(param):
    url = base_url + '?' + _url_(param) + 'Signature=' + _verfy_ac(private_key, param)
    print(url)
    resp = urllib.request.urlopen(url)
    data = resp.read()
    print(data)
    print("接口调用完成")
    return data
#以上属于字符串拼接以及加工主要框架，完成字符串处理签名以及接口调用的主接口
#---我是分割线------------------#
#以下主要是对调用的字典以及其他功能扩展
#查看服务组字符串
param={'Action':'DescribeUHostTags',
       'Region':'cn-gd',
       'Zone':'cn-gd-02',
       'PublicKey': 'DqTw4LBv58AqGa2ApYQWEsnFYDJtYbOdmEevnSvbQChNthctSbF5xw=='}
#创建云主机1main
createuhost1={'Action':'CreateUHostInstance',
        'Region':'cn-gd',
        'Zone':'cn-gd-02',
        'Tag':group,
        'ImageId':image[0],#镜像名main uimage-k4gv2s
        'CPU':1,
        'Memory':2048,
        'StorageType':'LocalDisk',#硬盘
        'DiskSpace':0,#硬盘大小
        'LoginMode':'Password',#登录模式
        'Password':'TmV0LmNyYXdsZXI=',#登录密码
        'Name':'main',#名称mian
        'ChargeType':'Dynamic',#付费模式，year为年，mouth为月，Dynamic按量
        'Quantity': 1,#付费时长
        'PublicKey': 'DqTw4LBv58AqGa2ApYQWEsnFYDJtYbOdmEevnSvbQChNthctSbF5xw=='}
#创建云主机2tianyawenshu
createuhost2={'Action':'CreateUHostInstance',
        'Region':'cn-gd',
        'Zone':'cn-gd-02',
        'Tag':group,
        'ImageId':image[1],#镜像名
        'CPU':1,
        'Memory':2048,
        'StorageType':'LocalDisk',#硬盘
        'DiskSpace':0,#硬盘大小
        'LoginMode':'Password',#登录模式
        'Password':'TmV0LmNyYXdsZXI=',#登录密码
        'Name':'tianyawenshu',#名称
        'ChargeType':'Dynamic',#付费模式，year为年，mouth为月，Dynamic按量
        'Quantity': 1,#付费时长
        'PublicKey': 'DqTw4LBv58AqGa2ApYQWEsnFYDJtYbOdmEevnSvbQChNthctSbF5xw=='}
#创建云主机3bkbrwenshu
createuhost3={'Action':'CreateUHostInstance',
        'Region':'cn-gd',
        'Zone':'cn-gd-02',
        'Tag':group,
        'ImageId':image[2],#镜像名
        'CPU':1,
        'Memory':2048,
        'StorageType':'LocalDisk',#硬盘
        'DiskSpace':0,#硬盘大小
        'LoginMode':'Password',#登录模式
        'Password':'TmV0LmNyYXdsZXI=',#登录密码
        'Name':'bkbrwenshu',#名称
        'ChargeType':'Dynamic',#付费模式，year为年，mouth为月，Dynamic按量
        'Quantity': 1,#付费时长
        'PublicKey': 'DqTw4LBv58AqGa2ApYQWEsnFYDJtYbOdmEevnSvbQChNthctSbF5xw=='}
#创建云主机4，bkbrwenshu360mobile
createuhost4={'Action':'CreateUHostInstance',
        'Region':'cn-gd',
        'Zone':'cn-gd-02',
        'Tag':group,
        'ImageId':image[3],#镜像名
        'CPU':1,
        'Memory':2048,
        'StorageType':'LocalDisk',#硬盘
        'DiskSpace':0,#硬盘大小
        'LoginMode':'Password',#登录模式
        'Password':'TmV0LmNyYXdsZXI=',#登录密码
        'Name':'bkbrwenshu360mobile',#名称
        'ChargeType':'Dynamic',#付费模式，year为年，mouth为月，Dynamic按量
        'Quantity': 1,#付费时长
        'PublicKey': 'DqTw4LBv58AqGa2ApYQWEsnFYDJtYbOdmEevnSvbQChNthctSbF5xw=='}

#创建网络
createeip={'Action':'AllocateEIP',
           'Bandwidth':100,#带宽大小
           'OperatorName':'Bgp',
           'Tag':group,#业务组
           'ChargeType':'Dynamic',#付费方式
           'Quantity':1,
           'PayMode':'Traffic',#流量计费
           'Name':'EIP',#名称
           'Region':'cn-gd',
           'PublicKey': 'DqTw4LBv58AqGa2ApYQWEsnFYDJtYbOdmEevnSvbQChNthctSbF5xw=='
           }
#绑定网络格式方式
bangip={'Action':'BindEIP',
        'Region':'cn-gd',
        'EIPId':'eip-1inlb2',
        'ResourceType':'uhost',
        'ResourceId':'uhost-0ttesd',
        'PublicKey': 'DqTw4LBv58AqGa2ApYQWEsnFYDJtYbOdmEevnSvbQChNthctSbF5xw=='
        }
#检查主机并找到相关主机
#检测云主机
checktest={'Action':'DescribeUHostInstance',
           'Region': 'cn-gd',
           'Zone': 'cn-gd-02',
           'Tag':group,
           # 'HostIds.0':'uhost-qs20fr',
# &UHostIds.0=uhost-qs20fr
# &Offset=0
    'Limit':100,
'PublicKey': 'DqTw4LBv58AqGa2ApYQWEsnFYDJtYbOdmEevnSvbQChNthctSbF5xw=='}
#重启主机
reboot={'Action':'RebootUHostInstance',
        'Region':'cn-gd',
        'Zone':'cn-gd-02',
        'UHostId':'uhost-qs20fr',
        'PublicKey': 'DqTw4LBv58AqGa2ApYQWEsnFYDJtYbOdmEevnSvbQChNthctSbF5xw=='
}

#应用防火墙
firewall={'Action':'GrantSecurityGroup',
            'Region':'cn-gd',
            'GroupId':'firewall-4wfrlx',
            'ResourceType':'UHost',
            'ResourceId':'uhost-test',
            'PublicKey': 'DqTw4LBv58AqGa2ApYQWEsnFYDJtYbOdmEevnSvbQChNthctSbF5xw=='
            }
def closehost(param):
    x = open('uhost.txt')
    b = []
    for line in x.readlines():
        b.append(line.strip())
        param['UHostId'] = line.strip()
        print(param)
        tt = _request_(param)
        pass
    print(b)
    x.close()
    return tt
#带ip的开机并写入文件
def buhostip(createhost,createip):
    try:
        hostparam={'Action':'BindEIP',
               'Region':'cn-gd',
               'EIPId':'',
               'ResourceType':'uhost',
               'ResourceId':'uhost-0ttesd',
               'PublicKey': 'DqTw4LBv58AqGa2ApYQWEsnFYDJtYbOdmEevnSvbQChNthctSbF5xw=='
               }
        host=_request_(createhost)#绑定的机器
        time.sleep(1)
        ip=_request_(createip)
        time.sleep(1)
        print(host)
        print(ip)
        hostparam['EIPId']=eval(ip)['EIPSet'][0]['EIPId']
        hostparam['ResourceId'] = eval(host)['UHostIds'][0]
        ddd=_request_(hostparam)
        print("ip机器绑定成功")
    except:
        print("ip绑定出现异常")
    return ddd
#文件输出写入
def filewrite(param,name):
    f=open(name,'a')
    f.writelines(param+'\n')
    f.close()
#文件读取

#删除主机函数调用，需先关闭主机,读取第一行，并且删除主机，然后删除第一行
def closehost(param):
    x = open('uhost.txt')
    a=x.readline()
    param['UHostId']=a.strip()
    print(param)
    tt=_request_(param)
    print(tt)
    # param['UHostId']=eval(tt)['UHostId'][0]
    # param['Action']='TerminateUHostInstance'
    # fout = open('uhost.txt', 'w')
    # b = ''.join(a[1:])
    # fout.write(b)
    x.close()
    # fout.close()
    return tt
#解绑IP
exitip={'Action':'UnBindEIP',
        'Region':'cn-gd',
        'EIPId':'eip',
        'ResourceType':'uhost',
        'ResourceId':'uhost',
        'PublicKey': 'DqTw4LBv58AqGa2ApYQWEsnFYDJtYbOdmEevnSvbQChNthctSbF5xw=='
        }
#释放IP
closeeip={'Action':'ReleaseEIP',
        'Region':'cn-gd',
        'EIPId':'eip',
        'PublicKey': 'DqTw4LBv58AqGa2ApYQWEsnFYDJtYbOdmEevnSvbQChNthctSbF5xw=='
        }
def closeip(param):
    x = open('ueip.txt')
    a = x.readline()
    param['UHostId'] = a.strip()
    print(param)
    tt = _request_(param)
    fout = open('ueip.txt', 'w')
    b = ''.join(a[1:])
    fout.write(b)
    x.close()
    fout.close()
    return tt
def _reboot_():
    bb = _request_(checktest).decode()
    print(bb)
    false = 0
    true = 1
    # uhostsset后的数字可遍历
    # print(eval(bb)['UHostSet'][0]['IPSet'][1]['IP'])
    # 主机ID
    print(eval(bb)['UHostSet'][1]['UHostId'])
    i = 0
    print(len(eval(bb)['UHostSet']))
    while i < len(eval(bb)['UHostSet']):
        print(eval(bb)['UHostSet'][i]['UHostId'])
        reboot['UHostId']=eval(bb)['UHostSet'][i]['UHostId']
        firewall['ResourceId']=eval(bb)['UHostSet'][i]['UHostId']
        _request_(reboot)
        _request_(firewall)
        print('正在重启'+reboot['UHostId'])
        i = i + 1


def _group_(a):
    count = 0
    while (count<a):
       print(a)
       count=count+1
       buhostip(createuhost1, createeip)
       time.sleep(1)
       buhostip(createuhost2, createeip)
       time.sleep(1)
       buhostip(createuhost3, createeip)
       time.sleep(1)
       buhostip(createuhost3, createeip)
       time.sleep(1)
       buhostip(createuhost4, createeip)
       time.sleep(1)
       buhostip(createuhost4, createeip)
       time.sleep(1)
def main():
    _group_(int(list))
    time.sleep(300)
    _reboot_()
    time.sleep(240)

if __name__ == '__main__':
    main()


# https://api.ucloud.cn/?Action=DescribeUHostTags&Region=cn-gd&PublicKey=DqTw4LBv58AqGa2ApYQWEsnFYDJtYbOdmEevnSvbQChNthctSbF5xw==&Zone=cn-gd-02&Signature=2be35cad6f45e87024f6fb79de4e273ef7e7e6d0
