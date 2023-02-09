# coding:utf-8
# author: hiddenblue
# 一个调用群晖download station 下载文件的api


from SynoAuto import SnoAuto

down_list = [] #这里面导入你需要批量下载的文件的url，带双引号，组成Python列表

# 直接复制群晖f12页面下方请求表头的cookies内容填入即可
cookies = '这里填入你的浏览器cookies'

entry_url = '这里填入你的群晖的地址' + '/webapi/entry.cgi'

# 在下面填入群晖f12页面请求表头里面的X-SYNO-TOKEN值，比如.xxxxxx
header = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78",
    'X-Requested-With': 'XMLHttpRequest',
    'X-SYNO-TOKEN': '.VuLDpcgVUEYU'}

path = '这里填入你的下载路径' # 比如 download 或者 video等

#群晖下载任务需要以上四个参数，缺一不可

snoauto = SnoAuto(cookies, entry_url, header, path)

for i in down_list:
    snoauto.synodown(i)