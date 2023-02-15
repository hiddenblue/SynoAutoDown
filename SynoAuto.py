import json
import requests
import re
from time import sleep

class SnoAuto(object):

    def __init__(self, account: str, passwd: str, down_path:str):
        self.down_path = down_path
        # 默认的同时进行的最大任务数
        self.max_down_task = 2
        self.max_error_task = 3
        self.session = requests.Session()
        self.initiateSession(account, passwd)
        # 默认的最大错误任务数
        # self.check_payload = {'sort_by': "task_id",'order': "ASC",'action': "enum",'type': '["emule"]','type_inverse': 'true','limit': '25','additional': '["detail", "transfer"]','status': 'null','status_inverse': 'null','api': 'SYNO.DownloadStation2.Task','method': 'list','version': '2',}

    #这一步是构建requests session 来初始化一个session对象，方便后面自动调用cookies，等参数
    def initiateSession(self, account, passwd):
        self.loginUrl = 'http://sustech.fun:5000/webapi/entry.cgi/'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41'}
        self.loginData  = {
        'api': 'SYNO.API.Auth',
        'version': '7',
        'method': 'login',
        'account': '%s'%account,
        'passwd': '%s'%passwd}
        self.session.headers = self.headers
        initialResponse =  self.session.post(self.loginUrl, data= self.loginData)
        print(initialResponse.status_code)
        print(initialResponse.text)
        if (initialResponse.status_code==200) and (json.loads(initialResponse.text).get("success")==True):
            print("successfully initiate the SnoAuto session")
        else:
            print("sorry. Fail to initiate the SnoAuto session")
            print("please check your network and login parameter")

    def connect(self, data: dict) -> str:
        resonse = self.session.post(url=self.loginUrl, data=data)
        print(resonse.status_code)
        return resonse.text

    def get_task_list(self) -> tuple[dict, list]:

        check_payload = {'sort_by': "task_id", 'order': "ASC", 'action': "enum", 'type': '["emule"]',
                         'type_inverse': 'true', 'limit': '100', 'additional': '["detail", "transfer"]',
                         'status': 'null', 'status_inverse': 'null', 'api': 'SYNO.DownloadStation2.Task',
                         'method': 'list', 'version': '2', }
        task_list_result = self.connect(check_payload)
        #print(task_list_result)
        response = json.loads(task_list_result).get('data').get('task')
        task_list = []
        if (response):
            for i in response:
                task_list.append(i['additional']['detail']['uri'])
        #print(task_list)
        print(len(task_list))
        return response,task_list

    def get_task_staus(self, task_list: any) -> list:

        print(len(task_list))
        status_re = re.compile(r"'status':\s(\d+),")
        status = re.findall(status_re, str(task_list))
        "task list status: 5 finished ; 2 downloading  107 connecting error; 3 paused;"
        task_list_status = [status.count('5'), status.count('2'), status.count('107')]
        print('当前下载任务列表状态码',task_list_status)

        return task_list_status

    def judge_in_list(self, down_link: str, tasklist: list) -> bool:
        #用来提取下载连接中文件名的正则表达式
        re_get_filename = re.compile(r'\/.+\/(.*\.\w{3,4})[\?]?')
        filename = re.findall(pattern=re_get_filename, string=down_link)
        if len(filename) == 0:
            print("下载任务url %s无匹配下载文件名称")
        else:
            if (str(tasklist).find(filename[0]) != -1):
                print("下载任务url提取的文件名：%s在下载任务列表中已存在"%filename)
                return True
            else:
                print("下载url %s中存在文件名%s，但是在下载任务列表中不存在该任务"%(down_link, filename))
        if down_link in tasklist:
            print("目标链接不存在于任务列表当中")
            return True
        else:
            print("目标链接已存在于任务列表当中，不进行下载")
            return False

    def start_down(self, down_link: str):
        add_task_payload = {
            'type': "url",
            'destination': "%s" % self.down_path,
            'create_list': 'true',
            'url': '["%s"]' % down_link,
            'api': 'SYNO.DownloadStation2.Task',
            'method': 'create',
            'version': '2'}

        start_down_result = self.connect(data=add_task_payload)
        start_task_status = json.loads(start_down_result).get('success')
        if (start_task_status):
            print(down_link+'\n')
            print("successfully add task to synology")
        else:
            print("failed to add download task to synology")
        "这里我们需要稍微延迟一下，因为添加任务后连接服务器时不是处于正在状态码2的下载状态，继续添加可能会在短时间导致同时下载数超过2"
        print("sleeping 10s, waiting ")
        sleep(10)

    def synodown(self, down_link: str):

        # snoauto = SnoAuto(cookies, entry_url, header, 'nts')

        response, task_list = self.get_task_list()
        task_status = self.get_task_staus(response)

        while ((task_status[1] > self.max_down_task) or (task_status[2] > self.max_error_task)):
            print("当前正在进行下载任务过多，超过 %d 设定阈值， 或者下载错误任务数超过 %d 设定阈值"%(self.max_down_task, self.max_error_task))
            sleep(60)
            response, task_list = self.get_task_list()
            task_status = self.get_task_staus(response)

        if not (self.judge_in_list(down_link, task_list)):
            self.start_down(down_link)
            print("完成该项下载任务")
