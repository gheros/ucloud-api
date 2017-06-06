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
group=config.get("group","group")
#基本配置
base_url='https://api.ucloud.cn/'
public_key='???'
private_key='???'
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
#接口调用访问程序
def _request_(param):
    url = base_url + '?' + _url_(param) + 'Signature=' + _verfy_ac(private_key, param)
    resp = urllib.request.urlopen(url)
    data = resp.read()
    print(data)
    print("接口调用完成")
    return data
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
#解绑IP
exitip={'Action':'UnBindEIP',
        'Region':'cn-gd',
        'EIPId':'eipid',
        'ResourceType':'uhost',
        'ResourceId':'uhostid',
        'PublicKey': 'DqTw4LBv58AqGa2ApYQWEsnFYDJtYbOdmEevnSvbQChNthctSbF5xw=='
        }
#停止主机
closeparam={'Action':'StopUHostInstance',
        'Region':'cn-gd',
        'Zone':'cn-gd-02',
        'UHostId':'uhost',
        'PublicKey': 'DqTw4LBv58AqGa2ApYQWEsnFYDJtYbOdmEevnSvbQChNthctSbF5xw=='
        }
#删除主机
delparam={'Action':'TerminateUHostInstance',
        'Region':'cn-gd',
        'Zone':'cn-gd-02',
        'UHostId':'uhost',
        'PublicKey': 'DqTw4LBv58AqGa2ApYQWEsnFYDJtYbOdmEevnSvbQChNthctSbF5xw=='
        }

#释放IP
delip={'Action':'ReleaseEIP',
        'Region':'cn-gd',
        'EIPId':'',
        'PublicKey': 'DqTw4LBv58AqGa2ApYQWEsnFYDJtYbOdmEevnSvbQChNthctSbF5xw=='
        }
def _del():
    false = 0
    true = 1
    param = eval(_request_(checktest).decode())
    print(param)
    #解绑定IP停止主机
    i=0
    while i<len(param['UHostSet']):
        try:
            exitip['EIPId']=param['UHostSet'][i]['IPSet'][1]['IPId']
        except :
            print('外网IP没有')
        exitip['ResourceId']=param['UHostSet'][i]['UHostId']
        closeparam['UHostId']=param['UHostSet'][i]['UHostId']
        _request_(exitip)
        _request_(closeparam)
        i=i+1
    ##删除主机释放IP
    i=0
    while i<len(param['UHostSet']):
        delparam['UHostId']=param['UHostSet'][i]['UHostId']
        try:
            delip['EIPId']=param['UHostSet'][i]['IPSet'][1]['IPId']
        except:
            print('外网IP没有')
        _request_(delparam)
        _request_(delip)
        i=i+1
    return
def main():
    _del()
if __name__ == '__main__':
    main()

# https://api.ucloud.cn/?Action=DescribeUHostTags&Region=cn-gd&PublicKey=DqTw4LBv58AqGa2ApYQWEsnFYDJtYbOdmEevnSvbQChNthctSbF5xw==&Zone=cn-gd-02&Signature=2be35cad6f45e87024f6fb79de4e273ef7e7e6d0
