# coding:utf-8
# author: hiddenblue
# 一个调用群晖download station 下载文件的api

from SynoAuto import SnoAuto

down_list = [] #这里面导入你需要批量下载的文件的url，带双引号，组成Python列表

account = "这里填入你的群晖用户名"

passwd = '这里填入你的群晖账户对应的密码'

path = '这里填入你的下载路径' # 比如 download 或者 video等

#初始化一个synoatuo实例对象
snoauto = SnoAuto(account, passwd, path)

#然后就开始快速下载了
for i in down_list:
    snoauto.synodown(i)